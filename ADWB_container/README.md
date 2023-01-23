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