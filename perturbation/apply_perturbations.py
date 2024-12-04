import boto3
import numpy as np
from astropy.io import fits
import io

# AWS S3 Configuration
s3_client = boto3.client("s3")
SOURCE_BUCKET = "ece5984-s3-brentlinger"
SOURCE_PREFIX = "JWST_Project/Data_Lake/"
DEST_PREFIX = "JWST_Project/Applied_Perturbations/"

# Perturbation parameters
NOISE_STD = 0.01  # Gaussian noise standard deviation
MISSING_VALUE_PROB = 0.1  # Probability of missing values
DATA_CORRUPTION_PROB = 0.05  # Probability of random data corruption

def apply_perturbations(data):
    """
    Add noise, missing values, and random corruption to a data array.
    """
    perturbed = data.copy()

    # Apply Gaussian noise
    perturbed += np.random.normal(0, NOISE_STD, perturbed.shape)

    # Introduce missing values
    perturbed[np.random.rand(*perturbed.shape) < MISSING_VALUE_PROB] = np.nan

    # Apply random corruption
    corruption_mask = np.random.rand(*perturbed.shape) < DATA_CORRUPTION_PROB
    perturbed[corruption_mask] = np.random.uniform(
        low=np.nanmin(perturbed), high=np.nanmax(perturbed), size=corruption_mask.sum()
    )

    return perturbed

def process_and_upload_fits_from_s3(s3_key):
    """
    Fetch FITS file from S3, apply perturbations, and upload the perturbed file back to S3.
    """
    # Download FITS file from the source bucket
    file_obj = s3_client.get_object(Bucket=SOURCE_BUCKET, Key=s3_key)
    with fits.open(io.BytesIO(file_obj['Body'].read())) as hdul:
        data = hdul[0].data
        if data is None:
            print(f"Skipping {s3_key}: No data found.")
            return

        # Apply perturbations
        hdul[0].data = apply_perturbations(data)

        # Save the perturbed file to an in-memory buffer
        buffer = io.BytesIO()
        hdul.writeto(buffer, overwrite=True)
        buffer.seek(0)

        # Define the destination S3 key
        dest_key = f"{DEST_PREFIX}{s3_key.split('/')[-1]}"

        # Upload the perturbed file to the destination bucket
        s3_client.upload_fileobj(buffer, SOURCE_BUCKET, dest_key)
        print(f"Uploaded: s3://{SOURCE_BUCKET}/{dest_key}")

def process_all_fits_in_s3():
    """
    List all FITS files in the source bucket and process them.
    """
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=SOURCE_BUCKET, Prefix=SOURCE_PREFIX):
        for obj in page.get("Contents", []):
            if obj["Key"].endswith(".fits"):
                process_and_upload_fits_from_s3(obj["Key"])

if __name__ == "__main__":
    print(f"Processing FITS files from s3://{SOURCE_BUCKET}/{SOURCE_PREFIX} and uploading to s3://{SOURCE_BUCKET}/{DEST_PREFIX}...")
    process_all_fits_in_s3()
    print("All files processed and uploaded.")
