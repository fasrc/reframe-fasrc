# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

# ReFrame FASSE cluster settings
#

import reframe.utility.osext as osext


site_configuration = {
    'systems': [
        {
            'name': 'fasse',
            'descr': 'FASSE',
            'hostnames': [
                'holy7c',
                'aagk80gpu',
                'fasselogin'
            ],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'login',
                    'scheduler': 'local',
                    'environs': [
                        'builtin',
                        'gnu',
                        'intel',
                    ],
                    'descr': 'Login nodes',
                    'max_jobs': 1,
                    'launcher': 'local'
                },
                {
                    'name': 'fasse',
                    'scheduler': 'slurm',
                    'environs': [
                         'builtin',
                         'gnu',
                         'intel',
                         'gnu-mpi',
                         'intel-mpi'
                    ],
                    'descr': 'FASSE CPU',
                    'max_jobs': 100,
                    'launcher': 'srun',
                    'access': ['-p fasse']
                },
                {
                    'name': 'fasse_gpu',
                    'scheduler': 'slurm',
                    'environs': [
                         'gpu'
                    ],
                    'descr': 'FASSE GPU',
                    'max_jobs': 100,
                    'launcher': 'srun',
                    'access': ['-p fasse_gpu'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gres=gpu:{num_gpus_per_node}']
                        }
                    ],

                }
            ]
        }
    ],
    'environments': [
        {
            'name': 'gnu',
            'modules': ['gcc/10.2.0-fasrc01'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'intel',
            'modules': ['intel/21.2.0-fasrc01'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort'
        },
        {
            'name': 'builtin',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'gnu-mpi',
            'modules': ['gcc/10.2.0-fasrc01','openmpi/4.1.0-fasrc01'],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'intel-mpi',
            'modules': ['intel/21.2.0-fasrc01','openmpi/4.1.0-fasrc01'],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'gpu',
            'modules': ['gcc','cuda'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        }
    ],
    'logging': [
        {
            'handlers': [
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s'
                },
                {
                    'type': 'file',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_info)s: %(message)s',   # noqa: E501
                    'append': False
                }
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': (
                        '%(check_job_completion_time)s|reframe %(version)s|'
                        '%(check_info)s|jobid=%(check_jobid)s|'
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        'ref=%(check_perf_ref)s '
                        '(l=%(check_perf_lower_thres)s, '
                        'u=%(check_perf_upper_thres)s)|'
                        '%(check_perf_unit)s'
                    ),
                    'append': True
                }
            ]
        }
    ],
}
