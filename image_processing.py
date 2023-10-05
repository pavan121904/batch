from PIL import Image
import boto3
from io import BytesIO

def resize_image_s3(input_bucket, input_key, output_bucket, output_key, width, height):
    """
    Resize an image stored in an S3 bucket using Pillow.

    Args:
    - input_bucket (str): Name of the input S3 bucket.
    - input_key (str): Key (path) of the input image in the input bucket.
    - output_bucket (str): Name of the output S3 bucket.
    - output_key (str): Key (path) to save the resized image in the output bucket.
    - width (int): New width for the image.
    - height (int): New height for the image.
    """
    try:
        # Initialize S3 client
        s3 = boto3.client("s3")

        # Download the input image from S3
        response = s3.get_object(Bucket=input_bucket, Key=input_key)
        image_bytes = response["Body"].read()

        # Open the image using Pillow
        image = Image.open(BytesIO(image_bytes))

        # Resize the image
        resized_image = image.resize((width, height), Image.ANTIALIAS)

        # Save the resized image to a buffer
        output_buffer = BytesIO()
        resized_image.save(output_buffer, format="JPEG")

        # Upload the resized image back to S3
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=output_buffer.getvalue(),
            ContentType="image/jpeg"  # Adjust the content type as needed
        )

        print(f"Image resized and saved to s3://{output_bucket}/{output_key}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Replace these values with your S3 bucket and file paths
    input_bucket = "pvn-input"
    input_key = "input.jpg"
    output_bucket = "pvn-output"
    output_key = "output.jpg"

    # Set the new dimensions for the resized image
    new_width = 200
    new_height = 200

    # Call the resize_image_s3 function
    resize_image_s3(input_bucket, input_key, output_bucket, output_key, new_width, new_height)
