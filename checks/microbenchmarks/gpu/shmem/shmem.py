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
        self.valid_systems = ['cannon:gpu_test','fasse:fasse_gpu','test:gpu']
        self.valid_prog_environs = ['gpu']
        self.build_system = 'Make'
        self.executable = 'shmem.x'
        self.sanity_patterns = self.assert_count_gpus()
        self.perf_patterns = {
            'bandwidth': sn.min(sn.extractall(
                r'^\s*\[[^\]]*\]\s*GPU\s*\d+: '
                r'Bandwidth\(double\) (?P<bw>\S+) GB/s',
                self.stdout, 'bw', float))
        }
        self.reference = {
            # theoretical limit for P100:
            # 8 [B/cycle] * 1.328 [GHz] * 16 [bankwidth] * 56 [SM] = 9520 GB/s
            'cannon:gpu_test': {
                'bandwidth': (13000, -0.01, None, 'GB/s')
            },
            '*': {
                'bandwidth': (8850, None, None, 'GB/s')
            },
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
        cp = self.current_partition.fullname
        if cp in {'fasse:fasse_gpu', 'test:gpu'}:
            self.num_gpus_per_node = 4
            self.num_cpus_per_task = 4
            self.num_tasks = 1
        elif cp in {'cannon:gpu_test'}:
            self.num_gpus_per_node = 2
            self.num_cpus_per_task = 2
            self.num_tasks = 1
        else:
            self.num_gpus_per_node = 1
            self.num_cpus_per_task = 1
            self.num_tasks = 1
