import logging
from typing import Optional
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, ContainerClient, generate_blob_sas, BlobSasPermissions
from azure.core.exceptions import AzureError, ResourceExistsError
import streamlit as st
from utils.Config import Config

# Configure logging
logger = logging.getLogger(__name__)

class BlobStorageService:
    """Service for handling Azure Blob Storage operations."""
    
    _instance: Optional['BlobStorageService'] = None
    _blob_service_client: Optional[BlobServiceClient] = None
    
    def __new__(cls):
        """Implement singleton pattern to reuse client connection."""
        if cls._instance is None:
            cls._instance = super(BlobStorageService, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance
    
    def _initialize_client(self) -> None:
        """Initialize the Blob Service Client with connection retry logic."""
        try:
            connection_string = Config.get("AZURE_STORAGE_CONN_STRING")
            if not connection_string:
                raise ValueError("AZURE_STORAGE_CONN_STRING not configured")
            
            self._blob_service_client = BlobServiceClient.from_connection_string(
                connection_string,
                retry_policy=None  # SDK handles retries by default
            )
            logger.info("✓ Blob Service Client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Blob Service Client: {e}")
            raise
    
    def _ensure_container_exists(self, container_name: str) -> ContainerClient:
        """Ensure the container exists, creating it if necessary."""
        try:
            container_client = self._blob_service_client.get_container_client(container_name)
            
            try:
                container_client.create_container()
                logger.info(f"✓ Container '{container_name}' created successfully")
            except ResourceExistsError:
                logger.debug(f"Container '{container_name}' already exists")
            
            return container_client
        except AzureError as e:
            logger.error(f"Azure error while accessing container '{container_name}': {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while ensuring container exists: {e}")
            raise
    
    def _generate_sas_url(self, container_name: str, blob_name: str, expiration_hours: int = 24) -> Optional[str]:
        """
        Generate a SAS URL for the blob.
        
        Args:
            container_name: The container name
            blob_name: The blob name
            expiration_hours: Hours until SAS URL expires (default: 24)
            
        Returns:
            A valid SAS URL for accessing the blob, or None if generation fails
        """
        try:
            account_name = Config.get("AZURE_STORAGE_STORAGE_NAME")
            account_key = Config.get("AZURE_STORAGE_API_KEY")
            
            if not account_name or not account_key:
                logger.warning("SAS URL generation requires AZURE_STORAGE_STORAGE_NAME and AZURE_STORAGE_API_KEY")
                return None
            
            # Generate SAS token
            sas_token = generate_blob_sas(
                account_name=account_name,
                container_name=container_name,
                blob_name=blob_name,
                account_key=account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=expiration_hours)
            )
            
            # Construct full SAS URL
            sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
            logger.info(f"✓ SAS URL generated for '{blob_name}' (expires in {expiration_hours}h)")
            return sas_url
            
        except ValueError as e:
            logger.warning(f"Cannot generate SAS URL: {e}")
            return None
        except Exception as e:
            logger.error(f"Error generating SAS URL: {e}")
            return None
    
    def _get_direct_url(self, account_name: str, container_name: str, blob_name: str) -> str:
        """
        Get direct blob URL (for public containers).
        
        Args:
            account_name: Storage account name
            container_name: Container name
            blob_name: Blob name
            
        Returns:
            Direct blob URL
        """
        return f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    
    def upload_file_to_blob(self, file, blob_name: str, use_sas: bool = True) -> Optional[str]:
        """
        Upload a file to Azure Blob Storage with optional SAS URL generation.
        
        Follows Azure SDK best practices:
        - Reuses singleton client connection for better throughput
        - Handles Azure errors gracefully with proper logging
        - Returns SAS URL for secure, temporary access (recommended for production)
        
        Args:
            file: The file object to upload
            blob_name: The name of the blob in storage
            use_sas: Generate SAS URL (default: True for security)
            
        Returns:
            A valid URL for accessing the blob, or None if upload fails
        """
        try:
            if not file or not blob_name:
                raise ValueError("File and blob_name are required")
            
            container_name = Config.get("AZURE_STORAGE_CONTAINER_NAME")
            account_name = Config.get("AZURE_STORAGE_STORAGE_NAME")
            
            if not container_name or not account_name:
                raise ValueError("Container and account name are required")
            
            # Ensure container exists
            container_client = self._ensure_container_exists(container_name)
            
            # Reset file pointer to beginning
            file.seek(0)
            
            # Get blob client and upload
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(file, overwrite=True)
            
            # Verify blob exists after upload
            blob_properties = blob_client.get_blob_properties()
            
            logger.info(
                f"✓ File '{blob_name}' uploaded successfully\n"
                f"  Size: {blob_properties.size} bytes"
            )
            
            # Return appropriate URL based on configuration
            if use_sas:
                sas_url = self._generate_sas_url(container_name, blob_name)
                if sas_url:
                    return sas_url
                else:
                    logger.warning("SAS generation failed, falling back to direct URL")
            
            # Fallback: return direct URL
            direct_url = self._get_direct_url(account_name, container_name, blob_name)
            logger.info(f"Using direct blob URL: {direct_url}")
            return direct_url
            
        except ValueError as e:
            error_msg = f"Configuration error: {e}"
            logger.error(error_msg)
            st.error(error_msg)
            return None
        except AzureError as e:
            error_msg = f"Azure error during file upload: {e}"
            logger.error(error_msg)
            st.error(error_msg)
            return None
        except Exception as e:
            error_msg = f"Unexpected error uploading file to Blob Storage: {e}"
            logger.error(error_msg)
            st.error(error_msg)
            return None


# Create singleton instance
_blob_service = BlobStorageService()

def upload_file_to_blob(file, blob_name: str, use_sas: bool = True) -> Optional[str]:
    """
    Wrapper function to upload file to blob storage.
    
    Uses singleton pattern to reuse client connection (Azure SDK best practice).
    """
    return _blob_service.upload_file_to_blob(file, blob_name, use_sas)