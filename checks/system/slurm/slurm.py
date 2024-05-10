# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.osext as osext
import reframe.utility.sanity as sn


class SlurmSimpleBaseCheck(rfm.RunOnlyRegressionTest):
    '''Base class for Slurm simple binary tests'''

    def __init__(self):
        self.valid_systems = ['cannon:test','cannon:gpu_test','fasse:fasse','fasse:fasse_gpu','test:rc-testing','test:gpu']
        self.valid_prog_environs = ['builtin']
        self.num_tasks_per_node = 1

class SlurmCompiledBaseCheck(rfm.RegressionTest):
    '''Base class for Slurm tests that require compiling some code'''

    def __init__(self):
        self.valid_systems = ['cannon:test','cannon:gpu_test','fasse:fasse','fasse:fasse_gpu','test:rc-testing','test:gpu']
        self.valid_prog_environs = ['builtin']
        self.num_tasks_per_node = 1

@rfm.simple_test
class HostnameCheck(SlurmSimpleBaseCheck):
    def __init__(self):
        super().__init__()
        self.executable = '/bin/hostname -s'
        self.valid_systems = ['cannon:test','cannon:gpu_test','fasse:fasse','fasse:fasse_gpu','test:rc-testing','test:gpu']
        self.valid_prog_environs = ['builtin']
        self.hostname_patt = {
            'cannon:test': r'^holy8c\d{5}$',
            'cannon:gpu_test': r'^holygpu7c\d{5}$',
            'test:rc-testing': r'^holy7c\d{5}$',
            'test:gpu': r'^holygpu7c\d{2}$',
            'fasse:fasse': r'^holy7c\d{5}$',
            'fasse:fasse_gpu': r'^holygpu7c\d{2}$',
        }

    @run_before('sanity')
    def set_sanity_patterns(self):
        partname = self.current_partition.fullname
        num_matches = sn.count(
            sn.findall(self.hostname_patt[partname], self.stdout)
        )
        self.sanity_patterns = sn.assert_eq(self.num_tasks, num_matches)


@rfm.simple_test
class EnvironmentVariableCheck(SlurmSimpleBaseCheck):
    def __init__(self):
        super().__init__()
        self.num_tasks = 2
        self.valid_systems = ['cannon:test','cannon:gpu_test','fasse:fasse','fasse:fasse_gpu','test:rc-testing','test:gpu']
        self.executable = '/bin/echo'
        self.executable_opts = ['$MY_VAR']
        self.env_vars = {'MY_VAR': 'TEST123456!'}
        num_matches = sn.count(sn.findall(r'TEST123456!', self.stdout))
        self.sanity_patterns = sn.assert_eq(self.num_tasks, num_matches)


@rfm.simple_test
class DefaultRequestGPU(SlurmSimpleBaseCheck):
    def __init__(self):
        super().__init__()
        self.valid_systems = ['cannon:gpu_test','fasse:fasse_gpu','test:gpu']
        self.valid_prog_environs = ['gpu']
        self.num_gpus_per_node = 1
        self.executable = 'nvidia-smi'
        self.sanity_patterns = sn.assert_found(
            r'NVIDIA-SMI.*Driver Version.*', self.stdout)


@rfm.simple_test
class DefaultRequestGPUSetsGRES(SlurmSimpleBaseCheck):
    def __init__(self):
        super().__init__()
        self.valid_prog_environs = ['gpu']
        self.valid_systems = ['cannon:gpu_test','fasse:fasse_gpu','test:gpu']
        self.num_gpus_per_node = 1
        self.executable = 'scontrol show job ${SLURM_JOB_ID}'
        self.sanity_patterns = sn.assert_found(
            r'.*(TresPerNode|Gres)=.*gpu:1.*', self.stdout)


@rfm.simple_test
class MemoryOverconsumptionCheck(SlurmCompiledBaseCheck):
    def __init__(self):
        super().__init__()
        self.time_limit = '1m'
        self.valid_systems += ['cannon:test','cannon:gpu_test','fasse:fasse','fasse:fasse_gpu','test:rc-testing','test:gpu']
        self.sourcepath = 'eatmemory.c'
        self.tags.add('mem')
        self.executable_opts = ['4000M']
        self.sanity_patterns = sn.assert_found(
            r'(exceeded memory limit)|(Out Of Memory)', self.stderr
        )

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem=2000']
