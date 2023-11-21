# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2023 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class PyMonteCarloPi(rfm.RunOnlyRegressionTest):
    descr = 'Estimating pi in serial using Python'
    valid_systems = ['cannon:local','cannon:test','fasse:fasse','test:rc-testing']
    valid_prog_environs = ['builtin']
    prerun_cmds = ['wget https://raw.githubusercontent.com/fasrc/User_Codes/master/Languages/Python/Example1/mc_pi.py']
    build_system = 'SingleSource'
    sourcepath = 'mc_pi.py'
    modules = ['python']
    executable = 'python mc_pi.py'

    @sanity_function
    def assert_sanity(self):
        return sn.assert_found(r'3.14', self.stdout)

