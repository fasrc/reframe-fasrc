# Copyright 2016-2020 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2026 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class GPUFryerFP32TensorTest(rfm.RunOnlyRegressionTest):
    def __init__(self):
        self.valid_systems = ['cannon:local-gpu','cannon:gpu_test','fasse:fasse_gpu','test:gpu','arm:local']
        self.build_system = 'SingleSource'
        self.executable = 'singularity run --nv --bind /usr/lib64/libnvidia-ml.so.1:/usr/lib/x86_64-linux-gnu/libnvidia-ml.so.1 /n/sw/singularity_images/FAS/gpu-fryer/gpu-fryer_1.1.0.sif --use-fp32 60'
        self.valid_prog_environs = ['gpu']
        self.time_limit = '10m'
        self.reference = {
            'cannon:local-gpu': {
                'perf': (5.2, -0.1, None, 'Gflops/s per gpu')
            },
            'cannon:gpu_test': {
                'perf': (5.2, -0.1, None, 'Gflops/s per gpu')
            },
            '*': {
                'perf': (3.35, None, None, 'Gflops/s per gpu')
            },
        }

    @sanity_function
    def assert_sanity(self):
        return sn.assert_found(r'All GPUs seem healthy', self.stdout)

    def _extract_metric(self, metric):
        return sn.extractall(r'GPU \#\d+:\s+(?P<perf>\S+)\s+Gflops\/s.+', self.stdout, metric, float)

    @performance_function('Gflop/s per gpu')
    def gpu_perf_min(self):
        '''Lowest performance recorded among all the selected devices.'''
        return sn.min(self._extract_metric('perf'))

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
