from astroquery.mast import Observations
from datetime import datetime
import os

if __name__ == '__main__':
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
        i += 1
        if i > 10:
            break
