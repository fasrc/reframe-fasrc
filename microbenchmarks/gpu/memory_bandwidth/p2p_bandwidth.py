# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe.utility.sanity as sn
import reframe as rfm


@rfm.parameterized_test(['peerAccess'], ['noPeerAccess'])
class P2pBandwidthCheck(rfm.RegressionTest):
    def __init__(self, peerAccess):
        self.valid_systems = ['test:gpu']
        self.valid_prog_environs = ['gpu']

        # Perform a single bandwidth test with a buffer size of 1024MB
        copy_size = 1073741824

        self.build_system = 'Make'
        self.executable = 'p2p_bandwidth.x'
        self.build_system.cxxflags = [f'-DCOPY={copy_size}']
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.exclusive_access = True

        if (peerAccess == 'peerAccess'):
            self.build_system.cxxflags += ['-DP2P']
            p2p = True
        else:
            p2p = False

        self.sanity_patterns = self.do_sanity_check()
        self.perf_patterns = {
            'bw': sn.min(sn.extractall(
                r'^[^,]*\[[^\]]*\]\s+GPU\s+\d+\s+(\s*\d+.\d+\s)+',
                self.stdout, 1, float))
        }

        self.tags = {'diagnostic', 'benchmark', 'mch'}
        self.maintainers = ['JO']

    @rfm.run_after('setup')
    def select_makefile(self):
        self.build_system.makefile = 'makefile_p2pBandwidth.cuda'

    @rfm.run_before('run')
    def set_num_gpus_per_node(self):
        self.num_gpus_per_node = 4

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
            r'^\s*\[([^,]{1,20})\]\s*Test Result\s*=\s*PASS',
            self.stdout, 1
        ))
        sn.evaluate(sn.assert_eq(
            node_names, good_nodes,
            msg='check failed on the following node(s): %s' %
            ','.join(sorted(node_names - good_nodes)))
        )

        return True
