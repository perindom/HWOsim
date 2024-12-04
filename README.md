# HWOsim
Simulating NASA HWO Observatory Data Streams using existing archival (batched) data.


## Description

### Objective

This project focuses on developing a data engineering pipeline to simulate future [NASA Habitable Worlds Observatory](https://science.nasa.gov/astrophysics/programs/habitable-worlds-observatory/) (HWO) data streams, leveraging archives from the [James Webb Space Telescope](https://science.nasa.gov/mission/webb/) (JWST). The goal is to provide a realistic, high-fidelity data environment for AI models that will be deployed to analyze live-streamed data from the HWO mission. A vital component of this simulation is data perturbation. This technique introduces controlled imperfections, such as noise, missing values, and data drift, to mimic the unpredictable nature of real-world data.


### Dataset
The [Mikulski Archive for Space Telescopes (MAST)](https://archive.stsci.edu/) is a NASA funded project to support and provide to the astronomical community a variety of astronomical data archives, with the primary focus on scientifically related data sets in the optical, ultraviolet, and near-infrared parts of the spectrum.
[HWOsim](https://github.com/perindom/HWOsim) utilizes data obtained from the MAST Portal, focusing on diverse datasets from the [JWST Mission](https://archive.stsci.edu/missions-and-data/jwst).

