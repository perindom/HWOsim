from PIL import Image
import numpy as np
import io
from s3fs.core import S3FileSystem

# AWS S3 Configuration
SOURCE_BUCKET = "ece5984-s3-perindom"
SOURCE_DIR = "hwo_datalake/"
DEST_DIR = "hwo_warehouse/"

# Constants for perturbations
NOISE_STD = 10  # Standard deviation for Gaussian noise
MISSING_VALUE_PROB = 0.05  # Probability of missing values
DATA_CORRUPTION_PROB = 0.05  # Probability of random corruption


def apply_perturbations_to_jpeg(image_array):
    """
    Add noise, missing values, and random corruption to a JPEG image represented as a numpy array.
    """

    # Ensure image has 3 channels (RGB)
    if image_array.ndim == 2:  # Grayscale image
        image_array = np.stack([image_array] * 3, axis=-1)  # Convert grayscale to RGB

    perturbed = image_array.copy()

    # Apply Gaussian noise
    perturbed = perturbed.astype(np.float32)
    perturbed += np.random.normal(0, NOISE_STD, perturbed.shape)

    # Introduce missing values (set some pixels to NaN)
    missing_mask = np.random.rand(*perturbed.shape[:2]) < MISSING_VALUE_PROB
    for channel in range(perturbed.shape[2]):
        perturbed[missing_mask, channel] = np.nan

    # Apply random corruption
    corruption_mask = np.random.rand(*perturbed.shape[:2]) < DATA_CORRUPTION_PROB
    for channel in range(perturbed.shape[2]):
        perturbed[corruption_mask, channel] = np.random.uniform(
            low=np.nanmin(perturbed[:, :, channel]),
            high=np.nanmax(perturbed[:, :, channel]),
            size=corruption_mask.sum()
        )
    # Replace NaN values with 0 (or another placeholder value)
    perturbed = np.nan_to_num(perturbed, nan=0)

    # Clip values to valid range for image data
    perturbed = np.clip(perturbed, 0, 255)

    return perturbed.astype(np.uint8)


def process_and_upload_jpeg_from_s3():
    """
    Fetch a JPEG file from S3, apply perturbations, and upload the perturbed file back to S3.
    """
    # Download JPEG file from the source bucket
    s3 = S3FileSystem()

    # Get the list of all files in the source directory
    source_files = s3.glob(f"{SOURCE_BUCKET}/{SOURCE_DIR}**")

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

                # Add random noise to the image
                noisy_img_array = apply_perturbations_to_jpeg(img_array)

                # Convert the NumPy array back to a PIL image
                noisy_img = Image.fromarray(noisy_img_array)

                # Save the noisy image to a byte stream
                with io.BytesIO() as output:
                    noisy_img.save(output, format="JPEG")
                    output.seek(0)

                    # Upload the modified image to the destination
                    s3.put(output, dest_file)

            print(f"Processed and uploaded {source_file} to {dest_file}")
        except Exception as e:
            print(f"Failed to process {source_file}: {e}")

    print("File processing completed.")


if __name__ == "__main__":
    print(
        f"Processing JPEG files from s3://{SOURCE_BUCKET}/{SOURCE_DIR} and uploading to s3://{SOURCE_BUCKET}/{DEST_DIR}...")
    process_and_upload_jpeg_from_s3()
    print("All files processed and uploaded.")
