# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2023 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class MatlabParallelMonteCarloPi(rfm.RunOnlyRegressionTest):
    descr = 'Uses Matlab to compute Pi in parallel using Monte Carlo method'
    valid_systems = ['cannon:local','cannon:test','fasse:fasse','test:rc-testing']
    valid_prog_environs = ['builtin']
    prerun_cmds = ['wget https://raw.githubusercontent.com/fasrc/User_Codes/master/Parallel_Computing/MATLAB/Example1/parallel_monte_carlo.m']
    build_system = 'SingleSource'
    sourcepath = 'parallel_monte_carlo.m'
    modules = ['matlab']
    executable = 'matlab -nosplash -nodesktop -r parallel_monte_carlo'

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=2G']

    @run_before('run')
    def set_num_threads(self):
        self.num_cpus_per_task = 8

    @sanity_function
    def assert_sanity(self):
        return sn.assert_found(r'Starting parallel pool', self.stdout)

