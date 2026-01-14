import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass

class Config:
    """Load and access environment variables with validation and error handling."""
    
    # Define required and optional environment variables
    REQUIRED_VARS = {
        "AZURE_DOCS_API_KEY": "Azure Document Intelligence API Key",
        "AZURE_DOCS_ENDPOINT": "Azure Document Intelligence Endpoint",
        "AZURE_DOCS_REGION": "Azure Document Intelligence Region",
        "AZURE_STORAGE_CONN_STRING": "Azure Storage Connection String",
        "AZURE_STORAGE_CONTAINER_NAME": "Azure Storage Container Name",
    }
    
    OPTIONAL_VARS = {
        "AZURE_STORAGE_STORAGE_NAME": "Azure Storage Account Name",
        "AZURE_STORAGE_API_KEY": "Azure Storage API Key",
        "DEBUG": "Enable debug mode",
    }
    
    _instance: Optional['Config'] = None
    _is_initialized: bool = False
    
    def __new__(cls):
        """Implement singleton pattern for configuration."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize and validate configuration on first instantiation."""
        if not Config._is_initialized:
            self._load_environment()
            Config._is_initialized = True
    
    def _load_environment(self) -> None:
        """Load environment variables from .env file."""
        try:
            # Calculate project root path (3 levels up from src/utils/)
            project_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '../..')
            )
            env_path = os.path.join(project_root, '.env')
            
            # Validate file existence
            if not os.path.exists(env_path):
                raise ConfigurationError(
                    f"❌ .env file not found at {env_path}\n"
                    f"📁 Expected location: {env_path}"
                )
            
            # Load environment variables
            if not load_dotenv(env_path):
                logger.warning(f"⚠️  Failed to load .env from {env_path}")
                return
            
            logger.info(f"✓ .env loaded successfully from {env_path}")
            self._validate_configuration()
            
        except ConfigurationError as e:
            logger.error(str(e))
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error loading configuration: {e}")
            raise ConfigurationError(f"Configuration loading failed: {e}")
    
    def _validate_configuration(self) -> None:
        """Validate that all required environment variables are loaded."""
        missing_required = []
        missing_optional = []
        
        # Check required variables
        for var_name, var_description in self.REQUIRED_VARS.items():
            if not os.getenv(var_name):
                missing_required.append(f"  • {var_name}: {var_description}")
        
        # Check optional variables
        for var_name, var_description in self.OPTIONAL_VARS.items():
            if not os.getenv(var_name):
                missing_optional.append(f"  • {var_name}: {var_description}")
        
        # Report missing required variables
        if missing_required:
            error_msg = "❌ Missing required environment variables:\n" + "\n".join(missing_required)
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
        
        # Warn about missing optional variables
        if missing_optional:
            warning_msg = "⚠️  Missing optional environment variables:\n" + "\n".join(missing_optional)
            logger.warning(warning_msg)
        
        logger.info("✓ All required environment variables loaded successfully")
    
    @staticmethod
    def get(key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get an environment variable.
        
        Args:
            key: The environment variable name
            default: Default value if variable is not found
            
        Returns:
            The environment variable value or default
        """
        value = os.getenv(key, default)
        if value is None:
            logger.debug(f"Environment variable '{key}' not found")
        return value
    
    @staticmethod
    def get_int(key: str, default: Optional[int] = None) -> Optional[int]:
        """
        Get an environment variable as integer.
        
        Args:
            key: The environment variable name
            default: Default value if variable is not found or invalid
            
        Returns:
            The environment variable value as int or default
        """
        try:
            value = os.getenv(key)
            return int(value) if value else default
        except ValueError:
            logger.warning(f"Environment variable '{key}' is not a valid integer")
            return default
    
    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """
        Get an environment variable as boolean.
        
        Args:
            key: The environment variable name
            default: Default value if variable is not found
            
        Returns:
            The environment variable value as bool or default
        """
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    @classmethod
    def is_debug_enabled(cls) -> bool:
        """Check if debug mode is enabled."""
        return cls.get_bool("DEBUG", False)


# Initialize configuration singleton
try:
    _config = Config()
    
    # Export environment variables as module-level constants
    AZURE_DOCS_API_KEY = Config.get("AZURE_DOCS_API_KEY")
    AZURE_DOCS_ENDPOINT = Config.get("AZURE_DOCS_ENDPOINT")
    AZURE_DOCS_REGION = Config.get("AZURE_DOCS_REGION")
    AZURE_STORAGE_STORAGE_NAME = Config.get("AZURE_STORAGE_STORAGE_NAME")
    AZURE_STORAGE_API_KEY = Config.get("AZURE_STORAGE_API_KEY")
    AZURE_STORAGE_CONN_STRING = Config.get("AZURE_STORAGE_CONN_STRING")
    AZURE_STORAGE_CONTAINER_NAME = Config.get("AZURE_STORAGE_CONTAINER_NAME")
    DEBUG = Config.is_debug_enabled()
    
except ConfigurationError as e:
    logger.critical(f"Configuration initialization failed: {e}")
    raise