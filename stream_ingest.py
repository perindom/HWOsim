import time
from kafka import KafkaConsumer
from json import loads
import json
from s3fs import S3FileSystem

def kafka_consumer():
    s3 = S3FileSystem()
    DIR = 's3://ece5984-s3-perindom/hwosim'
    t_end = time.time() + 60 * 10 # Amount of time data is sent for
    while time.time() < t_end:
        consumer = KafkaConsumer('jwst', # add Topic name here
                                 bootstrap_servers=['34.227.190.251:9092'], # add your IP and port number here
                                 value_deserializer=lambda x: loads(x.decode('utf-8')))
        for count, jwimage in enumerate(consumer):
            buffer = io.BytesIO()
            jwimage.save(buffer, format='JPEG')
            buffer.seek(0)
            with s3.open("{}/jwst_image_{}.jpg".format(DIR, count), 'wb') as s3_file:
                s3_file.write(jwimage)
    print("done consuming")
