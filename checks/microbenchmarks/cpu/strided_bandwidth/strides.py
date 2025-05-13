# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


class StridedBase(rfm.RegressionTest):
    def __init__(self):
        self.sourcepath = 'strides.cpp'
        self.build_system = 'SingleSource'
        self.valid_systems = ['cannon:local','cannon:local-gpu','cannon:test','fasse:fasse','test:rc-testing','arm:local']
        self.valid_prog_environs = ['builtin','gnu','gpu','intel']
        self.build_system.cxxflags = ['-std=c++11','-lpthread']
        self.num_tasks = 1
        self.num_tasks_per_node = 1

        self.sanity_patterns = sn.assert_eq(
            sn.count(sn.findall(r'bandwidth', self.stdout)),
            self.num_tasks_assigned)

        self.perf_patterns = {
            'bandwidth': sn.extractsingle(
                r'bandwidth: (?P<bw>\S+) GB/s',
                self.stdout, 'bw', float)
        }

        self.system_num_cpus = {
            'cannon:local': 96,
            'cannon:local-gpu': 32,
            'cannon:gpu_test': 16,
            'cannon:test': 48,
            'fasse:fasse': 48,
            'test:rc-testing':  32,
            'arm:local': 72,
            '*': 32,
        }


    @property
    @deferrable
    def num_tasks_assigned(self):
        return self.job.num_tasks


@rfm.simple_test
class StridedBandwidthTest(StridedBase):
    def __init__(self):
        super().__init__()

        self.reference = {
            'cannon:local': {
                'bandwidth': (185, -0.1, None, 'GB/s')
            },
            'cannon:local-gpu': {
                'bandwidth': (156, -0.1, None, 'GB/s')
            },
            'cannon:gpu_test': {
                'bandwidth': (84, -0.1, None, 'GB/s')
            },
            'cannon:test': {
                'bandwidth': (185, -0.1, None, 'GB/s')
            },
            'fasse:fasse': {
                'bandwidth': (90, -0.1, None, 'GB/s')
            },
            '*': {
                'bandwidth': (270, None, None, 'GB/s')
            },
        }

    @run_before('run')
    def set_exec_opts(self):
        self.num_cpus_per_task = self.system_num_cpus[self.current_partition.fullname]

        # 8-byte stride, using the full cacheline
        self.executable_opts = ['100000000', '1', '%s' % self.num_cpus_per_task]

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=3G']

@rfm.simple_test
class StridedBandwidthTest64(StridedBase):
    def __init__(self):
        super().__init__()

        self.reference = {
            'cannon:local': {
                'bandwidth': (23, -0.1, None, 'GB/s')
            },
            'cannon:local-gpu': {
                'bandwidth': (22, -0.1, None, 'GB/s')
            },
            'cannon:gpu_test': {
                'bandwidth': (12, -0.1, None, 'GB/s')
            },
            'cannon:test': {
                'bandwidth': (23, -0.1, None, 'GB/s')
            },
            'fasse:fasse': {
                'bandwidth': (23, -0.1, None, 'GB/s')
            },
            '*': {
                'bandwidth': (270, None, None, 'GB/s')
            },
        }

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=3G']

    @run_before('run')
    def set_exec_opts(self):
        self.num_cpus_per_task = self.system_num_cpus[self.current_partition.fullname]

        # 64-byte stride, using 1/8 of the cacheline
        self.executable_opts = ['100000000', '8', '%s' % self.num_cpus_per_task]


@rfm.simple_test
class StridedBandwidthTest128(StridedBase):
    def __init__(self):
        super().__init__()

        self.reference = {
            'cannon:local': {
                'bandwidth': (12, -0.1, None, 'GB/s')
            },
            'cannon:local-gpu': {
                'bandwidth': (14, -0.1, None, 'GB/s')
            },
            'cannon:gpu_test': {
                'bandwidth': (8, -0.1, None, 'GB/s')
            },
            'cannon:test': {
                'bandwidth': (12, -0.1, None, 'GB/s')
            },
            'fasse:fasse': {
                'bandwidth': (17, -0.1, None, 'GB/s')
            },
            '*': {
                'bandwidth': (270, None, None, 'GB/s')
            },
        }

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=3G']

    @run_before('run')
    def set_exec_opts(self):
        self.num_cpus_per_task = self.system_num_cpus[self.current_partition.fullname]

        # 128-byte stride, using 1/8 of every 2nd cacheline
        self.executable_opts = ['100000000', '16', '%s' % self.num_cpus_per_task]
