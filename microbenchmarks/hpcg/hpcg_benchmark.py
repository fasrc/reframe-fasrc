# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os
import reframe as rfm
import reframe.utility.sanity as sn


class HPCGHookMixin:
    @rfm.run_before('run')
    def guide_node_guess(self):
        '''Guide the node guess based on the test's needs.'''

        # Prelim guess
        ntasks_per_node = self.num_tasks_per_node or 1
        self.job.num_tasks_per_node = ntasks_per_node
        n = int(self.job.guess_num_tasks()/ntasks_per_node)

        def first_factor(x):
            if x <= 1:
                return 1

            for i in range(2, x+1):
                if x % i == 0:
                    return i

        def is_prime(x):
            return first_factor(x) == x

        # Correct the prelim node numbers
        # n = 11 would be the first number not meeting HPCG's condition
        while n > 10:
            x = int(n/first_factor(n))

            # If x==1, n is prime
            # if x > 8 and prime, it would also not meet HPCG's aspect ratio
            if x == 1 or (is_prime(x) and x > 8):
                n -= 1
            else:
                break

        self.num_tasks = int(n*ntasks_per_node)
        self.num_tasks_per_node = ntasks_per_node


@rfm.simple_test
class HPCGCheckRef(rfm.RegressionTest, HPCGHookMixin):
    def __init__(self):
        self.descr = 'HPCG reference benchmark'
        self.valid_systems = ['test:rc-testing']
        self.valid_prog_environs = ['gnu-mpi']

        self.build_system = 'Make'
        self.build_system.options = ['arch=MPI_GCC_OMP']
        self.sourcesdir = 'https://github.com/hpcg-benchmark/hpcg.git'
        self.executable = 'bin/xhpcg'
        self.executable_opts = ['--nx=104', '--ny=104', '--nz=104', '-t2']
        # use glob to catch the output file suffix dependent on execution time
        self.output_file = sn.getitem(sn.glob('HPCG*.txt'), 0)

        self.num_tasks = 72
        self.num_cpus_per_task = 1

    @property
    @sn.sanity_function
    def num_tasks_assigned(self):
        return self.job.num_tasks

    @rfm.run_before('compile')
    def set_tasks(self):
        self.num_tasks_per_node = 36

    @rfm.run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']

    @rfm.run_before('performance')
    def set_performance(self):
        num_nodes = self.num_tasks_assigned / self.num_tasks_per_node
        self.perf_patterns = {
            'gflops': sn.extractsingle(
                r'HPCG result is VALID with a GFLOP\/s rating of=\s*'
                r'(?P<perf>\S+)',
                self.output_file, 'perf',  float) / num_nodes
        }

    @rfm.run_before('sanity')
    def set_sanity(self):
        self.sanity_patterns = sn.all([
            sn.assert_eq(4, sn.count(
                sn.findall(r'PASSED', self.output_file))),
            sn.assert_eq(0, self.num_tasks_assigned % self.num_tasks_per_node)
        ])


@rfm.simple_test
class HPCGCheckMKL(rfm.RegressionTest, HPCGHookMixin):
    def __init__(self):
        self.descr = 'HPCG benchmark Intel MKL implementation'
        self.valid_systems = ['test:rc-testing']
        self.valid_prog_environs = ['intel-mpi']
        self.modules = ['intel-mkl/2019.5.281-fasrc01']
        self.build_system = 'Make'
        self.prebuild_cmds = ['cp -r ${MKLROOT}/benchmarks/hpcg/* .',
                             './configure OPENMPI_IOMP_AVX2']

        self.num_tasks = 4
        self.problem_size = 104

        self.variables = {
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


    @property
    @sn.sanity_function
    def num_tasks_assigned(self):
        return self.job.num_tasks

    @property
    @sn.sanity_function
    def outfile_lazy(self):
        pattern = (f'n{self.problem_size}-{self.job.num_tasks}p-'
                   f'{self.num_cpus_per_task}t*.*')
        return sn.getitem(sn.glob(pattern), 0)

    @rfm.run_before('compile')
    def set_tasks(self):
        self.num_tasks_per_node = 2
        self.num_cpus_per_task = 18

    @rfm.run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']

    @rfm.run_before('performance')
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

    @rfm.run_before('sanity')
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


@rfm.simple_test
class HPCG_GPUCheck(rfm.RunOnlyRegressionTest, HPCGHookMixin):
    def __init__(self):
        self.descr = 'HPCG benchmark on GPUs'
        self.sourcesdir = os.path.join(self.current_system.resourcesdir,
                                       'HPCG')

        # there's no binary with support for CUDA 10 yet
        self.valid_systems = ['test:gpu']
        self.valid_prog_environs = ['gpu']
        self.executable = 'xhpcg_gpu_3.1'
        self.prerun_cmds = ['chmod +x %s' % self.executable]
        self.num_tasks = 0
        self.num_tasks_per_node = 1
        self.num_cpus_per_task = 12
        self.variables = {
            'PMI_NO_FORK': '1',
            'MPICH_USE_DMAPP_COLL': '1',
            'OMP_SCHEDULE': 'static',
            'OMP_NUM_THREADS': str(self.num_cpus_per_task),
            'HUGETLB_VERBOSE': '0',
            'HUGETLB_DEFAULT_PAGE_SIZE': '8M',
        }

        self.output_file = sn.getitem(sn.glob('*.yaml'), 0)

        num_nodes = self.num_tasks_assigned / self.num_tasks_per_node
        self.perf_patterns = {
            'gflops': sn.extractsingle(
                r'HPCG result is VALID with a GFLOP\/s rating of:\s*'
                r'(?P<perf>\S+)',
                self.output_file, 'perf',  float) / num_nodes
        }

        self.sanity_patterns = sn.all([
            sn.assert_eq(4, sn.count(
                sn.findall(r'PASSED', self.output_file))),
            sn.assert_eq(0, self.num_tasks_assigned % self.num_tasks_per_node)
        ])

    @property
    @sn.sanity_function
    def num_tasks_assigned(self):
        return self.job.num_tasks

    @rfm.run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']
