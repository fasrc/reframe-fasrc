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

### System
These tests are to verify various aspects of the system.  Here is a short description of each test.

* io: Test runs IOR on several filesystems. Originally from CSCS 
* slurm: Various slurm sanity checks. Originally from CSCS

## Reframe Docs
https://github.com/eth-cscs/reframe

https://reframe-hpc.readthedocs.io/en/stable/index.html
