# ReFrame test cluster settings
#

import reframe.utility.osext as osext


site_configuration = {
    'systems': [
        {
            'name': 'test',
            'descr': 'Test Cluster',
            'hostnames': [
                'holyitc',
                'aagk80gpu'
            ],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'login',
                    'scheduler': 'local',
                    'environs': [
                        'builtin',
                        'gcc',
                        'intel'
                    ],
                    'descr': 'Login nodes',
                    'max_jobs': 4,
                    'launcher': 'local'
                },
                {
                    'name': 'rc-testing'
                    'scheduler': 'slurm',
                    'environs': [
                         'builtin',
                         'gcc',
                         'intel'
                    ],
                    'descr': 'Test Cluster CPU'
                    'max_jobs': 100,
                    'launcher': 'srun
                }
            ]
        }
    ],
    'environments': [
        {
            'name': 'gnu',
            'modules': ['gcc/9.2.0-fasrc01'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
            'name': 'intel'
            'modules': ['intel/19.0.5-fasrc01'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort'
        {
            'name': 'builtin',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
    ],
}
