# CISO Agent - Phishing Detection MCP Server

Chief Information Security Officer agent server designed to help any agent prevent phishing attacks using AI-powered security analysis.

## Overview

This MCP (Model Context Protocol) server provides a phishing detection tool that analyzes URLs using RAG (Retrieval Augmented Generation) with cybersecurity training materials from CISA. It returns a JSON assessment with risk analysis and recommendations.

## Features

- **URL Security Assessment**: Analyzes URLs for phishing and security threats
- **RAG-Powered**: Uses CISA phishing training materials for context-aware analysis
- **Risk Scoring**: Provides probability scores (0.0-1.0) and binary recommendations
- **MCP Compatible**: Works with Claude Desktop, Cline, and other MCP clients

## Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jomilu93/ciso-agent.git
cd ciso-agent
```

2. Install dependencies:
```bash
pip install -e .
# or
pip install -r requirements.txt
```

3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### As MCP Server

Run the server in stdio mode:
```bash
python main.py
```

Or use FastMCP dev mode for testing:
```bash
fastmcp dev main.py
```

### Test Mode

Test the tool directly from command line:
```bash
python main.py test https://example.com
```

### Configure in Claude Desktop

Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "ciso-agent": {
      "command": "python",
      "args": ["/path/to/ciso-agent/main.py"],
      "env": {
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Tool Interface

### CISO Agent - Phishing

**Input:**
- `url` (string): The URL to analyze for phishing/security threats

**Output:**
- JSON string with:
  - `risk_assessment` (string): Detailed analysis of the URL
  - `risk_probability` (float): 0.0 (safe) to 1.0 (malicious)
  - `recommendation` (int): 0 (safe to click) or 1 (don't click)

**Example:**
```json
{
  "risk_assessment": "Domain analysis shows legitimate structure...",
  "risk_probability": 0.15,
  "recommendation": 0
}
```

## Architecture

- **FastMCP**: MCP server framework with lifespan management
- **LangChain**: RAG orchestration and document processing
- **OpenAI**: Embeddings (text-embedding-ada-002) and LLM (GPT-4o-mini)
- **FAISS**: Vector similarity search for document retrieval
- **Knowledge Base**: CISA phishing training PDF (included)

## Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key for embeddings and LLM

## Development

### Project Structure

```
ciso-agent/
├── main.py                          # MCP server entry point
├── ciso_rag.py                      # RAG setup and vectorstore initialization
├── ciso_prompts.py                  # Prompt templates
├── CISO_Knowledge_Base/
│   └── CISA_Phising_Training.pdf   # Security training knowledge base
├── pyproject.toml                   # Project metadata and dependencies
├── requirements.txt                 # Pip requirements
└── README.md                        # This file
```

### Testing

Run syntax checks:
```bash
python -m py_compile main.py ciso_rag.py ciso_prompts.py
```

Test with a URL:
```bash
python main.py test www.google.com
```

## Deployment

### FastMCP Cloud

1. Ensure all changes are committed
2. Push to main branch
3. Deploy via FastMCP Cloud dashboard
4. Set `OPENAI_API_KEY` environment variable in cloud settings

### Requirements

- All dependencies are specified in `pyproject.toml`
- Python 3.10+ runtime
- OpenAI API key configured as environment variable

## Authors

- Jose Miguel Luna (jlunamugica26@gsb.columbia.edu)
- Ron Litvak (rlitvak26@gsb.columbia.edu)

## License

[Add your license here]

## Version

0.1.0
