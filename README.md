# EPND FAIRifier / FAIRnotator

## Introduction

This repository contains the FAIRifier/FAIRnotator developed for the [European Platform for Neurodegenerative Diseases (EPND)](https://epnd.org). The tool available in this repository aims to interpret the FAIR implementation profile (FIP) definition, its referenced implementation profile files (in this case CEDAR templates to describe cohort metadata; and SHACL files to describe the information elements requested in the cohort), and present the end-user a web-based user interface to make their data FAIR and available to use within the EPND platform.

## How to run this software?

1. Checkout the git repository: `git clone https://github.com/MaastrichtU-CDS/EPND-FAIRification.git`
2. Open the folder: `cd EPND-FAIRification`
3. Execute the [docker-compose.yml](docker-compose.yml) file using `docker-compose up -d`.
4. Open [http://localhost:5000](http://localhost:5000) and follow the steps

To use a sample FAIR implementation profile (FIP) use the URL: `https://raw.githubusercontent.com/MaastrichtU-CDS/EPND-FAIRification/main/fip/fip.ttl`

## How to build this software?

The software is actually built when executing docker-compose (see above). To force a re-build, use `docker-compose up -d --build`.

## How to develop on the frond-end?

1. Stop the web-ui service container (`docker-compose stop webui && docker-compose rm webui`)
2. Go to the management_webpage folder, and execute run.sh after all python dependencies are installed
    ```
    cd management_webpage
    python -m venv ./venv
    source ./venv/Scripts/activate
    pip install -r requirements.txt
    sh run.sh
    ```
## Demo video
A demo video based on commit version [d763069](https://github.com/MaastrichtU-CDS/EPND-FAIRification/tree/d7630693527bd5c884fdd778caf41a43291074db) is available on YouTube: [https://www.youtube.com/watch?v=T3lE1kw55IE](https://www.youtube.com/watch?v=T3lE1kw55IE)
