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
class Tensorflow(rfm.RunOnlyRegressionTest):
    descr = 'Runs a multi-gpu tensorflow example using a singularity container'
    valid_systems = ['cannon:local-gpu','cannon:gpu_test','fasse:fasse_gpu','test:gpu']
    valid_prog_environs = ['gpu']
    prerun_cmds = ['module purge',
                   'wget https://raw.githubusercontent.com/fasrc/User_Codes/master/AI/TensorFlow/Example4/tf_test_multi_gpu.py']
    build_system = 'SingleSource'
    sourcepath = 'tf_test_multi_gpu.py'
    executable = 'singularity exec --nv tensorflow_latest-gpu.sif python tf_test_multi_gpu.py'

    @run_after('init')
    def inject_dependencies(self):
        self.depends_on('TensorflowSingularity', udeps.fully)

    @require_deps
    def set_sourcedir(self, TensorflowSingularity):
        self.sourcesdir = os.path.join(TensorflowSingularity(environ='gpu').stagedir)

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem=8G']

    @run_before('run')
    def set_job_options(self):
        self.job.options += ['--gres=gpu:4']

    @sanity_function
    def assert_sanity(self):
        return sn.assert_found(r'Test accuracy', self.stdout)

@rfm.simple_test
class TensorflowSingularity(rfm.RunOnlyRegressionTest):
    descr = 'Pulls (downloads) singularity container with tensorflow'
    valid_systems = ['cannon:local-gpu','cannon:gpu_test','fasse:fasse_gpu','test:gpu']
    valid_prog_environs = ['gpu']
    build_system = 'SingleSource'
    executable = 'singularity pull --disable-cache docker://tensorflow/tensorflow:latest-gpu'

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
        return sn.assert_true(os.path.exists('tensorflow_latest-gpu.sif'))

