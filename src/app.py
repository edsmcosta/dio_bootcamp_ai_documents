import logging
import streamlit as st
from typing import Optional, Dict, Any
from services.blob_service import upload_file_to_blob
from services.document_service import analyze_credit_card_image
from utils.Config import DEBUG

# Configure logging based on DEBUG flag
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Streamlit page configuration
st.set_page_config(
    page_title="DIO BootCamp - Document Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS for better styling
st.markdown("""
    <style>
    .header-title {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .success-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .error-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .info-card {
        padding: 15px;
        border-radius: 8px;
        background-color: #e7f3ff;
        border-left: 4px solid #0066cc;
        margin: 10px 0;
    }
    .validation-valid {
        color: #28a745;
        font-weight: bold;
    }
    .validation-invalid {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def validate_credit_card_field(field_value: Any, field_name: str) -> bool:
    """
    Validate if a credit card field is present and not empty.
    
    Args:
        field_value: The field value to validate
        field_name: Name of the field for logging
        
    Returns:
        bool: True if field is valid, False otherwise
    """
    is_valid = field_value is not None and str(field_value).strip() != ""
    
    if not is_valid:
        logger.debug(f"Field validation failed for: {field_name}")
    
    return is_valid

def render_field_validation(
    field_name: str,
    field_value: Optional[str],
    field_display_name: str
) -> None:
    """
    Render a single credit card field with validation status.
    
    Args:
        field_name: Internal field name (for logging)
        field_value: The field value to display
        field_display_name: User-friendly field name
    """
    is_valid = validate_credit_card_field(field_value, field_name)
    
    if is_valid:
        st.markdown(
            f"<p><span class='validation-valid'>✓ {field_display_name}</span>: {field_value}</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<p><span class='validation-invalid'>✗ {field_display_name}</span>: Não detectado</p>",
            unsafe_allow_html=True
        )

def show_image_and_validation(blob_url: str, credit_card_info: Dict[str, Any]) -> None:
    """
    Display the uploaded credit card image and extracted information with validation.
    
    Args:
        blob_url: URL of the uploaded image in Azure Blob Storage
        credit_card_info: Dictionary containing extracted credit card fields
    """
    try:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📸 Imagem do Cartão")
            st.image(blob_url, caption="Cartão de crédito enviado", width='content')
        
        with col2:
            st.subheader("✅ Validação das Informações")
            
            if credit_card_info:
                # Count valid fields
                valid_fields = sum(
                    1 for value in credit_card_info.values()
                    if validate_credit_card_field(value, "")
                )
                total_fields = len(credit_card_info)
                
                st.markdown(f"<div class='info-card'>Campos detectados: {valid_fields}/{total_fields}</div>",
                           unsafe_allow_html=True)
                
                # Display individual fields
                render_field_validation(
                    "CardHolderName",
                    credit_card_info.get("CardHolderName"),
                    "Nome do Titular"
                )
                render_field_validation(
                    "CardNumber",
                    credit_card_info.get("CardNumber"),
                    "Número do Cartão"
                )
                render_field_validation(
                    "ExpirationDate",
                    credit_card_info.get("ExpirationDate"),
                    "Data de Validade"
                )
                render_field_validation(
                    "CardVerificationValue",
                    credit_card_info.get("CardVerificationValue"),
                    "CVV/CVC"
                )
                render_field_validation(
                    "PaymentNetwork",
                    credit_card_info.get("PaymentNetwork"),
                    "Bandeira"
                )
                render_field_validation(
                    "IssuingBank",
                    credit_card_info.get("IssuingBank"),
                    "Banco Emissor"
                )
                
                # Overall validation status
                st.divider()
                if valid_fields == total_fields:
                    st.markdown(
                        "<div class='success-box'><strong>✓ Cartão validado com sucesso!</strong></div>",
                        unsafe_allow_html=True
                    )
                    logger.info(f"Credit card validation successful. Fields detected: {valid_fields}/{total_fields}")
                else:
                    st.markdown(
                        f"<div class='info-card'><strong>⚠️  Cartão parcialmente validado.</strong> {valid_fields}/{total_fields} campos detectados.</div>",
                        unsafe_allow_html=True
                    )
                    logger.warning(f"Partial validation. Fields detected: {valid_fields}/{total_fields}")
            else:
                st.markdown(
                    "<div class='error-box'><strong>✗ Nenhuma informação de cartão detectada.</strong><br/>Por favor, verifique a qualidade da imagem e tente novamente.</div>",
                    unsafe_allow_html=True
                )
                logger.warning("No credit card information detected in image")
    
    except Exception as e:
        logger.error(f"Error rendering validation display: {e}", exc_info=True)
        st.error("❌ Erro ao processar as informações do cartão.")

def configure_interface() -> None:
    """
    Configure and render the main Streamlit interface for credit card analysis.
    """
    try:
        # Header
        st.markdown("<h1 class='header-title'>🏦 DIO BootCamp - Análise de Documentos Azure</h1>",
                   unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Análise de cartões de crédito usando Azure Document Intelligence</p>",
                   unsafe_allow_html=True)
        
        st.divider()
        
        # Sidebar
        with st.sidebar:
            st.header("ℹ️ Informações")
            st.markdown("""
            **Como usar:**
            1. Faça upload de uma imagem de cartão de crédito
            2. O sistema analisará automaticamente
            3. As informações serão validadas
            
            **Formatos suportados:** PNG, JPG, JPEG
            
            **Nota:** As imagens são processadas de forma segura usando Azure Document Intelligence.
            """)
            
            if DEBUG:
                st.warning("🐛 Modo DEBUG ativado")
        
        # File uploader
        st.subheader("📤 Enviar Cartão de Crédito")
        uploaded_file = st.file_uploader(
            "Selecione uma imagem do cartão de crédito",
            type=["png", "jpg", "jpeg"],
            help="Envie uma imagem clara e de boa qualidade do cartão"
        )
        
        if uploaded_file is not None:
            try:
                file_name = uploaded_file.name
                
                with st.spinner("📤 Enviando arquivo para Azure Blob Storage..."):
                    blob_url = upload_file_to_blob(uploaded_file, file_name)
                
                if blob_url:
                    st.markdown(
                        f"<div class='success-box'>✓ Arquivo <strong>{file_name}</strong> enviado com sucesso!</div>",
                        unsafe_allow_html=True
                    )
                    logger.info(f"File uploaded successfully: {file_name}")
                    
                    with st.spinner("🔍 Analisando cartão de crédito..."):
                        credit_card_info = analyze_credit_card_image(blob_url)
                    
                    if credit_card_info:
                        st.success("✓ Análise concluída!")
                        logger.info("Credit card analysis completed successfully")
                    
                    show_image_and_validation(blob_url, credit_card_info)
                else:
                    st.markdown(
                        f"<div class='error-box'>✗ Erro ao enviar arquivo <strong>{file_name}</strong> para Azure Blob Storage.<br/>Por favor, tente novamente.</div>",
                        unsafe_allow_html=True
                    )
                    logger.error(f"Failed to upload file: {file_name}")
            
            except Exception as e:
                logger.error(f"Error processing file: {e}", exc_info=True)
                st.error(f"❌ Erro ao processar arquivo: {str(e)}")
    
    except Exception as e:
        logger.critical(f"Critical error in configure_interface: {e}", exc_info=True)
        st.error("❌ Erro crítico na aplicação. Por favor, contate o suporte.")

if __name__ == "__main__":
    configure_interface()