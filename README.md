# reframe-fasrc
FASRC specific configuration for Reframe

## Configs
These are configs for different clusters run by FASRC.

* cannon: Configs for cannon.
* fasse: Configs for fasse.
* test: Configs for the test cluster.

## Checks
Checks currently are copied from the cscs-checks folder in reframe and tuned to the FASRC environment.

### Microbenchmarks
These are benchmark tests that are broken down by category.  Here is a short description of each test:

#### cpu
* alloc_speed: Tests speed of memory allocation. Originally from CSCS
* dgemm: Runs dgemm code to get a measure of FLOps. Originally from CSCS
* latency: Measures latency to L1, L2, L3 cache. Originally from CSCS
* stream: Runs STREAM test for measuring memory bandwidth. Originally from CSCS
* strided_bandwidth: Runs bandwidth test with various stride sizes. Originally from CSCS

#### gpu
* dgemm: Runs dgemm code to get a measure of FLOps. Originally from CSCS
* gpu_burn: Burns in GPU and gives a report of GFLOps for one GPU and its temperature. Originally from CSCS
* kernel_latency: Tests latency in loading the NVIDIA kernel. Originally from CSCS
* memory_bandwidth: Tests GPU memory bandwidth. Originally from CSCS
* pointer_chase: Runs a linked list search to test memory latencies. Originally from CSCS
* shmem: Tests shared memory bandwidth. Originally from CSCS

#### mpi
* fft: Test runs FFTW. Originally from CSCS
* halo_exchange: Simulates halo cell (aka ghost or boundary zone) exchange to test MPI communications. Originally from CSCS
* hpcg_benchmark: Runs the HPCG benchmark for gnu and MKL. Originally from CSCS
* osu: Various MPI benchmarks from OSU. Originally from CSCS

### Software
These are codes from [FASRC User_codes](https://github.com/fasrc/User_Codes) repo. We try to test the main software used on the cluster.

* AI
  * PyTorch: pulls PyTorch Singularity image and runs [`check_gpu.py`](https://github.com/fasrc/User_Codes/blob/master/AI/PyTorch/check_gpu.py) inside the container
  * TensorFlow: pulls TenforFlow Singularity image and runs [`tf_test_multi_gpu.py`](https://github.com/fasrc/User_Codes/tree/master/AI/TensorFlow/Example4/tf_test_multi_gpu.py) inside the container
* Languages
  * Cpp: runs [`dot_prod.cpp`](https://github.com/fasrc/User_Codes/tree/master/Languages/Cpp/dot_prod.cpp)
  * Python
    * `Example1/monte_carlo_pi.py` runs [`mc_pi.py`](https://github.com/fasrc/User_Codes/tree/master/Languages/Python/Example1/mc_pi.py)
    * `Example3/mamba_env.py` runs [`build_env.sh`](https://github.com/fasrc/User_Codes/tree/master/Languages/Python/Example3/build_env.sh) to build a mamba environment and [`numpy_pandas_ex.py`](https://github.com/fasrc/User_Codes/tree/master/Languages/Python/Example3/numpy_pandas_ex.py) to use python packages installed in the mamba environment
  * R: runs [`count_down.R`](https://github.com/fasrc/User_Codes/tree/master/Languages/R/Example1/count_down.R)
* Parallel computing
  * Matlab: runs [`parallel_monte_carlo.m`](https://github.com/fasrc/User_Codes/tree/master/Parallel_Computing/MATLAB/Example1/parallel_monte_carlo.m)

The reframe tests that run the codes listed above were modified tests from [Reframe tutorial](https://reframe-hpc.readthedocs.io/en/stable/tutorial_basics.html) and from University of Southern California [uschpc reframe repo](https://github.com/uschpc/reframe-tests/tree/main/tests). These tests can be run either from a login or a compute node as ReFrame runs these tests by submitting jobs to the Slurm scheduler.   

### System
These tests are to verify various aspects of the system.  Here is a short description of each test.

* io: Test runs IOR on several filesystems. Originally from CSCS 
* slurm: Various slurm sanity checks. Originally from CSCS

## Reframe Docs
https://github.com/eth-cscs/reframe

https://reframe-hpc.readthedocs.io/en/stable/index.html
