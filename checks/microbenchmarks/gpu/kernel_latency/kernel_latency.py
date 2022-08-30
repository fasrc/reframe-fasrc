# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class KernelLatencyTest(rfm.RegressionTest):
    valid_systems = ['cannon:local-gpu','cannon:gpu_test','fasse:fasse_gpu','test:gpu']
    valid_prog_environs = ['gpu']

    build_system = 'Make'
    executable = './kernel_latency.x'

    kernel_version = parameter(['sync', 'async'])

    @run_before('performance')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'latency': sn.max(sn.extractall(
                r'\[\S+\] \[gpu \d+\] Kernel launch latency: '
                r'(?P<latency>\S+) us', self.stdout, 'latency', float))
        }

    @run_before('compile')
    def set_cxxflags(self):
        if self.kernel_version == 'sync':
            self.build_system.cppflags = ['-D SYNCKERNEL=1']
        else:
            self.build_system.cppflags = ['-D SYNCKERNEL=0']

    @run_before('performance')
    def set_reference(self):
        self.sys_reference = {
            'sync': {
                'cannon:local-gpu': {
                    'latency': (6.0, None, 0.10, 'us')
                },
                'cannon:gpu_test': {
                    'latency': (4.0, None, 0.10, 'us')
                },
                '*': {
                    'latency': (15.1, None, None, 'us')
                },
            },
            'async': {
                'cannon:local-gpu': {
                    'latency': (6.0, None, 0.10, 'us')
                },
                'cannon:gpu_test': {
                    'latency': (4.0, None, 0.10, 'us')
                },
                '*': {
                    'latency': (2.2, None, None, 'us')
                },
            },
        }
        self.reference = self.sys_reference[self.kernel_version]


    @property
    @deferrable
    def num_tasks_assigned(self):
        return self.job.num_tasks

    @run_after('setup')
    def select_makefile(self):
        self.build_system.makefile = 'makefile.cuda'

    @run_before('run')
    def set_num_gpus_per_node(self):
        cp = self.current_partition.fullname
        if cp in {'cannon:local-gpu', 'fasse:fasse_gpu', 'test:gpu'}:
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

    @sanity_function
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
