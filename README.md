# HWOsim

Simulating NASA HWO Observatory Data Streams using existing batched data.

## Project Description

### Objective
The **HWOsim** project aims to develop a scalable, high-fidelity data engineering pipeline that simulates real-world data streams for the [NASA Habitable Worlds Observatory](https://science.nasa.gov/astrophysics/programs/habitable-worlds-observatory/) (HWO). The pipeline leverages archival data from the [James Webb Space Telescope](https://science.nasa.gov/mission/webb/) (JWST) and introduces controlled data perturbations to create a realistic environment for testing AI models. The ultimate objective is to ensure the readiness of AI systems for live mission operations in detecting, analyzing, and interpreting astronomical phenomena.

### Problem Statement
In preparation for the launch of future NASA observatories, such as HWO, there is a critical need for robust AI models capable of processing large-scale, real-time data streams from space telescopes. However, the unpredictable nature of live data streams, characterized by noise, data loss, and other anomalies, poses a significant challenge for AI deployment. Currently, there is no existing framework that simulates these real-world conditions with the fidelity required for pre-deployment AI testing.

HWOsim addresses this gap by creating a reproducible pipeline that:
1. Simulates the live-streaming environment using archived astronomical data.
2. Introduces controlled imperfections (perturbations) to mimic real-world data irregularities.
3. Allows for configurable testing of AI models against varying streaming rates and perturbation levels.

### Why This Problem Matters
The success of future space missions relies heavily on the ability to analyze data in real time, detecting critical events such as potential exoplanet signatures, anomalies, or other phenomena of interest. AI systems must be resilient to data imperfections and scalable to handle massive data volumes. By solving this problem, HWOsim:
- **Enhances AI robustness**: Prepares models to handle live-streamed data with unpredictable characteristics.
- **Promotes reproducibility**: Provides the scientific community with an open-source framework for testing operational AI systems.
- **Supports mission success**: Contributes to the readiness and reliability of AI tools for NASA's upcoming HWO mission.

## Dataset
The [Mikulski Archive for Space Telescopes (MAST)](https://archive.stsci.edu/) is a NASA-funded project to support and provide to the astronomical community a variety of astronomical data archives, with the primary focus on scientifically related data sets in the optical, ultraviolet, and near-infrared parts of the spectrum.  
[HWOsim](https://github.com/perindom/HWOsim) utilizes data obtained from the MAST Portal, focusing on diverse datasets from the [JWST Mission](https://archive.stsci.edu/missions-and-data/jwst).

## Pipeline Architecture
HWOsim's pipeline is comprised of these steps:
1. **Batch ingest archival data to an S3 data lake**: Use Astroquery and AWS S3 to collect JWST data and store it in a scalable data lake.
2. **Employ perturbation techniques**: Introduce controlled imperfections (e.g., noise, missing values, and data drift) to simulate live-streamed, uncleaned data conditions.
3. **Simulate streaming live data using Kafka**: Read data from the S3-stored batches, apply perturbations in real time, and stream it to downstream consumers (e.g., AI models or visualization tools).
4. **Configurable streaming**: Enable users to adjust perturbation levels and streaming frequency, allowing testing of model resilience to real-world data variations.


//INSERT INFOGRAPHIC here//

### Tools & Technologies

- Cloud - [**Amazon Web Services (AWS)**](https://aws.amazon.com/)
- Containerization - [**Docker**](https://www.docker.com)
- Stream Processing - [**Kafka**](https://kafka.apache.org), [**Spark Streaming**](https://spark.apache.org/docs/latest/streaming-programming-guide.html)
- Orchestration - [**Apache Airflow**](https://airflow.apache.org)
- Transformation - ?
- Data Lake & Data Warehouse - [**Amazon Simple Storage Service (Amazon S3)**](https://aws.amazon.com/s3/)
- Data Visualization - //INSERT WHATEVER WE USE HERE//
- Language - [**Python**](https://www.python.org)
