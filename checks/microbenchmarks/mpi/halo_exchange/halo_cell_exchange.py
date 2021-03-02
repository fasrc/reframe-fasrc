# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class HaloCellExchangeTest(rfm.RegressionTest):
    def __init__(self):
        self.sourcepath = 'halo_cell_exchange.c'
        self.build_system = 'SingleSource'
        self.build_system.cflags = ['-O2']
        self.valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
        self.valid_prog_environs = ['gnu-mpi','intel-mpi']
        self.num_tasks = 6
        self.num_tasks_per_node = 1
        self.num_gpus_per_node = 0

        self.executable_opts = ['input.txt']

        self.sanity_patterns = sn.assert_eq(
            sn.count(sn.findall(r'halo_cell_exchange', self.stdout)), 9)

        self.perf_patterns = {
            'time_2_10': sn.extractsingle(
                r'halo_cell_exchange 6 2 1 1 10 10 10'
                r' \S+ (?P<time_mpi>\S+)', self.stdout,
                'time_mpi', float),
            'time_2_10000': sn.extractsingle(
                r'halo_cell_exchange 6 2 1 1 10000 10000 10000'
                r' \S+ (?P<time_mpi>\S+)', self.stdout,
                'time_mpi', float),
            'time_2_1000000': sn.extractsingle(
                r'halo_cell_exchange 6 2 1 1 1000000 1000000 1000000'
                r' \S+ (?P<time_mpi>\S+)', self.stdout,
                'time_mpi', float),
            'time_4_10': sn.extractsingle(
                r'halo_cell_exchange 6 2 2 1 10 10 10'
                r' \S+ (?P<time_mpi>\S+)', self.stdout,
                'time_mpi', float),
            'time_4_10000': sn.extractsingle(
                r'halo_cell_exchange 6 2 2 1 10000 10000 10000'
                r' \S+ (?P<time_mpi>\S+)', self.stdout,
                'time_mpi', float),
            'time_4_1000000': sn.extractsingle(
                r'halo_cell_exchange 6 2 2 1 1000000 1000000 1000000'
                r' \S+ (?P<time_mpi>\S+)', self.stdout,
                'time_mpi', float),
            'time_6_10': sn.extractsingle(
                r'halo_cell_exchange 6 3 2 1 10 10 10'
                r' \S+ (?P<time_mpi>\S+)', self.stdout,
                'time_mpi', float),
            'time_6_10000': sn.extractsingle(
                r'halo_cell_exchange 6 3 2 1 10000 10000 10000'
                r' \S+ (?P<time_mpi>\S+)', self.stdout,
                'time_mpi', float),
            'time_6_1000000': sn.extractsingle(
                r'halo_cell_exchange 6 3 2 1 1000000 1000000 1000000'
                r' \S+ (?P<time_mpi>\S+)', self.stdout,
                'time_mpi', float)
        }

        self.reference = {
            'cannon:test': {
                'time_2_10': (1e-05, None, 0.50, 's'),
                'time_2_10000': (6e-05, None, 0.50, 's'),
                'time_2_1000000': (1e-03, None, 0.50, 's'),
                'time_4_10': (2e-05, None, 0.50, 's'),
                'time_4_10000': (7e-05, None, 0.50, 's'),
                'time_4_1000000': (1e-03, None, 0.50, 's'),
                'time_6_10': (2e-05, None, 0.50, 's'),
                'time_6_10000': (6e-05, None, 0.50, 's'),
                'time_6_1000000': (1e-03, None, 0.50, 's')
            },
            '*': {
                'time_2_10': (3.925395e-06, None, None, 's'),
                'time_2_10000': (9.721279e-06, None, None, 's'),
                'time_2_1000000': (4.934530e-04, None, None, 's'),
                'time_4_10': (5.878997e-06, None, None, 's'),
                'time_4_10000': (1.495080e-05, None, None, 's'),
                'time_4_1000000': (6.791397e-04, None, None, 's'),
                'time_6_10': (5.428815e-06, None, None, 's'),
                'time_6_10000': (1.540580e-05, None, None, 's'),
                'time_6_1000000': (9.179296e-04, None, None, 's')
            },
        }

    @rfm.run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']

    @rfm.run_before('run')
    def set_pmix(self):
        self.job.launcher.options = ['--mpi=pmix']
