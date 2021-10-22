# Copyright 2016-2020 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class GPUdgemmTest(rfm.RegressionTest):
    def __init__(self):
        self.valid_systems = ['cannon:local-gpu','cannon:gpu_test','fasse:fasse_gpu','test:gpu']
        self.valid_prog_environs = ['gpu']
        self.build_system = 'Make'
        self.executable = './dgemm.x'
        self.perf_patterns = {
            'perf': sn.min(sn.extractall(
                r'^\s*\[[^\]]*\]\s*GPU\s*\d+: (?P<fp>\S+) TF/s',
                self.stdout, 'fp', float))
        }
        self.reference = {
            'cannon:local-gpu': {
                'perf': (5.2, -0.1, None, 'TF/s per gpu')
            },
            'cannon:gpu_test': {
                'perf': (5.2, -0.1, None, 'TF/s per gpu')
            },
            '*': {
                'perf': (3.35, None, None, 'TF/s per gpu')
            },
        }

    @sanity_function
    def assert_num_gpus(self):
        return sn.assert_eq(
            sn.count(sn.findall(r'^\s*\[[^\]]*\]\s*Test passed', self.stdout)),
            sn.getattr(self.job, 'num_tasks'))

    @run_before('compile')
    def select_makefile(self):
        self.build_system.makefile = 'makefile.cuda'

    @run_before('run')
    def set_gpus_per_node(self):
        cp = self.current_partition.fullname
        if cp in {'cannon:local-gpu', 'fasse:fasse_gpu', 'test:gpu'}:
            self.num_gpus_per_node = 4
            self.num_cpus_per_task = 4
            self.num_tasks = 1
        elif cp in {'cannon:gpu_test'}:
            self.num_gpus_per_node = 2
            self.num_cpus_per_task = 2
            self.num_tasks = 1
        else:
            self.num_gpus_per_node = 1
            self.num_cpus_per_task = 1
            self.num_tasks = 1

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']
