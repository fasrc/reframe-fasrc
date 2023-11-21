# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2023 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class CppDotProduct(rfm.RegressionTest):
    valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
    valid_prog_environs = ['builtin','gnu','intel']
    prebuild_cmds = [
        'wget https://raw.githubusercontent.com/fasrc/User_Codes/master/Languages/Cpp/dot_prod.cpp'  # noqa: E501
    ]
    build_system = 'SingleSource'
    sourcepath = 'dot_prod.cpp'

    @run_before('compile')
    def set_compiler_flags(self):
        self.build_system.cflags = ['-O3', '-Wall']

    @run_before('run')
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=2G']

    @sanity_function
    def assert_hello(self):
        return sn.assert_found(r' Scallar product of x1 and x2', self.stdout)

