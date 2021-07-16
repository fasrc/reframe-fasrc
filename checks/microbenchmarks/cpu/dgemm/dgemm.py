# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class DGEMMTest(rfm.RegressionTest):
    def __init__(self):
        self.descr = 'DGEMM performance test'
        self.sourcepath = 'dgemm.c'

        # the perf patterns are automaticaly generated inside sanity
        self.perf_patterns = {}
        self.modules = ['intel-mkl/2021.2.0-fasrc01']
        self.valid_systems = ['cannon:local','cannon:test','fasse:fasse','test:rc-testing']
        self.valid_prog_environs = ['intel']

        self.num_tasks = 1
        self.use_multithreading = False
        self.executable_opts = ['6144', '12288', '3072']
        self.build_system = 'SingleSource'
        self.build_system.cflags = ['-O3']
        self.sys_reference = {
            'cannon:local': (2400.0, -0.15, None, 'Gflop/s'),
            'cannon:test': (2400.0, -0.15, None, 'Gflop/s'),
            'fasse:fasse': (2400.0, -0.15, None, 'Gflop/s'),
            '*': (0, None, None, 'Gflop/s'),
        }


    @run_before('compile')
    def setflags(self):
        if self.current_environ.name.startswith('gnu'):
            self.build_system.cflags += ['-fopenmp']
        elif self.current_environ.name.startswith('intel'):
            self.build_system.cppflags = [
                '-DMKL_ILP64', '-I${MKLROOT}/include'
            ]
            self.build_system.cflags = ['-qopenmp']
            self.build_system.ldflags = [
                '-mkl', '-static-intel', '-liomp5', '-lpthread', '-lm', '-ldl'
            ]

    @run_before('run')
    def set_tasks(self):
        if self.current_partition.fullname in ['test:rc-testing']:
            self.num_cpus_per_task = 36
        elif self.current_partition.fullname in ['cannon:local','cannon:test', 'fasse:fasse']:
            self.num_cpus_per_task = 48
        else:
            self.num_cpus_per_task = 32

        if self.num_cpus_per_task:
            self.variables = {
                'OMP_NUM_THREADS': str(self.num_cpus_per_task)
            }
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']

    @sanity_function
    def eval_sanity(self):
        all_tested_nodes = sn.evaluate(sn.extractall(
            r'(?P<hostname>\S+):\s+Time for \d+ DGEMM operations',
            self.stdout, 'hostname'))
        num_tested_nodes = len(all_tested_nodes)
        failure_msg = ('Requested %s node(s), but found %s node(s)' %
                       (self.job.num_tasks, num_tested_nodes))
        sn.evaluate(sn.assert_eq(num_tested_nodes, self.job.num_tasks,
                                 msg=failure_msg))

        for hostname in all_tested_nodes:
            partition_name = self.current_partition.fullname
            ref_name = '%s:%s' % (partition_name, hostname)
            self.reference[ref_name] = self.sys_reference.get(
                partition_name, (0.0, None, None, 'Gflop/s')
            )
            self.perf_patterns[hostname] = sn.extractsingle(
                r'%s:\s+Avg\. performance\s+:\s+(?P<gflops>\S+)'
                r'\sGflop/s' % hostname, self.stdout, 'gflops', float)

        return True
