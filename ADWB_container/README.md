# Alzheimer Disease WorkBench container

This folder contains the build script for a single container container:
- The web interface on port 5000
- A GraphDB instance on port 7200
- A Triplifier instance on port 8080

**This is not the intended method to use docker containers, but works for testing purposes.**

## How to build?
Run the script [run.sh](run.sh). This will build the Triplifier, and build the web interface on top of the GraphDB docker image.

## For development
If you need to recompile multiple times (and do not need the triplifier maven build), you can speed up the process **after the first build** by running [run_build_short.sh](run_build_short.sh).

If you want to do live development/debugging on the web interface, you can run [run_dev.sh](run_dev.sh). This will mount the [../management_webpage](../management_webpage) folder in the container.

## Build times
For reference, added some build times for the project.

**macOS**:
- [4 cpu, 1gb swap, 8gb mem, Macbook Pro i5 mid 2019] sh run.sh  23,05s user 75,05s system 6% cpu 23:43,29 total

**Windows (WSL2)**:
- [4 cpu, 16gb mem, i7-7660U surface pro 2017] sh run.sh 2.54s user 3.27s system 1% cpu 7:06.60 total

**Update**: It now works on macOS, checkout of repository *within* running docker image removes volume mount overhead and brings build time in ballpark of WSL2 and Ubuntu (native Docker)
