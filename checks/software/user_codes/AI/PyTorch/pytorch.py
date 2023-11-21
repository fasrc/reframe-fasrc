# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2023 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os

import reframe as rfm
import reframe.utility.sanity as sn
import reframe.utility.udeps as udeps


@rfm.simple_test
class PyTorch(rfm.RunOnlyRegressionTest):
    descr = 'Runs a PyTorch example using a singularity container'
    valid_systems = ['cannon:local-gpu','cannon:gpu_test','fasse:fasse_gpu','test:gpu']
    valid_prog_environs = ['gpu']
    prerun_cmds = ['module purge',
                   'wget https://raw.githubusercontent.com/fasrc/User_Codes/master/AI/PyTorch/check_gpu.py']
    build_system = 'SingleSource'
    sourcepath = 'check_gpu.py'
    executable = 'singularity exec --nv pytorch_latest.sif python check_gpu.py'

    @run_after('init')
    def inject_dependencies(self):
        self.depends_on('PyTorchSingularity', udeps.fully)

    @require_deps
    def set_sourcedir(self, PyTorchSingularity):
        self.sourcesdir = os.path.join(PyTorchSingularity(environ='gpu').stagedir)

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem=8G']

    @run_before('run')
    def set_job_options(self):
        self.job.options += ['--gres=gpu:1']

    @sanity_function
    def assert_sanity(self):
        return sn.assert_found(r'Using device: cuda', self.stdout)

@rfm.simple_test
class PyTorchSingularity(rfm.RunOnlyRegressionTest):
    descr = 'Pulls (downloads) singularity container with PyTorch'
    valid_systems = ['cannon:local-gpu','cannon:gpu_test','fasse:fasse_gpu','test:gpu']
    valid_prog_environs = ['gpu']
    build_system = 'SingleSource'
    executable = 'singularity pull --disable-cache docker://pytorch/pytorch:latest'

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem=8G']

    @run_before('run')
    def set_num_threads(self):
        self.num_cpus_per_task = 16

    @run_before('run')
    def set_job_options(self):
        self.job.options += ['--gres=gpu:1']

    @sanity_function
    def assert_sanity(self):
        return sn.assert_true(os.path.exists('pytorch_latest.sif'))

