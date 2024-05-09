# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class AlltoallTest(rfm.RegressionTest):
    variant = parameter(['production'])
    strict_check = False
    valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
    descr = 'Alltoall OSU microbenchmark'
    build_system = 'Make'
    executable = './osu_alltoall'
    # The -m option sets the maximum message size
    # The -x option sets the number of warm-up iterations
    # The -i option sets the number of iterations
    executable_opts = ['-m', '8', '-x', '1000', '-i', '20000']
    valid_prog_environs = ['gnu-mpi','intel-mpi']
    num_tasks_per_node = 1
    num_gpus_per_node  = 1
    num_tasks = 8

    reference = {
        'cannon:test': {
            'latency': (3.3, None, 0.1, 'us')
        },
        'fasse:fasse': {
            'latency': (3.3, None, 0.1, 'us')
        },
        '*': {
            'latency': (20.73, None, None, 'us')
        }
    }

    extra_resources = {
        'switches': {
            'num_switches': 1
        }
    }

    @run_before('compile')
    def set_makefile(self):
        self.build_system.makefile = 'Makefile_alltoall'

    @sanity_function
    def assert_found_8MB_latency(self):
        return sn.assert_found(r'^8', self.stdout)

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']

    @run_before('performance')
    def set_performance_patterns(self):
        self.perf_patterns = {
            'latency': sn.extractsingle(r'^8\s+(?P<latency>\S+)',
                                        self.stdout, 'latency', float)
        }


@rfm.simple_test
class FlexAlltoallTest(rfm.RegressionTest):
    def __init__(self):
        self.valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
        self.valid_prog_environs = ['gnu-mpi', 'intel-mpi']
        self.descr = 'Flexible Alltoall OSU test'
        self.build_system = 'Make'
        self.build_system.makefile = 'Makefile_alltoall'
        self.executable = './osu_alltoall'
        self.sanity_patterns = sn.assert_found(r'^1048576', self.stdout)

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']

    @run_before('run')
    def set_tasks(self):
        if self.current_partition.fullname in ['test:rc-testing']:
            self.num_tasks_per_node = 32
            self.num_tasks = 64
        elif self.current_partition.fullname in ['cannon:test', 'fasse:fasse']:
            self.num_tasks_per_node = 48
            self.num_tasks = 96
        else:
            self.num_tasks_per_node = 32
            self.num_tasks = 64


class AllreduceTest(rfm.RegressionTest):
    variant = parameter(['small'], ['large'])
    strict_check = False
    valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']

    descr = 'Allreduce OSU microbenchmark'
    build_system = 'Make'
    executable = './osu_allreduce'
    # The -x option controls the number of warm-up iterations
    # The -i option controls the number of iterations
    executable_opts = ['-m', '8', '-x', '1000', '-i', '20000']
    valid_prog_environs = ['gnu-mpi','intel-mpi']
    num_tasks_per_node = 1
    num_gpus_per_node  = 0
    extra_resources = {
        'switches': {
            'num_switches': 1
        }
    }

    @run_before('compile')
    def set_makefile(self):
        self.build_system.makefile = 'Makefile_allreduce'

    @run_before('run')
    def set_num_tasks(self):
        self.num_tasks = 6 if self.variant == 'small' else 12

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']

    @sanity_function
    def assert_found_8MB_latency(self):
        return sn.assert_found(r'^8', self.stdout)

    @run_before('performance')
    def set_performance_patterns(self):
        if variant == 'small':
            self.reference = {
                'cannon:test': {
                    'latency': (4.6, None, 0.05, 'us')
                },
                'fasse:fasse': {
                    'latency': (4.6, None, 0.05, 'us')
                },
                '*': {
                    'latency': (9.30, None, None, 'us')
                },
            }
        else:
            self.reference = {
                'cannon:test': {
                    'latency': (5.8, None, 0.05, 'us')
                },
                'fasse:fasse': {
                    'latency': (5.8, None, 0.05, 'us')
                },
                '*': {
                    'latency': (9.30, None, None, 'us')
                },
            }
        self.perf_patterns = {
            'latency': sn.extractsingle(r'^8\s+(?P<latency>\S+)',
                                        self.stdout, 'latency', float)
        }

class P2PBaseTest(rfm.RegressionTest):
    def __init__(self):
        self.strict_check = False
        self.num_tasks = 2
        self.num_tasks_per_node = 1
        self.descr = 'P2P microbenchmark'
        self.build_system = 'Make'
        self.build_system.makefile = 'Makefile_p2p'
        self.valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
        self.valid_prog_environs = ['gnu-mpi', 'intel-mpi']
        self.sanity_patterns = sn.assert_found(r'^4194304', self.stdout)

        self.extra_resources = {
            'switches': {
                'num_switches': 1
            }
        }
    
    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']


@rfm.simple_test
class P2PCPUBandwidthTest(P2PBaseTest):
    def __init__(self):
        super().__init__()
        self.valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
        self.valid_prog_environs = ['gnu-mpi', 'intel-mpi']
        self.executable = './p2p_osu_bw'
        self.executable_opts = ['-x', '100', '-i', '1000']
        self.reference = {
            'cannon:test': {
                'bw': (12000.0, -0.10, None, 'MB/s')
            },
            'fasse:fasse': {
                'bw': (12000.0, -0.10, None, 'MB/s')
            },
            '*': {
                'bw': (9649.0, None, None, 'MB/s')
            },
        }

        self.perf_patterns = {
            'bw': sn.extractsingle(r'^4194304\s+(?P<bw>\S+)',
                                   self.stdout, 'bw', float)
        }

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']


@rfm.simple_test
class P2PCPULatencyTest(P2PBaseTest):
    def __init__(self):
        super().__init__()
        self.valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
        self.valid_prog_environs = ['gnu-mpi', 'intel-mpi']
        self.executable_opts = ['-x', '100', '-i', '1000']

        self.executable = './p2p_osu_latency'
        self.reference = {
            'cannon:test': {
                'latency': (1.7, None, 0.70, 'us')
            },
            'fasse:fasse': {
                'latency': (1.7, None, 0.70, 'us')
            },
            '*': {
                'latency': (1.61, None, None, 'us')
            },
        }
        self.perf_patterns = {
            'latency': sn.extractsingle(r'^8\s+(?P<latency>\S+)',
                                        self.stdout, 'latency', float)
        }

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']
