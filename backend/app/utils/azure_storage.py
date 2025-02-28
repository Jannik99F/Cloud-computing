import os
from azure.storage.blob import BlobServiceClient, ContentSettings
import uuid

class AzureBlobStorage:
    def __init__(self):
        # Azure Blob Storage connection string
        connection_string = ""
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = "furniture-images"
        
        # Create the container if it doesn't exist
        self._create_container_if_not_exists()
    
    def _create_container_if_not_exists(self):
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            # Check if container exists by listing blobs
            container_client.list_blobs().next()
        except (StopIteration, Exception):
            # Container doesn't exist or error getting container, let's create it
            try:
                self.blob_service_client.create_container(self.container_name, public_access="blob")
            except Exception as e:
                print(f"Error creating container: {str(e)}")
    
    def upload_image(self, image_data, filename=None, content_type="image/jpeg"):
        """
        Upload an image to Azure Blob Storage
        
        Args:
            image_data: The bytes data of the image
            filename: Optional custom filename, if None a UUID will be generated
            content_type: The content type of the image (default: image/jpeg)
            
        Returns:
            URL of the uploaded image
        """
        if not filename:
            # Generate a unique filename with UUID
            filename = f"{str(uuid.uuid4())}.jpg"
        
        # Get blob client
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name, 
            blob=filename
        )
        
        # Set the content settings
        content_settings = ContentSettings(content_type=content_type)
        
        # Upload the image data
        blob_client.upload_blob(
            image_data,
            content_settings=content_settings,
            overwrite=True
        )
        
        # Return the URL to the blob
        return blob_client.url
    
    def delete_image(self, image_url):
        try:
            # Extract the blob name from the URL
            blob_name = image_url.split('/')[-1]
            
            # Get blob client
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, 
                blob=blob_name
            )
            
            # Delete the blob
            blob_client.delete_blob()
            return True
        except Exception as e:
            print(f"Error deleting blob: {str(e)}")
            return False