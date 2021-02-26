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
* alloc_speed: Tests speed of memory allocation
* dgemm: Runs dgemm code to get a measure of FLOps
* latency: Measures latency to L1, L2, L3 cache
* stream: Runs STREAM test for measuring memory bandwidth.
* strided_bandwidth: Runs bandwidth test with various stride sizes.

#### gpu
* gpu_burn: Burns in GPU and gives a report of GFLOps for one GPU and its temperature.
* kernel_latency: Tests latency in loading the NVIDIA kernel.
* memory_bandwidth: Tests GPU memory bandwidth.
* shmem: Tests shared memory bandwidth.

#### mpi
* fft: Test runs FFTW.
* halo_exchange: Simulates halo cell (aka ghost or boundary zone) exchange to test MPI communications.
* hpcg_benchmark: Runs the HPCG benchmark for gnu and MKL.
* osu: Various MPI benchmarks from OSU.

### System
These tests are to verify various aspects of the system.  Here is a short description of each test.

* io: Test runs IOR on several filesystems 
* slurm: Various slurm sanity checks

## Reframe Docs
https://github.com/eth-cscs/reframe

https://reframe-hpc.readthedocs.io/en/stable/index.html
