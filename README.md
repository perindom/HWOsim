# HWOsim
### Simulating NASA HWO Observatory Data Streams using existing batched data.

#### Team Members:
- Dominick Perini
- Jeri Brentlinger

## Project Description

### Objective
The **HWOsim** project aims to develop a scalable, high-fidelity data engineering pipeline that simulates real-world data streams for the [NASA Habitable Worlds Observatory](https://science.nasa.gov/astrophysics/programs/habitable-worlds-observatory/) (HWO). The pipeline leverages archival data from the [James Webb Space Telescope](https://science.nasa.gov/mission/webb/) (JWST) and introduces controlled data perturbations to create a realistic environment for testing AI models. The ultimate objective is to ensure the readiness of AI systems for live mission operations in detecting, analyzing, and interpreting astronomical phenomena.

### Problem Statement
In preparation for the launch of future NASA observatories, such as HWO, there is a critical need for robust AI models capable of processing large-scale, real-time data streams from space telescopes. However, the unpredictable nature of live data streams, characterized by noise, data loss, and other anomalies, poses a significant challenge for AI deployment. Currently, no existing framework simulates these real-world conditions with the fidelity required for pre-deployment AI testing.

HWOsim addresses this gap by creating a reproducible pipeline that:
1. Simulates the live-streaming environment using archived astronomical data.
2. Introduces controlled imperfections (perturbations) to mimic real-world data irregularities.
3. Allows for configurable testing of AI models against varying streaming rates and perturbation levels.

### Why This Problem Matters
The success of future space missions relies heavily on the ability to analyze data in real-time, detecting critical events such as potential exoplanet signatures, anomalies, or other phenomena of interest. AI systems must be resilient to data imperfections and scalable to handle massive data volumes. By solving this problem, HWOsim:
- **Enhances AI robustness**: Prepares models to handle live-streamed data with unpredictable characteristics.
- **Promotes reproducibility**: Provides the scientific community with an open-source framework for testing operational AI systems.
- **Supports mission success**: Contributes to the readiness and reliability of AI tools for NASA's upcoming HWO mission.

### Dataset and Provenance  

The [**Mikulski Archive for Space Telescopes (MAST)**](https://archive.stsci.edu/), a NASA-funded repository, serves as the cornerstone for this project’s data. MAST provides access to a comprehensive collection of scientifically validated astronomical datasets, with an emphasis on the optical, ultraviolet, and near-infrared parts of the spectrum. Specifically, this project leverages archives from the [**James Webb Space Telescope (JWST)**](https://archive.stsci.edu/missions-and-data/jwst) mission, one of the most advanced astronomical observatories, to simulate future Habitable Worlds Observatory (HWO) data streams.  

The datasets accessed via MAST are renowned for their authenticity, reliability, and scientific rigor. By building on this foundation, the project ensures that the simulated environment is grounded in real-world, high-fidelity data, enabling meaningful research and experimentation.  

### Data Transformations  
To mimic the unpredictability of real-world streaming data from the future HWO mission, controlled **data perturbations** are applied to the JWST datasets. These perturbations simulate environmental and operational challenges, such as:  
- **Noise Introduction**: Emulating instrumental or transmission noise.  
- **Missing Values**: Representing gaps due to observational limitations or system outages.  
- **Data Drift**: Simulating gradual changes in data distribution over time.  

These transformations are implemented dynamically within the pipeline using Python’s **pandas** library and are designed to reflect real-time streaming conditions. The modifications are strictly cosmetic; the core scientific integrity of the data remains intact.  

By introducing these transformations, the pipeline replicates operational challenges that AI models are likely to encounter during HWO’s mission. This approach ensures robust testing and validation of algorithms and workflows, equipping researchers with tools to analyze and adapt to live-streamed astronomical data effectively.  

## Pipeline Architecture
HWOsim's pipeline is comprised of these steps:
1. **Batch ingest archival data to an S3 data lake**: Use Astroquery and AWS S3 to collect JWST data and store it in a scalable data lake.
2. **Employ perturbation techniques**: Introduce controlled imperfections (e.g., noise, missing values, and data drift) to simulate live-streamed, uncleaned data conditions.
3. **Simulate streaming live data using MySql**: Read data from the S3-stored batches, apply perturbations in real-time, and stream it to downstream consumers (e.g., AI models or visualization tools).
4. **Configurable streaming**: Enable users to adjust perturbation levels and streaming frequency, allowing testing of model resilience to real-world data variations.

### Pipeline Infographic

![image](https://github.com/user-attachments/assets/5167e8a5-66a6-4417-9125-b14d642ec36b)



### Tools & Technologies

- Cloud - [**Amazon Web Services (AWS)**](https://aws.amazon.com/), [**Amazon Elastic Compute Cloud (Amazon EC2)**](https://aws.amazon.com/pm/ec2/)
- Containerization - [**Docker**](https://www.docker.com)
- Analytics Database Storage - [**MySQL**](https://www.mysql.com/)
- Orchestration - [**Apache Airflow**](https://airflow.apache.org)
- Transformation - [**Python Pillow Library**](https://pypi.org/project/pillow/)
- Data Lake & Data Warehouse - [**Amazon Simple Storage Service (Amazon S3)**](https://aws.amazon.com/s3/)
- Data Visualization - [**Matplotlib**](https://pypi.org/project/matplotlib/)
- Language - [**Python**](https://www.python.org)

## Data Transformation  
We introduce controlled perturbations to the archived data from the future Habitable Worlds Observatory (HWO) to simulate live-streaming data from the James Webb Space Telescope (JWST). These perturbations mimic the unpredictable nature of real-world streaming data and are a critical component of our pipeline.

The transformations include:  
- **Noise Addition**: Introducing random noise to emulate signal interference or transmission errors.  
- **Missing Values**: Simulating incomplete data streams caused by telemetry loss or hardware glitches.  
- **Data Drift**: Applying gradual changes to the data to represent evolving conditions, such as sensor recalibrations or environmental effects.  

These perturbations are dynamically applied to the data using Python and integrated into the pipeline through the **Perturbation** module. By introducing these transformations, we ensure the pipeline accurately reflects the challenges of real-time data ingestion and processing, enabling robust AI/ML model development and testing.

## Replicating this Project  

Follow the instructions below to replicate this project and run the data pipeline to simulate future HWO datastreams. Ensure that all prerequisites are installed and configured correctly before proceeding.

#### Environment  
1. **Operating System**: This pipeline is compatible with Linux, macOS, and Windows environments.  
2. **Programming Languages**: Python 3.8 or higher is required.  
3. **Python Libraries**: Install the dependencies listed in `requirements.txt` using the command:  
   ```bash
   pip install -r requirements.txt
   ```
4. **Cloud Resources**: AWS S3: Used for the data lake and data warehouse layers. Ensure you have valid AWS credentials configured.
5. **Optional Tools**: Docker (for containerizing and orchestrating the pipeline).

#### Steps
Follow these steps to replicate the pipeline:
1. **Clone the Repository**: Clone this repository to your local machine:
```
git clone https://github.com/perindom/HWOsim.git
cd HWOsim
```
2. **Set Up the Environment**: Create a virtual environment and activate it:
```
python3 -m venv env  
source env/bin/activate  # For Linux/macOS  
env\Scripts\activate  # For Windows
```
3. **Prepare Cloud Resources**:Create an AWS S3 bucket and update the bucket name in scripts. Set up Apache Kafka locally or in the cloud.
4. **Run the Pipeline**:
- Batch Ingestion: (dag.py)
```
python batch_ingest.py
```
- Perturbations: (dag_perturbation.py)
```
python apply_perturbations.py
```
- Send to MySQL: (dag_send.py)
```
python mysqlcode.py
```
5. **Visualize Results**: Analyze processed data using visualization tools like Tableau or custom dashboards.



### Thorough Investigation  

This project represents an innovative step toward simulating live-streaming data environments for future missions like NASA’s Habitable Worlds Observatory (HWO). By leveraging archival datasets from the James Webb Space Telescope (JWST) and introducing realistic perturbations, this pipeline effectively creates a high-fidelity testbed for developing and validating AI-driven analytical systems.  

#### Viability and Scalability  
The results of this pilot project demonstrate the technical feasibility of simulating real-time data streams with controlled perturbations. The modular design of the pipeline ensures flexibility, allowing it to scale with additional datasets, more complex perturbation techniques, and enhanced streaming frequencies.  
- **Scalability Potential**: With additional computational and cloud resources, this pipeline can be expanded to process larger volumes of data or accommodate real-time analysis for multiple observatories simultaneously.  
- **Adaptability**: The pipeline’s architecture is modular, making it easy to integrate new data sources, refine perturbation methods, or incorporate additional analytics capabilities.  

#### Innovation Assessment  
This project is highly innovative in its application of controlled perturbations to simulate live-streamed astronomical data. It bridges a critical gap in preparing AI models for operational deployment by providing a realistic and reproducible data environment. This approach ensures that AI systems are robust, adaptable, and ready to handle the complexities of live space mission data.  

#### Technical and Platform Challenges  
While the project achieved its objectives, several challenges were identified:  
- **Cloud Resource Costs**: Scaling up S3 storage and streaming simulations with Apache Kafka incurs significant cloud costs. Cost optimization strategies are essential for sustainability.  
- **Data Latency**: Real-time streaming simulations require low-latency infrastructure, which may demand higher-end hardware or more optimized configurations.  
- **Perturbation Complexity**: Introducing more advanced or mission-specific perturbations will require further research and computational power.  

#### Recommendations for Next Steps  
To take this project to the next phase, we recommend the following:  
1. **Integrate More Datasets**: Expand the pipeline to include additional archival datasets, such as those from the Hubble Space Telescope or TESS, to enhance versatility.  
2. **Optimize Perturbation Algorithms**: Refine the perturbation methods to reflect even more realistic mission scenarios, including dynamic changes in data quality or observational conditions.  
3. **Enhance Real-Time Capabilities**: Invest in infrastructure improvements to minimize latency and enable real-time processing at scale.  
4. **Develop Advanced Analytics**: Incorporate machine learning models into the pipeline to autonomously detect anomalies, classify events, or predict trends in the streaming data.  
5. **Collaborate with Mission Teams**: Engage with NASA teams and the broader scientific community to align the pipeline with operational needs and ensure its readiness for mission deployment.  

This project lays a strong foundation for the future of data engineering in space missions, demonstrating both technical feasibility and potential for significant scientific impact. By continuing to develop and refine this pipeline, it can serve as a critical tool for enabling AI-driven discovery in the next generation of astronomical missions.  

