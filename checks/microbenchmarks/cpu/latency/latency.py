# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class CPULatencyTest(rfm.RegressionTest):
    def __init__(self):
        self.sourcepath = 'latency.cpp'
        self.build_system = 'SingleSource'
        self.valid_systems = ['*']
        self.valid_prog_environs = ['*']
        self.num_tasks = 1
        self.num_tasks_per_node = 1

        self.build_system.cxxflags = ['-std=c++11','-lpthread','-O3']

        self.executable_opts = ['16000', '128000', '8000000', '500000000']

        self.sanity_patterns = sn.assert_eq(
            sn.count(sn.findall(r'latency', self.stdout)),
            self.num_tasks_assigned * len(self.executable_opts))

        def lat_pattern(index):
            return sn.extractsingle(
                r'latency \(ns\) for input size %s: (?P<bw>\S+) clocks' %
                self.executable_opts[index], self.stdout, 'bw', float)

        self.perf_patterns = {
            'latencyL1': lat_pattern(0),
            'latencyL2': lat_pattern(1),
            'latencyL3': lat_pattern(2),
            'latencyMem': lat_pattern(3),
        }

        self.reference = {
            'cannon:local': {
                'latencyL1':  (1.14, None, 0.26, 'ns'),
                'latencyL2':  (4.0, None, 0.26, 'ns'),
                'latencyL3':  (23, None, 0.075, 'ns'),
                'latencyMem': (80, None, 0.05, 'ns')
            },
            'cannon:local-gpu': {
                'latencyL1':  (1.1, None, 0.26, 'ns'),
                'latencyL2':  (4.0, None, 0.26, 'ns'),
                'latencyL3':  (23, None, 0.075, 'ns'),
                'latencyMem': (90, None, 0.05, 'ns')
            },
            'cannon:gpu_test': {
                'latencyL1':  (1.14, None, 0.26, 'ns'),
                'latencyL2':  (4.0, None, 0.26, 'ns'),
                'latencyL3':  (21, None, 0.075, 'ns'),
                'latencyMem': (90, None, 0.05, 'ns')
            },
            'cannon:test': {
                'latencyL1':  (1.14, None, 0.26, 'ns'),
                'latencyL2':  (4.0, None, 0.26, 'ns'),
                'latencyL3':  (26, None, 0.075, 'ns'),
                'latencyMem': (200, None, 0.05, 'ns')
            },
            'fasse:fasse': {
                'latencyL1':  (1.14, None, 0.26, 'ns'),
                'latencyL2':  (4.0, None, 0.26, 'ns'),
                'latencyL3':  (26, None, 0.075, 'ns'),
                'latencyMem': (200, None, 0.05, 'ns')
            },
            '*': {
                'latencyL1':  (1.14, None, None, 'ns'),
                'latencyL2':  (4.0, None, None, 'ns'),
                'latencyL3':  (21, None, None, 'ns'),
                'latencyMem': (79, None, None, 'ns')
            },
        }

    @rfm.run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem=4G']

    @property
    @sn.sanity_function
    def num_tasks_assigned(self):
        return self.job.num_tasks
