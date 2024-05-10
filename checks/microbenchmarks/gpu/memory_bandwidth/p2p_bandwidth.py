# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe.utility.sanity as sn
import reframe as rfm


@rfm.simple_test
class P2pBandwidthCheck(rfm.RegressionTest):
    valid_systems = ['cannon:local-gpu','cannon:gpu_test','fasse:fasse_gpu','test:gpu']
    valid_prog_environs = ['gpu']

    # Perform a single bandwidth test with a buffer size of 1024MB
    copy_size = 1073741824

    build_system = 'Make'
    executable = './p2p_bandwidth.x'

    peerAccess = parameter(['peerAccess', 'noPeerAccess'])

    @run_before('compile')
    def set_cxxflags(self):
        if (self.peerAccess == 'peerAccess'):
            self.build_system.cxxflags = [f'-DCOPY={self.copy_size}']
            self.build_system.cxxflags += ['-DP2P']
        else:
            self.build_system.cxxflags = [f'-DCOPY={self.copy_size}']

    @run_before('performance')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'bw': sn.min(sn.extractall(
                r'^[^,]*\[[^\]]*\]\s+GPU\s+\d+\s+(\s*\d+.\d+\s)+',
                self.stdout, 1, float))
        }

    @run_before('performance')
    def set_reference(self):
        self.sys_reference = {
            'peerAccess': {
                'cannon:local-gpu': {
                    'bw':   (28, -0.05, None, 'GB/s'),
                },
                'cannon:gpu_test': {
                    'bw':   (9, -0.05, None, 'GB/s'),
                },
                '*': {
                    'bw':   (172.5, None, None, 'GB/s'),
                },
            },
            'noPeerAccess': {
                'cannon:local-gpu': {
                    'bw': (35, -0.05, None, 'GB/s'),
                },
                'cannon:gpu_test': {
                    'bw': (11, -0.05, None, 'GB/s'),
                },
                '*': {
                    'bw': (79.6, None, None, 'GB/s'),
                },
            },
        }
        self.reference = self.sys_reference[self.peerAccess]


    @run_after('setup')
    def select_makefile(self):
        self.build_system.makefile = 'makefile_p2pBandwidth.cuda'

    @run_before('run')
    def set_num_gpus_per_node(self):
        cp = self.current_partition.fullname
        if cp in {'cannon:local-gpu','fasse:fasse_gpu', 'test:gpu'}:
            self.num_gpus_per_node = 4
            self.num_cpus_per_task = 4
            self.num_tasks = 1
        else:
            self.num_gpus_per_node = 1
            self.num_cpus_per_task = 1
            self.num_tasks = 1

    @sanity_function
    def do_sanity_check(self):
        node_names = set(sn.extractall(
            r'^\s*\[([^,]{1,100})\]\s*Found %s device\(s\).'
            % self.num_gpus_per_node, self.stdout, 1
        ))

        return True
