# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


class StridedBase(rfm.RegressionTest):
    def __init__(self):
        self.sourcepath = 'strides.cpp'
        self.build_system = 'SingleSource'
        self.valid_systems = ['*']
        self.valid_prog_environs = ['builtin','gnu','intel']
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

        self.num_cpus = 32

    @property
    @sn.sanity_function
    def num_tasks_assigned(self):
        return self.job.num_tasks


@rfm.required_version('>=2.16-dev0')
@rfm.simple_test
class StridedBandwidthTest(StridedBase):
    def __init__(self):
        super().__init__()

    @rfm.run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem=4G']
    def set_exec_opts(self):
        # 8-byte stride, using the full cacheline
        self.executable_opts = ['100000000', '1', '%s' % self.num_cpus]


@rfm.required_version('>=2.16-dev0')
@rfm.simple_test
class StridedBandwidthTest64(StridedBase):
    def __init__(self):
        super().__init__()

    @rfm.run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem=4G']
    def set_exec_opts(self):
        # 64-byte stride, using 1/8 of the cacheline
        self.executable_opts = ['100000000', '8', '%s' % self.num_cpus]


@rfm.required_version('>=2.16-dev0')
@rfm.simple_test
class StridedBandwidthTest128(StridedBase):
    def __init__(self):
        super().__init__()

    @rfm.run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem=4G']
    def set_exec_opts(self):
        # 128-byte stride, using 1/8 of every 2nd cacheline
        self.executable_opts = ['100000000', '16', '%s' % self.num_cpus]
