# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import getpass
import os
import re

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class IorCheck(rfm.RunOnlyRegressionTest):
    base_dir = parameter(['/scratch/','/n/holyscratch01/rc_admin/test'])
    valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
    valid_prog_environs = ['intel-mpi']
    modules = ['ior']
    sourcesdir = None
    executable = 'ior'

    @run_before('compile')
    def set_vars(self):
        self.descr = f'IOR check ({self.base_dir})'
        self.tags = {'ops', self.base_dir}
        self.basedir = self.base_dir
        self.username = getpass.getuser()
        self.test_dir = os.path.join(self.basedir,
                                     self.username,
                                     'ior')
        self.prerun_cmds = ['mkdir -p ' + self.test_dir]
        self.test_file = os.path.join(self.test_dir, 'ior')
        self.fs = {
            '/scratch/': {
                'num_tasks': 4,
                'num_tasks_per_node': 4
            },
            '/n/holyscratch01/rc_admin/test': {
                'num_tasks': 96,
                'num_tasks_per_node': 32,
                'ior_block_size': '32g',
            },
        }

        # Setting some default values
        for data in self.fs.values():
            data.setdefault('ior_block_size', '24g')
            data.setdefault('ior_access_type', 'MPIIO')
            data.setdefault(
                'reference',
                {
                    'read_bw': (0, None, None, 'MiB/s'),
                    'write_bw': (0, None, None, 'MiB/s')
                }
            )
            data.setdefault('dummy', {})  # entry for unknown systems

        cur_sys = self.current_system.name
        if cur_sys not in self.fs[self.base_dir]:
            cur_sys = 'dummy'

        self.num_tasks = self.fs[self.base_dir].get('num_tasks', 1)
        tpn = self.fs[self.base_dir].get('num_tasks_per_node', 1)
        self.num_tasks_per_node = tpn

        self.ior_block_size = self.fs[self.base_dir]['ior_block_size']
        self.ior_access_type = self.fs[self.base_dir]['ior_access_type']
        self.executable_opts = ['-F', '-C', '-Q 1', '-t 1m', '-D 60',
                                '-b', self.ior_block_size,
                                '-a', self.ior_access_type]

        # Default umask is 0022, which generates file permissions -rw-r--r--
        # we want -rw-rw-r-- so we set umask to 0002
        os.umask(2)
        self.time_limit = '10m'
        # Our references are based on fs types but regression needs reference
        # per system.
        self.reference = {
            '*': self.fs[self.base_dir]['reference']
        }

    @run_before('run')
    def set_exec_opts(self):
        self.test_file += '.' + self.current_partition.name
        self.executable_opts += ['-o', self.test_file]

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=3G']

    @run_before('sanity')
    def set_sanity_patterns(self):
        self.sanity_patterns = sn.assert_found(r'^write ', self.stdout)
        self.sanity_patterns = sn.assert_found(r'^read ', self.stdout)

    @run_before('performance')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'write_bw': sn.extractsingle(
                r'^write \s+(?P<write_bw>\S+)', self.stdout,
                'write_bw', float),
            'read_bw': sn.extractsingle(
                r'^read \s+(?P<read_bw>\S+)', self.stdout,
                'read_bw', float)
        }
