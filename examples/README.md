# Examples/Tutorial

**NOTE:** Make sure you installed `reframe` as explained
[here](https://github.com/reframe-hpc/reframe#installation). If you prefer to
use a newer version of python instead of the system python, you can do `module
load python` prior to running `./boostrap.sh`

Here, you can find simple examples to get started on running reframe on the
FASRC clusters.

We suggest that you create a reframe working directory with:

1. [reframe original repo](https://github.com/reframe-hpc/refram) directory
2. [reframe-fasrc repo](https://github.com/fasrc/reframe-fasrc) directory
3. and a `runs` directory

We recommend having a separate `runs` directory because `reframe` creates a bunch
of directories and it can mess up git version control.  For example:

```bash
[paulasan@holylogin04 reframe_dir]$ pwd
/n/home_rc/paulasan/projects/reframe_dir
[paulasan@holylogin04 reframe_dir]$ tree -L 2
.
├── reframe
│   ├── bin
│   ├── bootstrap.sh
│   ├── ci-scripts
│   ├── config
│   ├── CONTRIBUTING.md
│   ├── docs
│   ├── external
│   ├── hpctestlib
│   ├── Jenkinsfile
│   ├── LICENSE
│   ├── MANIFEST.in
│   ├── output
│   ├── pyproject.toml
│   ├── README.md
│   ├── README_minimal.md
│   ├── reframe
│   ├── requirements.txt
│   ├── setup.cfg
│   ├── share
│   ├── stage
│   ├── test_reframe.py
│   ├── tools
│   ├── tutorials
│   └── unittests
├── reframe-fasrc
│   ├── checks
│   ├── config
│   ├── examples
│   ├── LICENSE
│   └── README.md
└── runs
    ├── output
    ├── perflogs
    ├── reports
    └── stage
```

Note: some of the subdirectories in `runs` are only created after you run
reframe with specific flags (e.g., `perflogs` will only be created after running
reframe with the flag `--performance-report`).

## Systems

At FASRC, we have  three different systems:

1. `cannon`, production Cannon
2. `fasse`, production FASSE
3. `rc-testing`, test cluster

You can see each configuration on [config](../config/).

In this doc's examples, we use the test cluster, which is typically accessible
from `builds01` node.

To run only on Cannon, use a Cannon login or compute node. Run the reframe
command with the flag `--system="cannon:test"` for CPU codes and
`--system="cannon:gpu_test"` for GPU codes

To run only on FASSE, use a FASSE login node or a Remote Desktop
session. Remember to repeat the steps above on FASSE to ensure a fresh
creation of the reframe working directory and a new installation of
the ReFrame repo therein, as Cannon's filesystem is not visible from
FASSE. Run the reframe command with the flag `--system="fasse"` for
CPU codes and `--system="fasse_gpu"` for GPU codes

## Hello world example

This is example `hello1.py` adapted from [reframe
docs](https://reframe-hpc.readthedocs.io/en/stable/tutorial_basics.html#the-hello-world-test). 

Note that specifying the system on the `hello1.py` file is not suffient. You
have to add the flag `--sytem`, otherwise it will not work.

```bash
[paulasan@holylogin04 reframe-fasrc]$ pwd
/n/home_rc/paulasan/projects/reframe_dir/reframe-fasrc
[paulasan@holylogin04 reframe-fasrc]$ cat examples/hello/hello1.py
# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class HelloTest(rfm.RegressionTest):
    valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
    valid_prog_environs = ['*']
    sourcepath = 'hello.c'

    @sanity_function
    def assert_hello(self):
        return sn.assert_found(r'Hello, World\!', self.stdout)
```

In the `runs` directory, you can run a single test `hello1.py` with
the following command. One can also declare a `$WORKDIR` variable to
store the location of the top-level `reframe` directory, which is
`reframe_dir` in this case. For example,
WORKDIR="~/projects/reframe_dir" and then execute the following
command using `$WORKDIR`, e.g.: `$WORKDIR/reframe/bin/reframe
--config-file...` and so on. Additionally, remember to execute `module
load python` prior to executing the command below to avoid getting
python version related errors, specifically, `SyntaxError: future
feature annotations is not defined`. 

```bash
[paulasan@builds01 runs]$ ~/projects/reframe_dir/reframe/bin/reframe --config-file ~/projects/reframe_dir/reframe-fasrc/config/test.py     --checkpath ~/projects/reframe_dir/reframe-fasrc/examples/hello/hello1.py --run --system="test:rc-testing"
WARNING: redefinition of environment '*:builtin': already defined in '<builtin>'
[ReFrame Setup]
  version:           4.4.0-dev.4+29047c42
  command:           '/n/home_rc/paulasan/projects/reframe_dir/reframe/bin/reframe --config-file /n/home_rc/paulasan/projects/reframe_dir/reframe-fasrc/config/test.py --checkpath /n/home_rc/paulasan/projects/reframe_dir/reframe-fasrc/examples/hello/hello1.py --run --system=test:rc-testing'
  launched by:       paulasan@builds01.rc.fas.harvard.edu
  working directory: '/n/home_rc/paulasan/projects/reframe_dir/runs'
  settings files:    '<builtin>', '/n/home_rc/paulasan/projects/reframe_dir/reframe-fasrc/config/test.py'
  check search path: '/n/home_rc/paulasan/projects/reframe_dir/reframe-fasrc/examples/hello/hello1.py'
  stage directory:   '/n/home_rc/paulasan/projects/reframe_dir/runs/stage'
  output directory:  '/n/home_rc/paulasan/projects/reframe_dir/runs/output'
  log files:         '/tmp/rfm-a4r9a0fj.log'

[==========] Running 1 check(s)
[==========] Started on Wed Nov 22 11:29:23 2023

[----------] start processing checks
[ RUN      ] HelloTest /2b3e4546 @test:rc-testing+builtin
[ RUN      ] HelloTest /2b3e4546 @test:rc-testing+gnu
[ RUN      ] HelloTest /2b3e4546 @test:rc-testing+intel
[ RUN      ] HelloTest /2b3e4546 @test:rc-testing+gnu-mpi
[ RUN      ] HelloTest /2b3e4546 @test:rc-testing+intel-mpi
[       OK ] (1/5) HelloTest /2b3e4546 @test:rc-testing+builtin
[       OK ] (2/5) HelloTest /2b3e4546 @test:rc-testing+gnu
[       OK ] (3/5) HelloTest /2b3e4546 @test:rc-testing+intel
[       OK ] (4/5) HelloTest /2b3e4546 @test:rc-testing+gnu-mpi
[       OK ] (5/5) HelloTest /2b3e4546 @test:rc-testing+intel-mpi
[----------] all spawned checks have finished

[  PASSED  ] Ran 5/5 test case(s) from 1 check(s) (0 failure(s), 0 skipped, 0 aborted)
[==========] Finished on Wed Nov 22 11:29:32 2023
Log file(s) saved in '/tmp/rfm-a4r9a0fj.log'
```

## Running multiple tests

To run multiple examples within a directory, you can use the flag `--recursive`
(or `-R`):

This is example `hello2.py` adapted from [reframe
docs](https://reframe-hpc.readthedocs.io/en/stable/tutorial_basics.html#more-of-hello-world). 


```bash
[paulasan@holylogin04 reframe-fasrc]$ cat examples/hello/hello2.py
# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class HelloMultiLangTest(rfm.RegressionTest):
    lang = parameter(['c', 'cpp', 'f90'])

    valid_systems = ['cannon:test','fasse:fasse','test:rc-testing']
    valid_prog_environs = ['*']

    @run_before('compile')
    def set_sourcepath(self):
        self.sourcepath = f'hello.{self.lang}'

    @sanity_function
    def assert_hello(self):
        return sn.assert_found(r'Hello, World\!', self.stdout)
```

Run both `examples/hello/hello1.py` and `examples/hello/hello2.py`:

```bash
[paulasan@builds01 runs]$ ~/projects/reframe_dir/reframe/bin/reframe --recursive --config-file ~/projects/reframe_dir/reframe-fasrc/config/test.py     --checkpath ~/projects/reframe_dir/reframe-fasrc/examples/hello --run --system="test:rc-testing"
WARNING: redefinition of environment '*:builtin': already defined in '<builtin>'
[ReFrame Setup]
  version:           4.4.0-dev.4+29047c42
  command:           '/n/home_rc/paulasan/projects/reframe_dir/reframe/bin/reframe --recursive --config-file /n/home_rc/paulasan/projects/reframe_dir/reframe-fasrc/config/test.py --checkpath /n/home_rc/paulasan/projects/reframe_dir/reframe-fasrc/examples/hello --run --system=test:rc-testing'
  launched by:       paulasan@builds01.rc.fas.harvard.edu
  working directory: '/n/home_rc/paulasan/projects/reframe_dir/runs'
  settings files:    '<builtin>', '/n/home_rc/paulasan/projects/reframe_dir/reframe-fasrc/config/test.py'
  check search path: (R) '/n/home_rc/paulasan/projects/reframe_dir/reframe-fasrc/examples/hello'
  stage directory:   '/n/home_rc/paulasan/projects/reframe_dir/runs/stage'
  output directory:  '/n/home_rc/paulasan/projects/reframe_dir/runs/output'
  log files:         '/tmp/rfm-4fd3fhav.log'

[==========] Running 4 check(s)
[==========] Started on Wed Nov 22 11:50:29 2023

[----------] start processing checks
[ RUN      ] HelloMultiLangTest %lang=f90 /a000fc24 @test:rc-testing+builtin
[ RUN      ] HelloMultiLangTest %lang=f90 /a000fc24 @test:rc-testing+gnu
[ RUN      ] HelloMultiLangTest %lang=f90 /a000fc24 @test:rc-testing+intel
[ RUN      ] HelloMultiLangTest %lang=f90 /a000fc24 @test:rc-testing+gnu-mpi
[ RUN      ] HelloMultiLangTest %lang=f90 /a000fc24 @test:rc-testing+intel-mpi
[ RUN      ] HelloMultiLangTest %lang=cpp /b059a3fc @test:rc-testing+builtin
[ RUN      ] HelloMultiLangTest %lang=cpp /b059a3fc @test:rc-testing+gnu
[ RUN      ] HelloMultiLangTest %lang=cpp /b059a3fc @test:rc-testing+intel
[ RUN      ] HelloMultiLangTest %lang=cpp /b059a3fc @test:rc-testing+gnu-mpi
[ RUN      ] HelloMultiLangTest %lang=cpp /b059a3fc @test:rc-testing+intel-mpi
[ RUN      ] HelloMultiLangTest %lang=c /ed3216b7 @test:rc-testing+builtin
[ RUN      ] HelloMultiLangTest %lang=c /ed3216b7 @test:rc-testing+gnu
[ RUN      ] HelloMultiLangTest %lang=c /ed3216b7 @test:rc-testing+intel
[ RUN      ] HelloMultiLangTest %lang=c /ed3216b7 @test:rc-testing+gnu-mpi
[ RUN      ] HelloMultiLangTest %lang=c /ed3216b7 @test:rc-testing+intel-mpi
[ RUN      ] HelloTest /2b3e4546 @test:rc-testing+builtin
[ RUN      ] HelloTest /2b3e4546 @test:rc-testing+gnu
[ RUN      ] HelloTest /2b3e4546 @test:rc-testing+intel
[ RUN      ] HelloTest /2b3e4546 @test:rc-testing+gnu-mpi
[ RUN      ] HelloTest /2b3e4546 @test:rc-testing+intel-mpi
[       OK ] ( 1/20) HelloMultiLangTest %lang=f90 /a000fc24 @test:rc-testing+builtin
[       OK ] ( 2/20) HelloMultiLangTest %lang=f90 /a000fc24 @test:rc-testing+gnu
[       OK ] ( 3/20) HelloMultiLangTest %lang=f90 /a000fc24 @test:rc-testing+intel
[       OK ] ( 4/20) HelloMultiLangTest %lang=f90 /a000fc24 @test:rc-testing+gnu-mpi
[       OK ] ( 5/20) HelloMultiLangTest %lang=f90 /a000fc24 @test:rc-testing+intel-mpi
[       OK ] ( 6/20) HelloMultiLangTest %lang=cpp /b059a3fc @test:rc-testing+builtin
[       OK ] ( 7/20) HelloMultiLangTest %lang=cpp /b059a3fc @test:rc-testing+gnu
[       OK ] ( 8/20) HelloMultiLangTest %lang=cpp /b059a3fc @test:rc-testing+intel
[       OK ] ( 9/20) HelloMultiLangTest %lang=cpp /b059a3fc @test:rc-testing+gnu-mpi
[       OK ] (10/20) HelloMultiLangTest %lang=cpp /b059a3fc @test:rc-testing+intel-mpi
[       OK ] (11/20) HelloMultiLangTest %lang=c /ed3216b7 @test:rc-testing+builtin
[       OK ] (12/20) HelloMultiLangTest %lang=c /ed3216b7 @test:rc-testing+gnu
[       OK ] (13/20) HelloMultiLangTest %lang=c /ed3216b7 @test:rc-testing+intel
[       OK ] (14/20) HelloMultiLangTest %lang=c /ed3216b7 @test:rc-testing+gnu-mpi
[       OK ] (15/20) HelloMultiLangTest %lang=c /ed3216b7 @test:rc-testing+intel-mpi
[       OK ] (16/20) HelloTest /2b3e4546 @test:rc-testing+builtin
[       OK ] (17/20) HelloTest /2b3e4546 @test:rc-testing+gnu
[       OK ] (18/20) HelloTest /2b3e4546 @test:rc-testing+intel
[       OK ] (19/20) HelloTest /2b3e4546 @test:rc-testing+gnu-mpi
[       OK ] (20/20) HelloTest /2b3e4546 @test:rc-testing+intel-mpi
[----------] all spawned checks have finished

[  PASSED  ] Ran 20/20 test case(s) from 4 check(s) (0 failure(s), 0 skipped, 0 aborted)
[==========] Finished on Wed Nov 22 11:50:56 2023
Log file(s) saved in '/tmp/rfm-4fd3fhav.log'
```

## Choosing specific compilers

If you would like to test only one compiler, you can change in `examples/hello/hello1.py` the
`valid_prog_environs = ['*']` to a specific compiler. For example,

```bash
valid_prog_environs = ['gnu']
```

All the compilers available for the test cluster, Cannon, and FASSE are specified in their respective files in the [config folder](../config/).

## Monitoring jobs

You can monitor Reframe jobs in the same way that you monitor slurm jobs (note
that for the test cluster, you need to be on `builds01`). For example:

```bash
[paulasan@builds01 runs]$ sacct
JobID           JobName  Partition    Account  AllocCPUS      State ExitCode
------------ ---------- ---------- ---------- ---------- ---------- --------
3580         rfm_Hello+ rc-testing   rc_admin          1  COMPLETED      0:0
3580.batch        batch              rc_admin          1  COMPLETED      0:0
3580.extern      extern              rc_admin          1  COMPLETED      0:0
3580.0        HelloTest              rc_admin          1  COMPLETED      0:0
3581         rfm_Hello+ rc-testing   rc_admin          1  COMPLETED      0:0
3581.batch        batch              rc_admin          1  COMPLETED      0:0
3581.extern      extern              rc_admin          1  COMPLETED      0:0
3581.0        HelloTest              rc_admin          1  COMPLETED      0:0
```

## Troubleshooting

If you have a failed test, look at the reframe output. It will tell you the
`stage` and `output` directories, where you can look for `*.out` and `*.err`
files.

