import os
from astroquery.mast import Observations
import boto3
import time

# AWS S3 Configuration
s3_client = boto3.client("s3")
S3_BUCKET = "ece5984-s3-brentlinger"
S3_PATH = "JWST_Project/Data_Lake/"

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
        observations = Observations.query_criteria(obs_collection="JWST", dataproduct_type="image", obs_id="*")
        fits_products = Observations.get_product_list(observations)

        # Filter only public FITS files
        fits_products = fits_products[fits_products["productFilename"].astype(str).str.endswith(".fits")]
        fits_products = fits_products[fits_products["dataRights"] == "PUBLIC"]
        print(f"Found {len(fits_products)} public FITS files.")

        # Limit files for processing
        fits_products = fits_products[:limit]
        print(f"Processing first {len(fits_products)} files...")

        for idx, file_info in enumerate(fits_products):
            file_name = file_info["productFilename"]
            file_url = file_info["dataURI"]
            download_path = os.path.join(DOWNLOAD_DIR, file_name)

            try:
                print(f"Downloading {file_name} ({idx + 1}/{len(fits_products)})...")
                Observations.download_file(file_url, download_path)
                print(f"Downloaded to {download_path}")

                # Upload to S3
                s3_client.upload_file(download_path, S3_BUCKET, f"{S3_PATH}{file_name}")
                print(f"Uploaded {file_name} to s3://{S3_BUCKET}/{S3_PATH}{file_name}")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

        print("All files have been processed.")
    except Exception as e:
        print(f"An error occurred during data retrieval: {e}")

# Main execution
if __name__ == "__main__":
    start_time = time.time()
    fetch_and_upload_jwst_data(limit=100)
    end_time = time.time()
    print(f"Script completed in {end_time - start_time:.2f} seconds.")
