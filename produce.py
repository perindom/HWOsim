import sys
from datetime import datetime
from kafka import KafkaProducer
from json import dumps
import requests
import astroquery
from PIL import Image
import os
import time

def get_jwst_data(producer, max_examples=1000):
    jw = Observations.query_criteria(obs_collection='JWST')
    datalist = jw[jw['dataproduct_type'] == 'image']
    current_time = datetime.now().strftime("%H_%M")
    # Specify the directory name and path
    directory_name = './data_' + str(current_time) +'/'
    path = "./" + directory_name  # Creates the directory in the current working directory
    # Create the directory
    os.mkdir(path)
    i = 0
    for row in datalist:
        product_path = row['jpegURL']
        save_file_path = Observations.download_file(product_path, local_path=directory_name+product_path.split('/')[-1], cache=True)
        # Sloppy way to transfer data to a variable...
        image = Image.open(save_file_path)
        producer.send('jwst', value=image)
        print('Image Sent!')
        i += 1
        if i > max_examples:
            break	

def kafka_producer(ip):
    producer = KafkaProducer(bootstrap_servers=[ip]) # change ip and port number here
    get_jwst_data(producer, max_examples=100)
    print("done producing")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print('Arguments passed: ', sys.argv[1:])
    kafka_producer(ip=sys.argv[1])
