# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2023 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class RCountDown(rfm.RunOnlyRegressionTest):
    descr = 'Count down from 10 to 1 using R'
    valid_systems = ['cannon:local','cannon:test','fasse:fasse','test:rc-testing']
    valid_prog_environs = ['builtin']
    prerun_cmds = ['wget https://raw.githubusercontent.com/fasrc/User_Codes/master/Languages/R/Example1/count_down.R']
    build_system = 'SingleSource'
    sourcepath = 'count_down.R'
    modules = ['R']
    #executable = 'Rscript count_down.R > count_down.Rout'
    executable = 'R CMD BATCH --no-save --no-restore count_down.R'

    @sanity_function
    def assert_sanity(self):
        return sn.assert_found(r'CountDown\( 10 \)', "count_down.Rout")

