from s3fs import S3FileSystem
from astroquery.mast import Observations

def load_data(ul_dir='s3://ece5984-s3-perindom/hwo_datalake', limit=100):
    s3 = S3FileSystem()
    dl_dir = '/tmp'
    # Astroquery configuration
    Observations.TIMEOUT = 1200  # 20 minutes timeout for API requests
    
    # Query JWST public science images
    jw = Observations.query_criteria(
        dataRights='public',
        calib_level=3,
        intentType='science',
        dataproduct_type='IMAGE',
        obs_collection='JWST'
    )

    for i, datum in enumerate(jw):
        if i >= limit:
            break
        product_path = datum['jpegURL']
        if not product_path:
            print(f"No jpegURL for observation {datum['obs_id']}, skipping.")
            continue

        product_name = product_path.split('/')[-1]
        local_file_path = f"{dl_dir}/{product_name}"
        
        # Download the file locally
        try:
            _ = Observations.download_file(
                product_path, local_path=local_file_path, cache=True
            )
            # Upload the downloaded file to S3
            s3.put(local_file_path, f"{ul_dir}/{product_name}")
            print(f"Uploaded {product_name} to {ul_dir}")
        except Exception as e:
            print(f"Failed to process {product_name}: {e}")

