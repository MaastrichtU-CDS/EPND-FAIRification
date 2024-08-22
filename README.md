<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Apache License][license-shield]][license-url]

<br />
<div align="center">
  <h3 align="center">FairNotator</h3>

  <p align="center">
    Annotate mappings for all your data sources
    <br />
    <a href="https://github.com/MaastrichtU-CDS/EPND-FAIRification"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://maastrichtu-cds.github.io/EPND-FAIRification/#">View Demo</a>
    ·
    <a href="https://github.com/MaastrichtU-CDS/EPND-FAIRification/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/MaastrichtU-CDS/EPND-FAIRification/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

## About The Project
This project is meant as a starting point for a new FairNotator. The goal is to create a simple interface to allow domain experts to map the syntax of their local data (CSV is assumed for the time being) to a common terminology (currently represented as an excel sheet).

The output of the mapping is a JSON-LD, which is to be used as a starting point that can be plugged into a variety of ETL solutions based on project needs (such as OMOP or R2RML ETL pipelines).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![React](https://img.shields.io/badge/-ReactJs-61DAFB?logo=react&logoColor=white&style=for-the-badge)](https://react.dev/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Prerequisites
 - [Node.js & npm](https://nodejs.org/en)

## Getting Started
For development and testing, run:
```
npm start
```

The current version is not configurable yet and uses hardcoded values for the column names of the terminology sheet. Copy paste the contents of [this file](https://github.com/MaastrichtU-CDS/EPND-FAIRification/blob/main/EPNDCS1Terminology.xls) to a google sheet to link to.

The [dummydata.csv](https://github.com/MaastrichtU-CDS/EPND-FAIRification/blob/fairnotator-1.0/dummydata.csv) file can be used as an example of a local data file.

[output_example.json](https://github.com/MaastrichtU-CDS/EPND-FAIRification/blob/fairnotator-1.0/output_example.json) provides an example of what outputs should look like.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

See the [open issues](https://github.com/MaastrichtU-CDS/EPND-FAIRification/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the Apache 2.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/MaastrichtU-CDS/EPND-FAIRification.svg?style=for-the-badge
[contributors-url]: https://github.com/MaastrichtU-CDS/EPND-FAIRification/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/MaastrichtU-CDS/EPND-FAIRification.svg?style=for-the-badge
[forks-url]: https://github.com/MaastrichtU-CDS/EPND-FAIRification/network/members
[stars-shield]: https://img.shields.io/github/stars/MaastrichtU-CDS/EPND-FAIRification.svg?style=for-the-badge
[stars-url]: https://github.com/MaastrichtU-CDS/EPND-FAIRification/stargazers
[issues-shield]: https://img.shields.io/github/issues/MaastrichtU-CDS/EPND-FAIRification.svg?style=for-the-badge
[issues-url]: https://github.com/MaastrichtU-CDS/EPND-FAIRification/issues
[license-shield]: https://img.shields.io/github/license/MaastrichtU-CDS/EPND-FAIRification.svg?style=for-the-badge
[license-url]: https://github.com/MaastrichtU-CDS/EPND-FAIRification/blob/main/LICENSE