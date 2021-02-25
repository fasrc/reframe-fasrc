# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class GPUShmemTest(rfm.RegressionTest):
    def __init__(self):
        self.valid_systems = ['test:gpu']
        self.valid_prog_environs = ['gpu']
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.exclusive_access = True
        self.build_system = 'Make'
        self.executable = 'shmem.x'
        self.sanity_patterns = self.assert_count_gpus()
        self.perf_patterns = {
            'bandwidth': sn.min(sn.extractall(
                r'^\s*\[[^\]]*\]\s*GPU\s*\d+: '
                r'Bandwidth\(double\) (?P<bw>\S+) GB/s',
                self.stdout, 'bw', float))
        }

    @property
    @sn.sanity_function
    def num_tasks_assigned(self):
        return self.job.num_tasks

    @sn.sanity_function
    def assert_count_gpus(self):
        return sn.assert_eq(
            sn.count(sn.findall(r'Bandwidth', self.stdout)),
            self.num_tasks_assigned * 2 * self.num_gpus_per_node)

    @rfm.run_after('setup')
    def select_makefile(self):
        self.build_system.makefile = 'makefile.cuda'

    @rfm.run_before('run')
    def set_gpus_per_node(self):
        self.num_gpus_per_node = 4
