from astroquery.mast import Observations
from s3fs.core import S3FileSystem

def load_data(ul_dir='s3://ece5984-s3-perindom/hwo_datalake', limit=100):
    s3 = S3FileSystem()
    dl_dir = '/tmp'
    # Astroquery configuration
    Observations.TIMEOUT = 1200  # 20 minutes timeout for API requests
    jw = Observations.query_criteria(dataRights='public',calib_level=3, intentType='science', dataproduct_type='IMAGE', obs_collection='JWST')

    for i, datum in enumerate(jw):
        if i > limit:
            break
        product_path = datum['jpegURL']
        product_name = product_path.split('/')[-1]
        save_file_path = Observations.download_file(product_path, local_path=dl_dir+'/'+product_name, cache=True)
        # Push data to S3 bucket as a pickle file
        with s3.open('{}/{}'.format(ul_dir, product_name), 'wb') as f:
            s3.put(dl_dir+'/'+product_name, ul_dir)
