# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.parameterized_test(['sync'], ['async'])
class KernelLatencyTest(rfm.RegressionTest):
    def __init__(self, kernel_version):
        self.valid_systems = ['test:gpu']
        self.valid_prog_environs = ['gpu']

        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.exclusive_access = True
        self.build_system = 'Make'
        self.executable = 'kernel_latency.x'
        if kernel_version == 'sync':
            self.build_system.cppflags = ['-D SYNCKERNEL=1']
        else:
            self.build_system.cppflags = ['-D SYNCKERNEL=0']

        self.sanity_patterns = self.assert_count_gpus()

        self.perf_patterns = {
            'latency': sn.max(sn.extractall(
                r'\[\S+\] \[gpu \d+\] Kernel launch latency: '
                r'(?P<latency>\S+) us', self.stdout, 'latency', float))
        }

    @property
    @sn.sanity_function
    def num_tasks_assigned(self):
        return self.job.num_tasks

    @rfm.run_after('setup')
    def select_makefile(self):
        self.build_system.makefile = 'makefile.cuda'

    @rfm.run_before('run')
    def set_num_gpus_per_node(self):
        self.num_gpus_per_node = 4

    @sn.sanity_function
    def assert_count_gpus(self):
        return sn.all([
            sn.assert_eq(
                sn.count(
                    sn.findall(r'\[\S+\] Found \d+ gpu\(s\)',
                               self.stdout)
                ),
                self.num_tasks_assigned
            ),
            sn.assert_eq(
                sn.count(
                    sn.findall(r'\[\S+\] \[gpu \d+\] Kernel launch '
                               r'latency: \S+ us', self.stdout)
                ),
                self.num_tasks_assigned * self.num_gpus_per_node
            )
        ])
