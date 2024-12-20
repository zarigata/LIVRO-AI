# AI Book Generator Setup Guide

## Prerequisites
- Python 3.9+
- Docker (optional but recommended)
- CUDA-capable GPU (recommended for faster image generation)

## Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-book-generator.git
cd ai-book-generator
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Ollama
- Download from [Ollama Official Website](https://ollama.ai/)
- Run: `ollama pull llama2`

### 5. Install Stable Diffusion
- Option 1: Use Hugging Face Diffusers (included in requirements)
- Option 2: Install [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

### 6. Run the Application
```bash
streamlit run src/web_app.py
```

## Docker Setup (Recommended)
```bash
docker-compose up --build
```

## Troubleshooting
- Ensure CUDA drivers are updated for GPU acceleration
- Check Ollama and Stable Diffusion model compatibility
- Verify all dependencies are correctly installed

## Configuration
Modify `src/book_generator_agent.py` and `src/image_generator.py` to customize:
- LLM Model
- Image Generation Parameters
- Workflow Logic

## Performance Tips
- Use a CUDA-capable GPU
- Allocate sufficient RAM (16GB+)
- Use latest GPU drivers
