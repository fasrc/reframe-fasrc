# reframe-fasrc
FASRC specific configuration for Reframe

## Tests
Tests currently are copied from the cscs-checks folder in reframe and tuned to the FASRC environment.

### Microbenchmarks
These are benchmark tests that are broken down by category.  Here is a sort description of each test:

#### cpu
* alloc_speed: Tests speed of memory allocation
* dgemm: Runs dgemm code to get a measure of FLOps
* latency: Measures latency to L1, L2, L3 cache
* stream: Runs STREAM test for measuring memory bandwidth.

## Reframe Docs
https://github.com/eth-cscs/reframe

https://reframe-hpc.readthedocs.io/en/stable/index.html
