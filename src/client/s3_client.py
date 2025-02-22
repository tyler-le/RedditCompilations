import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class S3Client:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = "rscraped"
    
    def upload_to_s3(self, local_path):
        """Upload file to S3."""
        s3_path = self.get_postfix_after_output(local_path)
        try:
            with open(local_path, "rb") as f:
                self.s3_client.upload_fileobj(f, self.bucket_name, s3_path)
            print(f"✅ Successfully uploaded {local_path} to S3 at {s3_path}")
        except FileNotFoundError:
            print(f"❌ File not found: {local_path}")
        except NoCredentialsError:
            print("❌ AWS credentials not found.")
        except PartialCredentialsError:
            print("❌ Incomplete AWS credentials.")
        except Exception as e:
            print(f"❌ Failed to upload {local_path} to S3: {e}") 

    @staticmethod
    def get_postfix_after_output(file_path):
        # Split the path at 'output' and get the part after it
        parts = file_path.split(os.path.sep)
        # Find the index of 'output' in the parts and get everything after it
        try:
            output_index = parts.index('output')
            postfix = os.path.sep.join(parts[output_index + 1:])
            return postfix
        except ValueError:
            return "output" 