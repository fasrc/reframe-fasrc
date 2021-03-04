# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.parameterized_test(['nompi'], ['mpi'])
class FFTWTest(rfm.RegressionTest):
    def __init__(self, exec_mode):
        self.sourcepath = 'fftw_benchmark.c'
        self.build_system = 'SingleSource'
        self.valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
        self.modules = ['fftw']
        self.num_tasks_per_node = 12
        self.num_gpus_per_node = 0
        self.sanity_patterns = sn.assert_eq(
            sn.count(sn.findall(r'execution time', self.stdout)), 1)
        self.build_system.cflags = ['-O2','-lfftw3']
        self.valid_prog_environs = ['gnu-mpi', 'intel-mpi']

        self.perf_patterns = {
            'fftw_exec_time': sn.extractsingle(
                r'execution time:\s+(?P<exec_time>\S+)', self.stdout,
                'exec_time', float),
        }

        if exec_mode == 'nompi':
            self.num_tasks = 12
            self.executable_opts = ['72 12 1000 0']
            self.reference = {
                'cannon:test': {
                    'fftw_exec_time': (0.5, None, 0.05, 's'),
                },
                'fasse:fasse': {
                    'fftw_exec_time': (0.5, None, 0.05, 's'),
                },
                '*': {
                    'fftw_exec_time': (0.59, None, None, 's'),
                },
            }

        else:
            self.num_tasks = 72
            self.executable_opts = ['144 72 200 1']
            self.reference = {
                'cannon:test': {
                    'fftw_exec_time': (0.6, None, 0.05, 's'),
                },
                'fasse:fasse': {
                    'fftw_exec_time': (0.6, None, 0.05, 's'),
                },
                '*': {
                    'fftw_exec_time': (0.59, None, None, 's'),
                },
            }


    @rfm.run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']
