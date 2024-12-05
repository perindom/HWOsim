import s3fs
from s3fs.core import S3FileSystem
import numpy as np
import pickle
import pandas as pd
import tempfile

def perturbation():
    s3 = S3FileSystem()
    # S3 bucket directory (data warehouse)
    DIR_datalake = 's3://ece5984-s3-perindom/hwo_datalake'
    DIR_warehouse = 's3://ece5984-s3-perindom/hwo_warehouse'

    # Save model temporarily
    with tempfile.TemporaryDirectory() as tempdir:
        lstm_aapl.save(f"{tempdir}/lstm_aapl.h5")
        # Push saved model to S3
        s3.put(f"{tempdir}/lstm_aapl.h5", f"{DIR_aapl}/lstm_aapl.h5")


    with tempfile.TemporaryDirectory() as tempdir:
        lstm_googl.save(f"{tempdir}/lstm_googl.h5")
        # Push saved temporary model to S3
        s3.put(f"{tempdir}/lstm_googl.h5", f"{DIR_googl}/lstm_googl.h5")
