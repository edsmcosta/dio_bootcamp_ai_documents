# 🏦 DIO BootCamp - Document Intelligence Azure

Aplicação Streamlit para análise automatizada de cartões de crédito utilizando **Azure Document Intelligence** e **Azure Blob Storage**, seguindo as melhores práticas de arquitetura cloud-native.

## 📋 Tabela de Conteúdos

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Recursos](#recursos)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Padrões e Boas Práticas](#padrões-e-boas-práticas)
- [Documentação de Componentes](#documentação-de-componentes)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)

---

## 🎯 Visão Geral

Este projeto implementa uma solução completa para análise de documentos (cartões de crédito) na nuvem Azure, combinando:

- **Azure Document Intelligence**: Reconhecimento óptico de caracteres (OCR) e extração estruturada
- **Azure Blob Storage**: Armazenamento seguro com SAS URLs
- **Streamlit**: Interface web responsiva e intuitiva
- **Python 3.10**: Backend com type hints e logging profissional

**Caso de Uso Principal**: Validação e extração de dados de cartões de crédito para sistemas financeiros com conformidade PCI-DSS.

---

## 🏗️ Arquitetura

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend (app.py)              │
│  - File Upload Interface                                    │
│  - Real-time Validation & Visualization                     │
│  - Responsive UI with CSS Styling                           │
└────────────────┬────────────────────────────────────────────┘
                 │
     ┌───────────┴───────────┐
     │                       │
     ▼                       ▼
┌──────────────┐      ┌──────────────────┐
│ BlobService  │      │ DocumentService  │
│ - Upload     │      │ - Analyze        │
│ - SAS URLs   │      │ - Extract        │
│ - Security   │      │ - Validation     │
└──────┬───────┘      └────────┬─────────┘
       │                       │
       ▼                       ▼
┌──────────────────┐   ┌──────────────────┐
│  Azure Blob      │   │  Azure Document  │
│  Storage         │   │  Intelligence    │
│  - Secure Store  │   │  - prebuilt-     │
│  - SAS Auth      │   │    creditCard    │
└──────────────────┘   └──────────────────┘
       ▲                       ▲
       │                       │
       └───────────┬───────────┘
                   │
            ┌──────▼──────┐
            │  Config.py  │
            │  - .env     │
            │  - Secrets  │
            └─────────────┘
```

### Fluxo de Dados

```
1. User Upload
   ↓
2. File → Blob Storage (SAS URL)
   ↓
3. Document Intelligence API
   ↓
4. Extract & Validate Fields
   ↓
5. Display Results (UI)
```

---

## ✨ Recursos

### Funcionalidades Principais

- ✅ **Upload de Imagens**: Suporte para PNG, JPG, JPEG
- ✅ **Análise Automática**: Extração de dados de cartão via Azure Document Intelligence
- ✅ **Validação em Tempo Real**: Feedback visual imediato
- ✅ **Armazenamento Seguro**: SAS URLs com expiração configurável
- ✅ **Logging Profissional**: Rastreamento completo de operações
- ✅ **Interface Responsiva**: Design moderno com Streamlit

### Campos Extraídos

| Campo | Descrição | Validação |
|-------|-----------|-----------|
| `CardHolderName` | Nome do titular | ✓ Obrigatório |
| `CardNumber` | Número do cartão | ✓ Obrigatório |
| `ExpirationDate` | Data de validade | ✓ Obrigatório |
| `CardVerificationValue` | CVV/CVC | ✓ Opcional |
| `PaymentNetwork` | Bandeira (Visa, MC, Amex) | ✓ Opcional |
| `IssuingBank` | Banco emissor | ✓ Opcional |

---

## 📦 Pré-requisitos

### Requisitos do Sistema

- **Python**: 3.10+
- **Sistema Operacional**: Windows, macOS, Linux
- **Memória**: Mínimo 2GB RAM
- **Conexão**: Internet para acesso aos serviços Azure

### Serviços Azure Necessários

1. **Azure Document Intelligence**
   - Recurso criado na região `eastus` (recomendado)
   - API Key e Endpoint configurados

2. **Azure Storage Account**
   - Conta de armazenamento criada
   - Container `cartoes` (ou personalizado)
   - Connection String e API Key

### Credenciais

Solicite ao administrador:
- `AZURE_DOCS_API_KEY`
- `AZURE_DOCS_ENDPOINT`
- `AZURE_STORAGE_CONN_STRING`
- `AZURE_STORAGE_API_KEY`

---

## 🚀 Instalação

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/dio_bootcamp_ai_documents.git
cd dio_bootcamp_ai_documents
```

### 2. Criar Ambiente Virtual (Python 3.10)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3.10 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r dio_bootcamp_ai_documents/src/requirements.txt
```

### 4. Verificar Instalação

```bash
python --version  # Deve exibir 3.10.x
pip list | grep -E "streamlit|azure"
```

---

## ⚙️ Configuração

### 1. Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```bash
# filepath: .env

# Azure Document Intelligence
AZURE_DOCS_API_KEY="seu-api-key-aqui"
AZURE_DOCS_ENDPOINT="https://seu-endpoint.cognitiveservices.azure.com/"
AZURE_DOCS_REGION="eastus"

# Azure Storage Account
AZURE_STORAGE_STORAGE_NAME="seustorageaccount"
AZURE_STORAGE_API_KEY="sua-api-key-aqui"
AZURE_STORAGE_CONN_STRING="DefaultEndpointsProtocol=https;AccountName=...;..."
AZURE_STORAGE_CONTAINER_NAME="cartoes"

# Aplicação
DEBUG=false
USE_SAS_URLS=true
SAS_EXPIRATION_HOURS=24
```

### 2. Validar Configuração

```bash
cd dio_bootcamp_ai_documents/src
python -c "from utils.Config import Config; print('✓ Config loaded successfully')"
```

**Saída esperada:**
```
✓ .env loaded successfully from ...
✓ All required environment variables loaded successfully
✓ Config loaded successfully
```

---

## 💻 Uso

### Execução Local

```bash
# Navegue até o diretório do projeto
cd dio_bootcamp_ai_documents

# Execute a aplicação Streamlit
streamlit run src/app.py
```

**A aplicação abrirá em:**
```
http://localhost:8501
```

### Interface da Aplicação

1. **Sidebar (Esquerda)**
   - Instruções de uso
   - Status de modo DEBUG

2. **Área Principal**
   - Upload de arquivo (drag & drop)
   - Spinner de processamento
   - Imagem do cartão
   - Validação de campos

3. **Relatório de Validação**
   - Status de cada campo (✓/✗)
   - Contagem de campos detectados
   - Status geral do cartão

### Exemplo de Fluxo

```
1. Clique em "Selecione uma imagem do cartão de crédito"
2. Selecione um arquivo PNG/JPG
3. Aguarde o processamento (spinner)
4. Visualize a imagem e os resultados
5. Verifique o status de validação
```

---

## 📁 Estrutura do Projeto

```
dio_bootcamp_ai_documents/
├── .env                              # Variáveis de ambiente (⚠️ não commitir)
├── .gitignore                        # Arquivos ignorados
├── README.md                         # Este arquivo
├── requirements.txt                  # Dependências Python
│
├── dio_bootcamp_ai_documents/
│   ├── src/
│   │   ├── app.py                   # 🎯 Aplicação Streamlit principal
│   │   │
│   │   ├── services/
│   │   │   ├── blob_service.py      # Gerenciamento Azure Blob Storage
│   │   │   ├── document_service.py  # Análise Azure Document Intelligence
│   │   │   └── __init__.py
│   │   │
│   │   ├── utils/
│   │   │   ├── Config.py            # Gerenciamento de configurações
│   │   │   └── __init__.py
│   │   │
│   │   ├── requirements.txt         # Dependências específicas
│   │   └── __init__.py
│   │
│   └── tests/                        # Testes unitários (futuro)
│       └── __init__.py
│
└── .vscode/
    └── launch.json                   # Configuração de debug VS Code
```

---

## 🎨 Padrões e Boas Práticas

### 1. Padrão Singleton

**Aplicado em:** `BlobStorageService`, `Config`

```python
class BlobStorageService:
    _instance: Optional['BlobStorageService'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_client()
        return cls._instance
```

**Benefícios:**
- ✅ Reutiliza conexão Azure SDK (melhor throughput)
- ✅ Reduz overhead de inicialização
- ✅ Thread-safe no Streamlit

### 2. Type Hints

**Aplicado em:** Todas as funções

```python
def upload_file_to_blob(file, blob_name: str, use_sas: bool = True) -> Optional[str]:
    """Type hints melhoram legibilidade e detectam bugs."""
```

**Benefícios:**
- ✅ Melhor autocompletar em IDEs
- ✅ Detecção estática de erros
- ✅ Documentação inline

### 3. Logging Estruturado

**Aplicado em:** Todos os módulos

```python
import logging

logger = logging.getLogger(__name__)

logger.info("✓ Operação concluída")
logger.warning("⚠️  Aviso importante")
logger.error("❌ Erro crítico")
```

**Benefícios:**
- ✅ Rastreamento de operações
- ✅ Debugging facilitado
- ✅ Monitoramento em produção

### 4. Tratamento de Exceções

**Padrão:** Try/Catch com logging e fallback

```python
try:
    # Operação principal
    sas_url = self._generate_sas_url(container_name, blob_name)
except ValueError as e:
    logger.error(f"Erro de configuração: {e}")
    # Fallback para URL direta
    return self._get_direct_url(account_name, container_name, blob_name)
except Exception as e:
    logger.error(f"Erro inesperado: {e}", exc_info=True)
    return None
```

### 5. Configuração via Ambiente

**Aplicado em:** `Config.py`

```python
# Carregamento seguro de secrets
AZURE_DOCS_API_KEY = Config.get("AZURE_DOCS_API_KEY")

# Com valores padrão
DEBUG = Config.get_bool("DEBUG", False)

# Validação obrigatória
if not api_key:
    raise ConfigurationError("API key not configured")
```

**Benefícios:**
- ✅ Secrets não no código
- ✅ Configuração por ambiente
- ✅ Fácil para containers/K8s

### 6. Modularização de Serviços

**Separação de responsabilidades:**

| Módulo | Responsabilidade |
|--------|-----------------|
| `app.py` | UI e orquestração |
| `blob_service.py` | Interação Azure Blob Storage |
| `document_service.py` | Análise de documentos |
| `Config.py` | Gerenciamento de configuração |

---

## 📚 Documentação de Componentes

### `app.py` - Interface Streamlit

**Principais Funções:**

```python
def validate_credit_card_field(field_value: Any, field_name: str) -> bool:
    """Valida se um campo do cartão é válido."""

def render_field_validation(field_name: str, field_value: Optional[str], 
                           field_display_name: str) -> None:
    """Renderiza um campo com status de validação."""

def show_image_and_validation(blob_url: str, 
                             credit_card_info: Dict[str, Any]) -> None:
    """Exibe imagem e resultados da validação."""

def configure_interface() -> None:
    """Configura a interface Streamlit principal."""
```

### `blob_service.py` - Gerenciamento de Storage

**Principais Métodos:**

| Método | Descrição | Retorno |
|--------|-----------|---------|
| `upload_file_to_blob()` | Upload com SAS ou URL direta | `str` (URL) |
| `_generate_sas_url()` | Gera URL com assinatura | `Optional[str]` |
| `_get_direct_url()` | URL direta (público) | `str` |
| `_ensure_container_exists()` | Cria container se necessário | `ContainerClient` |

**Exemplo de Uso:**

```python
from services.blob_service import upload_file_to_blob

# Upload com SAS URL (recomendado)
blob_url = upload_file_to_blob(file_object, "cartao.jpg", use_sas=True)

# Fallback para URL direta
blob_url = upload_file_to_blob(file_object, "cartao.jpg", use_sas=False)
```

### `document_service.py` - Análise de Documentos

**Principais Funções:**

```python
def analyze_credit_card_image(blob_url: str) -> dict:
    """Analisa imagem de cartão e extrai campos."""

def _extract_fields_from_result(result) -> dict:
    """Extrai campos estruturados do resultado."""
```

**Campos Retornados:**

```python
{
    "CardHolderName": "JOHN DOE",
    "CardNumber": "4532 XXXX XXXX 1234",
    "ExpirationDate": "12/25",
    "CardVerificationValue": "***",
    "PaymentNetwork": "Visa",
    "IssuingBank": "Bank Name"
}
```

### `Config.py` - Gerenciamento de Configuração

**API Pública:**

```python
# Obter string
api_key = Config.get("AZURE_DOCS_API_KEY")

# Obter com valor padrão
region = Config.get("AZURE_DOCS_REGION", "eastus")

# Obter inteiro
timeout = Config.get_int("TIMEOUT", 30)

# Obter booleano
debug = Config.get_bool("DEBUG", False)

# Verificar se debug está ativo
if Config.is_debug_enabled():
    print("Debug mode is on")
```

---

## 🐛 Troubleshooting

### Erro: `FileNotFoundError: [Errno 2] No such file or directory: '.env'`

**Solução:**
```bash
# Verifique se .env está na raiz do projeto
ls -la .env  # macOS/Linux
dir .env     # Windows

# Se não existir, crie:
touch .env  # macOS/Linux
type nul > .env  # Windows
```

### Erro: `AttributeError: module 'utils.Config' has no attribute 'get'`

**Solução:**
```python
# ❌ Errado
from utils import Config
Config.get("KEY")

# ✅ Correto
from utils.Config import Config
Config.get("KEY")
```

### Erro: `ResourceNotFound: The specified resource does not exist`

**Possíveis Causas:**
1. Container privado sem SAS URL válida
2. Arquivo não foi enviado corretamente
3. Credenciais inválidas

**Solução:**
```bash
# Verifique as credenciais no .env
grep AZURE_STORAGE .env

# Teste a conexão
python -c "from services.blob_service import _blob_service; print('✓ Connected')"
```

### Erro: `429: Request Rate Too Large`

**Explicação:** Limite de requisições atingido

**Solução:**
- Aguarde antes de novas requisições
- Aumente o número de RUs em produção
- Use retry-after logic (SDK já implementa)

---

## 🔒 Segurança

### Boas Práticas Implementadas

✅ **Secrets no `.env`** — Nunca no código  
✅ **SAS URLs** — Acesso temporário com expiração  
✅ **Type Hints** — Validação de tipos  
✅ **Logging Seguro** — Não expõe credenciais  
✅ **Exceção Customizada** — `ConfigurationError` para falhas claras  

### Para Produção

- [ ] Usar **Azure Key Vault** para secrets
- [ ] Habilitar **Managed Identity** em VMs/containers
- [ ] Configurar **SSL/TLS** para HTTPS
- [ ] Adicionar **autenticação** na API
- [ ] Implementar **rate limiting**
- [ ] Configurar **Azure Monitor** para logging

---

## 📈 Performance

### Otimizações Implementadas

| Otimização | Impacto | Detalhes |
|-----------|--------|----------|
| Singleton Pattern | Alta | Reutiliza conexão Azure SDK |
| SAS URLs | Média | Acesso sem autenticação repetida |
| Async/Await | Futura | Pronto para implementação |
| Batch Operations | Futura | Para múltiplos uploads |

### Benchmarks Esperados

- Upload: ~2-5s (depende do tamanho)
- Análise: ~3-8s (depende da complexidade)
- Validação: <1s

---

## 🧪 Testes

### Estrutura (Futura)

```python
# tests/test_config.py
def test_config_loads_env():
    assert Config.get("AZURE_DOCS_API_KEY") is not None

# tests/test_blob_service.py
def test_upload_file_generates_sas_url():
    url = upload_file_to_blob(test_file, "test.jpg", use_sas=True)
    assert "?sv=" in url  # SAS token presente

# tests/test_document_service.py
def test_analyze_credit_card_image():
    result = analyze_credit_card_image(test_blob_url)
    assert "CardNumber" in result
```

### Executar Testes

```bash
# Instalar pytest
pip install pytest pytest-asyncio

# Rodar testes
pytest tests/ -v
```

---

## 🎯 Roadmap

### v1.0 (Atual)
- ✅ Upload de imagens
- ✅ Análise de cartões de crédito
- ✅ Validação em tempo real
- ✅ SAS URLs seguras

### v1.1 (Próximo)
- [ ] Testes unitários completos
- [ ] Suporte para documentos adicionais (invoices, receipts)
- [ ] Dashboard de histórico
- [ ] Exportação de relatórios

### v2.0 (Futuro)
- [ ] API REST (FastAPI)
- [ ] Autenticação de usuários
- [ ] Azure Cosmos DB para persistência
- [ ] Vector Search para RAG
- [ ] Multi-tenancy

---

## 📞 Suporte

### Recursos

- [Azure Document Intelligence Docs](https://learn.microsoft.com/pt-br/azure/ai-services/document-intelligence/)
- [Azure Blob Storage Docs](https://learn.microsoft.com/pt-br/azure/storage/blobs/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [DIO Bootcamp](https://www.dio.me/)

### Contato

- **Issues**: GitHub Issues
- **Email**: ed.costa@emcdl.com.br
- **Discord**: Comunidade DIO

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** — veja o arquivo `LICENSE` para detalhes.

---

## 👥 Contribuidores

- **Ed Costa** — Desenvolvimento principal
- **DIO Bootcamp** — Mentoria e direcionamento

---

## 🙏 Agradecimentos

Agradecimentos especiais a:
- Microsoft Azure por fornecer ferramentas poderosas
- Comunidade DIO pelo suporte
- Você por usar este projeto!

---

**Última atualização:** Janeiro 14, 2026  
**Status:** ✅ Produção-Ready