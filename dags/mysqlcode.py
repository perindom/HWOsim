from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import numpy as np
from s3fs.core import S3FileSystem

def send_images():
    s3 = S3FileSystem()

    # S3 bucket directory (data warehouse)
    SOURCE_BUCKET = 's3://ece5984-s3-perindom'
    SOURCE_DIR = 'hwo_warehouse'
    
    # Download JPEG file from the source bucket
    s3 = S3FileSystem()

    # Get the list of all files in the source directory
    source_files = s3.glob(f"{SOURCE_BUCKET}/{SOURCE_DIR}**")

    # Create sqlalchemy engine to connect to MySQL
    user = "admin"
    pw = "9G>c(JolkKDkpanP:jBfp?P+<{yJ" # Update the password to the latest password from db_info.txt file inside EC2 instance
    endpnt = "data-eng-db.cluster-cwgvgleixj0c.us-east-1.rds.amazonaws.com"
    db_name = "perindom" # Name of the database: Insert your PID (email without @vt.edu) here

    # Connect to MySQL server (without specifying a database)
    engine = create_engine(f"mysql+pymysql://{user}:{pw}@{endpnt}")

    # Check if the database already exists
    with engine.connect() as connection:
        db_exists = connection.execute(f"SHOW DATABASES LIKE'{db_name}';").fetchone()
        if not db_exists:
            # Create the database if it does not exist
            connection.execute(f"CREATE DATABASE {db_name}")

    # Reconnect to the specific database
    engine = create_engine(f"mysql+pymysql://{user}:{pw}@{endpnt}/{db_name}")
    
    # Loop through each file and copy to the destination directory
    for source_file in source_files:
        # Extract the filename from the source path
        filename = source_file.split('/')[-1]

        # Define the destination file path
        dest_file = f"{SOURCE_BUCKET}/{DEST_DIR}{filename}"

        try:
            # Get the file object from S3
            with s3.open(source_file, 'rb') as f:
                # Read the file into a PIL image
                img = Image.open(f)

                # Convert the image to a NumPy array
                img_array = np.array(img)
                img_array.to_sql(filename, con=engine, if_exists='replace', chunksize=1000)
        except Exception as e:
            print(e)
