# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import getpass
import os
import re

import reframe as rfm
import reframe.utility.sanity as sn


class IorCheck(rfm.RegressionTest):
    def __init__(self, base_dir):
        self.descr = f'IOR check ({base_dir})'
        self.tags = {'ops', base_dir}
        self.base_dir = base_dir
        self.username = getpass.getuser()
        self.test_dir = os.path.join(self.base_dir,
                                     self.username,
                                     '.ior')
        self.prerun_cmds = ['mkdir -p ' + self.test_dir]
        self.test_file = os.path.join(self.test_dir, 'ior')
        self.valid_systems = ['test:rc-testing']
        self.fs = {
            '/scratch/': {
                'num_tasks': 4
            },
            '/n/holyscratch01/rc_admin/test': {
                'num_tasks': 10
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
        if cur_sys not in self.fs[base_dir]:
            cur_sys = 'dummy'

        self.num_tasks = self.fs[base_dir].get('num_tasks', 1)
        tpn = self.fs[base_dir].get('num_tasks_per_node', 1)
        self.num_tasks_per_node = tpn

        self.ior_block_size = self.fs[base_dir]['ior_block_size']
        self.ior_access_type = self.fs[base_dir]['ior_access_type']
        self.executable_opts = ['-B', '-F', '-C ', '-Q 1', '-t 4m', '-D 30',
                                '-b', self.ior_block_size,
                                '-a', self.ior_access_type]
        self.valid_prog_environs = ['intel-mpi']
        self.modules = ['ior']

        # Default umask is 0022, which generates file permissions -rw-r--r--
        # we want -rw-rw-r-- so we set umask to 0002
        os.umask(2)
        self.time_limit = '5m'
        # Our references are based on fs types but regression needs reference
        # per system.
        self.reference = {
            '*': self.fs[base_dir]['reference']
        }

    @rfm.run_before('run')
    def set_exec_opts(self):
        self.test_file += '.' + self.current_partition.name
        self.executable_opts += ['-o', self.test_file]


@rfm.parameterized_test(['/scratch/'],
                        ['/n/holyscratch01/rc_admin/test'])
class IorWriteCheck(IorCheck):
    def __init__(self, base_dir):
        super().__init__(base_dir)
        self.executable_opts += ['-w', '-k']
        self.sanity_patterns = sn.assert_found(r'^Max Write: ', self.stdout)
        self.perf_patterns = {
            'write_bw': sn.extractsingle(
                r'^Max Write:\s+(?P<write_bw>\S+) MiB/sec', self.stdout,
                'write_bw', float)
        }
        self.tags |= {'write'}


@rfm.parameterized_test(['/scratch/'],
                        ['/n/holyscratch01/rc_admin/test'])
class IorReadCheck(IorCheck):
    def __init__(self, base_dir):
        super().__init__(base_dir)
        self.executable_opts += ['-r']
        self.sanity_patterns = sn.assert_found(r'^Max Read: ', self.stdout)
        self.perf_patterns = {
            'read_bw': sn.extractsingle(
                r'^Max Read:\s+(?P<read_bw>\S+) MiB/sec', self.stdout,
                'read_bw', float)
        }
        self.depends_on(re.sub(r'IorReadCheck', 'IorWriteCheck', self.name))
        self.tags |= {'read'}
