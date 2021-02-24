# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe.utility.sanity as sn
import reframe as rfm


@rfm.simple_test
class GpuBandwidthCheck(rfm.RegressionTest):
    def __init__(self):
        self.valid_systems = ['test:gpu']
        self.valid_prog_environs = ['gpu']

        # Perform a single bandwidth test with a buffer size of 1024MB
        self.copy_size = 1073741824

        self.build_system = 'Make'
        self.executable = 'memory_bandwidth.x'
        self.build_system.cxxflags = [f'-DCOPY={self.copy_size}']
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.exclusive_access = True

        # perf_patterns and reference will be set by the sanity check function
        self.sanity_patterns = self.do_sanity_check()
        self.perf_patterns = {
            'h2d': sn.min(sn.extractall(self._xfer_pattern('h2d'),
                                        self.stdout, 1, float)),
            'd2h': sn.min(sn.extractall(self._xfer_pattern('d2h'),
                                        self.stdout, 1, float)),
            'd2d': sn.min(sn.extractall(self._xfer_pattern('d2d'),
                                        self.stdout, 1, float)),
        }

    @rfm.run_after('setup')
    def select_makefile(self):
        self.build_system.makefile = 'makefile_memoryBandwidth.cuda'

    @rfm.run_before('run')
    def set_num_gpus_per_node(self):
        self.num_gpus_per_node = 4

    def _xfer_pattern(self, xfer_kind):
        '''generates search pattern for performance analysis'''
        if xfer_kind == 'h2d':
            direction = 'Host to device'
        elif xfer_kind == 'd2h':
            direction = 'Device to host'
        else:
            direction = 'Device to device'

        # Extract the bandwidth corresponding to the right node, transfer and
        # device.
        return (rf'^[^,]*\[[^,]*\]\s*{direction}\s*bandwidth on device'
                r' \d+ is \s*(\S+)\s*Mb/s.')

    @sn.sanity_function
    def do_sanity_check(self):
        node_names = set(sn.extractall(
            r'^\s*\[([^,]{1,100})\]\s*Found %s device\(s\).'
            % self.num_gpus_per_node, self.stdout, 1
        ))
        sn.evaluate(sn.assert_eq(
            self.job.num_tasks, len(node_names),
            msg='requested {0} node(s), got {1} (nodelist: %s)' %
            ','.join(sorted(node_names))))
        good_nodes = set(sn.extractall(
            r'^\s*\[([^,]{1,100})\]\s*Test Result\s*=\s*PASS',
            self.stdout, 1
        ))
        sn.evaluate(sn.assert_eq(
            node_names, good_nodes,
            msg='check failed on the following node(s): %s' %
            ','.join(sorted(node_names - good_nodes)))
        )

        return True
