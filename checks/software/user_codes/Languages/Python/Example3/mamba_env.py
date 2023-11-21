# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2023 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class PyMambaEnv(rfm.RunOnlyRegressionTest):
    descr = 'Creates a conda environment, test numpy and pandas, deletes conda environment'
    valid_systems = ['cannon:local','cannon:test','fasse:fasse','test:rc-testing']
    valid_prog_environs = ['builtin']
    prerun_cmds = ['wget https://raw.githubusercontent.com/fasrc/User_Codes/master/Languages/Python/Example3/build_env.sh',
                   'wget https://raw.githubusercontent.com/fasrc/User_Codes/master/Languages/Python/Example3/numpy_pandas_ex.py',
                   'sh build_env.sh',
                   'mamba activate my_env']
    build_system = 'SingleSource'
    sourcepath = 'numpy_pandas_ex.py'
    modules = ['python']
    executable = 'python numpy_pandas_ex.py'
    postrun_cmds= ['mamba deactivate',
                   'mamba env remove -n my_env']

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']

    @sanity_function
    def assert_sanity(self):
        return sn.assert_found(r'0      1       2', self.stdout)

