import logging
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utils.Config import AZURE_DOCS_ENDPOINT, AZURE_DOCS_API_KEY

# Configure logging
logger = logging.getLogger(__name__)

def analyze_credit_card_image(blob_url: str) -> dict:
    """
    Analyze a credit card image from Azure Blob Storage using Document Intelligence.
    
    Extracts structured information from credit card documents using Azure's
    prebuilt credit card recognition model.
    
    Args:
        blob_url (str): The URL of the credit card image in Azure Blob Storage
        
    Returns:
        dict: Extracted credit card information with fields like:
            - CardHolderName: Name on the card
            - CardNumber: Card number
            - ExpirationDate: Expiration date
            - cvv: CVV/CVC code
            - PaymentNetwork: Card network (Visa, Mastercard, etc)
            
    Raises:
        Returns empty dict if analysis fails
    """
    try:
        if not blob_url:
            raise ValueError("blob_url is required")
        
        # Initialize Document Intelligence Client
        endpoint = AZURE_DOCS_ENDPOINT
        api_key = AZURE_DOCS_API_KEY
        
        if not endpoint or not api_key:
            raise ValueError("Azure Document Intelligence credentials not configured")
        
        credential = AzureKeyCredential(api_key)
        client = DocumentIntelligenceClient(endpoint=endpoint, credential=credential)
        
        logger.info(f"Analyzing credit card image from: {blob_url}")
        
        # Prepare analysis request
        model_id = "prebuilt-creditCard"
        analyze_request = AnalyzeDocumentRequest(url_source=blob_url)
        
        # Analyze document
        poller = client.begin_analyze_document(model_id, analyze_request)
        result = poller.result()
        
        # Extract credit card information
        credit_card_info = _extract_fields_from_result(result)
        
        if credit_card_info:
            logger.info(f"✓ Successfully extracted {len(credit_card_info)} fields from credit card")
        else:
            logger.warning("No credit card fields detected in image")
        
        return credit_card_info
    
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error analyzing document: {e}", exc_info=True)
        return {}

def _extract_fields_from_result(result) -> dict:
    """
    Extract fields from Azure Document Intelligence result.
    
    Args:
        result: The analysis result object from Document Intelligence
        
    Returns:
        dict: Extracted fields with their values
    """
    credit_card_info = {}
    
    try:
        # Check if result has documents
        if not hasattr(result, 'documents') or not result.documents:
            logger.debug("No documents found in analysis result")
            return credit_card_info
        
        # Process each document
        for document in result.documents:
            if not hasattr(document, 'fields') or not document.fields:
                logger.debug("Document has no fields")
                continue
            
            # Extract fields from document
            fields = document.fields
            
            # Iterate through fields (fields is a dict)
            for field_name, field_content in fields.items():
                try:
                    # field_content is an object with 'content' attribute
                    if hasattr(field_content, 'content') and field_content.content is not None:
                        credit_card_info[field_name] = field_content.content
                        logger.debug(f"Extracted field: {field_name} = {field_content.content}")
                    else:
                        logger.debug(f"Field '{field_name}' has no content")
                        
                except AttributeError as e:
                    logger.warning(f"Could not extract field '{field_name}': {e}")
                    continue
        
        return credit_card_info
        
    except Exception as e:
        logger.error(f"Error extracting fields: {e}")
        return {}