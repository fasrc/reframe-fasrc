# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class AllocSpeedTest(rfm.RegressionTest):
    hugepages = parameter(['no', '2M'])
    sourcepath = 'alloc_speed.cpp'
    build_system = 'SingleSource'
    valid_systems = ['*']
    valid_prog_environs = ['*']

    @run_after('init')
    def set_descr(self):
        self.descr = (f'Time to allocate 4096 MB using {self.hugepages} '
                      f'hugepages')

    @run_before('compile')
    def set_cxxflags(self):
        self.build_system.cxxflags = ['-O3', '-std=c++11']

    @sanity_function
    def assert_4GB(self):
        return sn.assert_found('4096 MB', self.stdout)

    @run_before('performance')
    def set_reference(self):
        sys_reference = {
            'no': {
                'cannon:local': {
                    'time': (1.0, None, 0.5, 's')
                },
                'cannon:local-gpu': {
                    'time': (1.0, None, 0.5, 's')
                },
                'cannon:gpu_test': {
                    'time': (1.0, None, 0.5, 's')
                },
                'cannon:test': {
                    'time': (2.0, None, 0.5, 's')
                },
                'fasse:fasse': {
                    'time': (2.0, None, 0.5, 's')
                },
                '*': {
                    'time': (0, None, None, 's')
                },
            },
            '2M': {
                'cannon:local': {
                    'time': (1.0, None, 0.5, 's')
                },
                'cannon:local-gpu': {
                    'time': (1.0, None, 0.5, 's')
                },
                'cannon:gpu_test': {
                    'time': (1.0, None, 0.5, 's')
                },
                'cannon:test': {
                    'time': (2.0, None, 0.5, 's')
                },
                'fasse:fasse': {
                    'time': (2.0, None, 0.5, 's')
                },
                '*': {
                    'time': (0, None, None, 's')
                }
            },
        }
        self.reference = sys_reference[hugepages]

    @performance_function('s')
    def time(self):
        return sn.extractsingle(r'4096 MB, allocation time (?P<time>\S+)',
                                self.stdout, 'time', float)

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem=5G']
