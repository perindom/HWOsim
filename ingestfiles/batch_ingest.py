import os
from astroquery.mast import Observations
import boto3
import time

# AWS S3 Configuration
s3_client = boto3.client("s3")
S3_BUCKET = "ece5984-s3-perindom"
S3_PATH = "hwo_datalake"

# Temporary directory for downloads
DOWNLOAD_DIR = "/root/jwst_downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Astroquery configuration
Observations.TIMEOUT = 1200  # 20 minutes timeout for API requests

def fetch_and_upload_jwst_data(limit=100):
    """
    Query, download, and upload JWST public FITS files to S3.
    """
    print("Querying JWST data from MAST...")

    try:
        # Query public JWST observations
        observations = Observations.query_criteria(obs_collection="JWST")
	datalist = observations[observations['dataproduct_type'] == 'image']
	i=0
        for row in datalist:
            product_path = row['jpegURL']
            save_file_path = Observations.download_file(product_path, local_path='.'+product_path.split('/')[-1], cache=True)
            # Upload to S3
            s3_client.upload_file(download_path, S3_BUCKET, f"{S3_PATH}{file_name}")
            print(f"Uploaded {file_name} to s3://{S3_BUCKET}/{S3_PATH}{file_name}")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")
            i+1
            if i > limit:
                break

        print(f"All {i} files have been processed.")
    except Exception as e:
        print(f"An error occurred during data retrieval: {e}")

# Main execution
if __name__ == "__main__":
    start_time = time.time()
    fetch_and_upload_jwst_data(limit=100)
    end_time = time.time()
    print(f"Script completed in {end_time - start_time:.2f} seconds.")
