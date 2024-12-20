# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os

import reframe as rfm
import reframe.utility.sanity as sn
import reframe.utility.osext as osext

@rfm.simple_test
class GpuBurnTest(rfm.RegressionTest):
    def __init__(self):
        self.valid_systems = ['cannon:local-gpu','cannon:gpu_test','fasse:fasse_gpu','test:gpu','arm:local']
        self.descr = 'GPU burn test'
        self.valid_prog_environs = ['gpu']
        self.executable_opts = ['-d', '40']
        self.build_system = 'Make'
        self.build_system.makefile = 'makefile.cuda'
        self.executable = './gpu_burn.x'
        self.reference = {
            'cannon:local-gpu': {
                'perf': (6200, -0.10, None, 'Gflop/s per gpu'),
            },
            'cannon:gpu_test': {
                'perf': (6200, -0.10, None, 'Gflop/s per gpu'),
            },
            'test:gpu': {
                'perf': (4115, None, None, 'Gflop/s per gpu'),
            },
            '*': {
                'perf': (4115, None, None, 'Gflop/s per gpu'),
            },
            '*': {'temp': (0, None, None, 'degC')}
        }

    @property
    @deferrable
    def num_tasks_assigned(self):
        return self.job.num_tasks * self.num_gpus_per_node

    @run_before('run')
    def set_gpus_per_node(self):
        cp = self.current_partition.fullname
        if cp in {'cannon:local-gpu', 'fasse:fasse_gpu', 'test:gpu'}:
            self.num_gpus_per_node = 4
            self.num_cpus_per_task = 4
            self.num_tasks = 1
        else:
            self.num_gpus_per_node = 1
            self.num_cpus_per_task = 1
            self.num_tasks = 1

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']

    @sanity_function
    def assert_sanity(self):
        num_gpus_detected = sn.extractsingle(
            r'==> devices selected \((\d+)\)', self.stdout, 1, int
        )
        return sn.assert_eq(
            sn.count(sn.findall(r'GPU\s+\d+\(OK\)', self.stdout)),
            num_gpus_detected
        )

    def _extract_metric(self, metric):
        return sn.extractall(
            r'GPU\s+\d+\(OK\):\s+(?P<perf>\S+)\s+GF/s\s+'
            r'(?P<temp>\S+)\s+Celsius', self.stdout, metric, float
        )

    @performance_function('Gflop/s per gpu')
    def gpu_perf_min(self):
        '''Lowest performance recorded among all the selected devices.'''
        return sn.min(self._extract_metric('perf'))

    @performance_function('degC')
    def gpu_temp_max(self):
        '''Maximum temperature recorded among all the selected devices.'''
        return sn.max(self._extract_metric('temp'))
