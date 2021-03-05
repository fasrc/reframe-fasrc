# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.parameterized_test(['no'], ['2M'])
class AllocSpeedTest(rfm.RegressionTest):
    def __init__(self, hugepages):
        self.descr = 'Time to allocate 4096 MB using %s hugepages' % hugepages
        self.sourcepath = 'alloc_speed.cpp'
        self.build_system = 'SingleSource'
        self.build_system.cxxflags = ['-O3', '-std=c++11']
        self.valid_systems = ['*']
        self.valid_prog_environs = ['*']

        self.sanity_patterns = sn.assert_found('4096 MB', self.stdout)
        self.perf_patterns = {
            'time': sn.extractsingle(r'4096 MB, allocation time (?P<time>\S+)',
                                     self.stdout, 'time', float)
        }

        self.sys_reference = {
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
        self.reference = self.sys_reference[hugepages]



    @rfm.run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem=5G']
