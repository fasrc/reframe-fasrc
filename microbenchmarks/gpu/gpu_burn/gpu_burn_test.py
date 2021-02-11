# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class GpuBurnTest(rfm.RegressionTest):
    def __init__(self):
        self.valid_systems = ['test:gpu']
        self.descr = 'GPU burn test'
        self.valid_prog_environs = ['gpu']
        self.exclusive_access = True
        self.executable_opts = ['-d', '40']
        self.build_system = 'Make'
        self.build_system.makefile = 'makefile.cuda'
        self.executable = './gpu_burn.x'
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.sanity_patterns = self.assert_num_tasks()
        patt = (r'^\s*\[[^\]]*\]\s*GPU\s+\d+\(\S*\):\s+(?P<perf>\S*)\s+GF\/s'
                r'\s+(?P<temp>\S*)\s+Celsius')
        self.perf_patterns = {
            'perf': sn.min(sn.extractall(patt, self.stdout, 'perf', float)),
            'temp': sn.max(sn.extractall(patt, self.stdout, 'temp', float)),
        }

    @property
    @sn.sanity_function
    def num_tasks_assigned(self):
        return self.job.num_tasks * self.num_gpus_per_node

    @sn.sanity_function
    def assert_num_tasks(self):
        return sn.assert_eq(sn.count(sn.findall(
            r'^\s*\[[^\]]*\]\s*GPU\s*\d+\(OK\)', self.stdout)
        ), self.num_tasks_assigned)

    @rfm.run_before('run')
    def set_gpus_per_node(self):
        self.num_gpus_per_node = 4

    @rfm.run_before('performance')
    def report_nid_with_smallest_flops(self):
        regex = r'\[(\S+)\] GPU\s+\d\(OK\): (\d+) GF/s'
        rptf = os.path.join(self.stagedir, sn.evaluate(self.stdout))
        self.nids = sn.extractall(regex, rptf, 1)
        self.flops = sn.extractall(regex, rptf, 2, float)

        # Find index of smallest flops and update reference dictionary to
        # include our patched units
        index = self.flops.evaluate().index(min(self.flops))
        unit = f'GF/s ({self.nids[index]})'
        for key, ref in self.reference.items():
            if not key.endswith(':temp'):
                self.reference[key] = (*ref[:3], unit)
