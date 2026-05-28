# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

# ReFrame Cannon cluster settings
#

import reframe.utility.osext as osext
from reframe.core.backends import register_launcher
from reframe.core.launchers import JobLauncher


@register_launcher('srun-harvard')
class MySmartLauncher(JobLauncher):
    def command(self, job):
        return ['srun -c ${SLURM_CPUS_PER_TASK:-1} -n ${SLURM_NTASKS:-1} --mpi=pmix']

@register_launcher('srun-harvard-pmi2')
class MySmartLauncher(JobLauncher):
    def command(self, job):
        return ['srun -c ${SLURM_CPUS_PER_TASK:-1} -n ${SLURM_NTASKS:-1} --mpi=pmi2']

site_configuration = {
    'systems': [
        {
            'name': 'cannon',
            'descr': 'Cannon Cluster',
            'hostnames': [
                'holy7c',
                'holygpu'
            ],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'local',
                    'scheduler': 'local',
                    'environs': [
                        'builtin',
                        'gnu',
                        'intel',
                        'gnu-mpi',
                        'intel-mpi',
                        'intel-intelmpi'
                    ],
                    'descr': 'Run on local node',
                    'max_jobs': 1,
                    'launcher': 'local'
                },
                {
                    'name': 'local-gpu',
                    'scheduler': 'local',
                    'environs': [
                        'gpu',
                    ],
                    'descr': 'Run on local GPU node',
                    'max_jobs': 1,
                    'launcher': 'local'
                },
                {
                    'name': 'test',
                    'scheduler': 'slurm',
                    'environs': [
                         'builtin',
                         'gnu',
                         'intel',
                         'gnu-mpi',
                         'intel-mpi',
                         'intel-intelmpi'
                    ],
                    'descr': 'Cannon test partition',
                    'max_jobs': 5,
                    'launcher': 'srun-harvard',
                    'access': ['-p test']
                },
                {
                    'name': 'gpu_test',
                    'scheduler': 'slurm',
                    'environs': [
                         'gpu'
                    ],
                    'descr': 'Cannon gpu_test partition',
                    'max_jobs': 5,
                    'launcher': 'srun-harvard',
                    'access': ['-p gpu_test'],
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
            'modules': ['gcc'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'intel',
            'modules': ['intel'],
            'cc': 'icx',
            'cxx': 'icpx',
            'ftn': 'ifx'
        },
        {
            'name': 'builtin',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'gnu-mpi',
            'modules': ['gcc','openmpi'],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'intel-mpi',
            'modules': ['intel','openmpi'],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort'
        },
        {
            'name': 'intel-intelmpi',
            'modules': ['intel','intelmpi'],
            'cc': 'mpiicx',
            'cxx': 'mpiicpx',
            'ftn': 'mpiifx'
        },
        {
            'name': 'gpu',
            'modules': ['gcc/12.2.0-fasrc01','cuda'],
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
