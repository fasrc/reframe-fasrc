# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class HPCGCheckRef(rfm.RegressionTest):
    def __init__(self):
        self.descr = 'HPCG reference benchmark'
        self.valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
        self.valid_prog_environs = ['gnu-mpi']

        self.build_system = 'Make'
        self.build_system.options = ['arch=MPI_GCC_OMP']
        self.sourcesdir = 'https://github.com/hpcg-benchmark/hpcg.git'
        self.executable = 'bin/xhpcg'
        self.executable_opts = ['--nx=104', '--ny=104', '--nz=104', '-t2']
        # use glob to catch the output file suffix dependent on execution time
        self.output_file = sn.getitem(sn.glob('HPCG*.txt'), 0)

        self.num_tasks = 96
        self.num_cpus_per_task = 1

        self.system_num_tasks = {
            'cannon:test':  48,
            'fasse:fasse': 48,
            'test:rc-testing':  32,
            '*': 32
        }

        self.reference = {
            'cannon:test': {
                'gflops': (28, -0.1, None, 'Gflop/s')
            },
            'fasse:fasse': {
                'gflops': (28, -0.1, None, 'Gflop/s')
            },
            '*': {
                'gflops': (13.4, None, None, 'Gflop/s')
            }
        }


    @property
    @deferrable
    def num_tasks_assigned(self):
        return self.job.num_tasks

    @run_before('compile')
    def set_tasks(self):
        self.num_tasks_per_node = self.system_num_tasks.get(
            self.current_partition.fullname, 1
        )

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=3G']

    @run_before('performance')
    def set_performance(self):
        num_nodes = self.num_tasks_assigned / self.num_tasks_per_node
        self.perf_patterns = {
            'gflops': sn.extractsingle(
                r'HPCG result is VALID with a GFLOP\/s rating of=\s*'
                r'(?P<perf>\S+)',
                self.output_file, 'perf',  float) / num_nodes
        }

    @run_before('sanity')
    def set_sanity(self):
        self.sanity_patterns = sn.all([
            sn.assert_eq(4, sn.count(
                sn.findall(r'PASSED', self.output_file))),
            sn.assert_eq(0, self.num_tasks_assigned % self.num_tasks_per_node)
        ])


@rfm.simple_test
class HPCGCheckMKL(rfm.RegressionTest):
    def __init__(self):
        self.descr = 'HPCG benchmark Intel MKL implementation'
        self.valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
        self.valid_prog_environs = ['intel-intelmpi']
        self.modules = ['intel-mkl']
        self.build_system = 'Make'
        self.prebuild_cmds = ['cp -r ${MKLROOT}/share/mkl/benchmarks/hpcg/* .',
                             './configure INTELMPI_IOMP_AVX2']

        self.num_tasks = 4
        self.problem_size = 104

        self.env_vars = {
            'HUGETLB_VERBOSE': '0',
            'MPICH_MAX_THREAD_SAFETY': 'multiple',
            'MPICH_USE_DMAPP_COLL': '1',
            'PMI_NO_FORK': '1',
            'KMP_AFFINITY': 'granularity=fine,compact'
        }

        self.executable = 'bin/xhpcg_avx2'
        self.executable_opts = [f'--nx={self.problem_size}',
                                f'--ny={self.problem_size}',
                                f'--nz={self.problem_size}', '-t2']

        self.reference = {
            'cannon:test': {
                'gflops': (39, -0.1, None, 'Gflop/s')
            },
            'fasse:fasse': {
                'gflops': (39, -0.1, None, 'Gflop/s')
            },
            '*': {
                'gflops': (13.4, None, None, 'Gflop/s')
            }
        }

    @property
    @deferrable
    def num_tasks_assigned(self):
        return self.job.num_tasks

    @property
    @sanity_function
    def outfile_lazy(self):
        pattern = (f'n{self.problem_size}-{self.job.num_tasks}p-'
                   f'{self.num_cpus_per_task}t*.*')
        return sn.getitem(sn.glob(pattern), 0)

    @run_before('compile')
    def set_tasks(self):
        if self.current_partition.fullname in ['cannon:test', 'fasse:fasse']:
            self.num_tasks_per_node = 2
            self.num_cpus_per_task = 24
        elif self.current_partition.fullname in ['test:rc-testing']:
            self.num_tasks_per_node = 2
            self.num_cpus_per_task = 16
        else:
            self.num_tasks_per_node = 2
            self.num_cpus_per_task = 16

    @run_after('setup')
    def prepare_test(self):
        self.env_vars['OMP_NUM_THREADS'] = str(self.num_cpus_per_task)

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=3G']

    @run_before('performance')
    def set_performance(self):
        # since this is a flexible test, we divide the extracted
        # performance by the number of nodes and compare
        # against a single reference
        num_nodes = self.num_tasks_assigned / self.num_tasks_per_node
        self.perf_patterns = {
            'gflops': sn.extractsingle(
                r'HPCG result is VALID with a GFLOP\/s rating of(=|:)\s*'
                r'(?P<perf>\S+)',
                self.outfile_lazy, 'perf',  float) / num_nodes
        }

    @run_before('sanity')
    def set_sanity(self):
        self.sanity_patterns = sn.all([
            sn.assert_not_found(
                r'invalid because the ratio',
                self.outfile_lazy,
                msg='number of processes assigned could not be factorized'
            ),
            sn.assert_eq(
                4, sn.count(sn.findall(r'PASSED', self.outfile_lazy))
            ),
            sn.assert_eq(0, self.num_tasks_assigned % self.num_tasks_per_node)
        ])
