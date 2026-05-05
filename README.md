# Smart Recruiter GenAI

## Overview

Smart Recruiter GenAI is an AI-powered resume screening and hiring system built with FastAPI. It leverages multi-agent architecture to intelligently route and evaluate candidates based on job requirements. The system integrates with vector databases for semantic search, supports multiple LLM providers (Ollama, Mistral), and provides a RESTful API for seamless integration.

## Features

- **Multi-Agent Architecture**: Specialized agents for parsing, routing, and evaluating resumes
- **AI-Powered Evaluation**: Uses LLMs to assess candidate fit for specific roles
- **Vector Search**: Qdrant integration for semantic similarity search on resumes
- **Resume Processing**: PDF parsing and text extraction capabilities
- **Database Integration**: MySQL for structured data, Qdrant for vector embeddings
- **RESTful API**: Comprehensive endpoints for candidates, jobs, evaluations, and interviews
- **Modular Design**: Clean separation of concerns with services, models, and schemas

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: MySQL (SQLAlchemy ORM)
- **Vector Database**: Qdrant
- **LLM Integration**: Ollama, Mistral AI
- **Embeddings**: Sentence Transformers
- **PDF Processing**: PyPDF
- **Other**: Pydantic for data validation, Uvicorn for ASGI server

## Prerequisites

- Python 3.8+
- MySQL Server
- Qdrant (running locally or remote)
- Ollama (for local LLM inference)
- Mistral API key (optional, for cloud LLM)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up databases**:
   - Ensure MySQL is running and create a database named `resume_ai`
   - Start Qdrant server (default: localhost:6333)

4. **Configure environment variables**:
   Create a `.env` file  with the following variables:
   ```env
   APP_NAME=AI Resume Screener
   APP_VERSION=1.0.0

   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_DB=resume_ai
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password

   QDRANT_HOST=localhost
   QDRANT_PORT=6333

   OLLAMA_MODEL=llama3
   OLLAMA_BASE_URL=http://localhost:11434

   MISTRAL_API_KEY=your_mistral_api_key
   MISTRAL_MODEL=mistral-large-latest
   ```

## Running the Application

1. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API**:
   - API Documentation: http://localhost:8000/docs (Swagger UI)
   - Root endpoint: http://localhost:8000/

## API Endpoints


For detailed API documentation, visit the Swagger UI at `/docs`.

## Project Structure

```
backend/
├── app/
│   ├── agents/          # AI agents for parsing, routing, evaluation
│   ├── api/             # API routes and router
│   ├── core/            # Configuration and constants
│   ├── db/              # Database initialization and connections
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic services
│   └── util/            # Utility functions
├── requirements.txt     # Python dependencies
└── uploads/             # File upload directory
    └── resumes/         # Resume storage
```

## Development

- **Code Style**: Follow PEP 8 guidelines
- **Testing**: Add unit tests in appropriate directories
- **Linting**: Use tools like flake8 or black for code quality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Copyright

© 2026 Anirban Das

Email: anirban.techlead@gmail.com  
Phone: +91 9038873072

## Support

For questions or issues, please open an issue in the repository or contact the development team.