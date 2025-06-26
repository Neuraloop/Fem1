# Overview

Fem-MultiModel is a web-based Finite Element Analysis (FEA) problem-solving application that leverages multiple AI models to provide comprehensive solutions. The application uses Flask as the web framework and integrates with Google's Gemini AI models through LangChain to solve complex FEA problems with high accuracy.

# System Architecture

## Frontend Architecture
- **Web Interface**: Flask-based web application with Bootstrap 5 for responsive UI
- **Interactive UI**: Space-themed design with animated elements and real-time problem input
- **Client-side Logic**: JavaScript-based frontend application (`FemMultiModel` class) for handling user interactions
- **Template Engine**: Jinja2 templates for server-side rendering

## Backend Architecture
- **Web Framework**: Flask with SQLAlchemy ORM for database operations
- **AI Integration**: LangChain framework with LangGraph for orchestrating AI model workflows
- **Model Management**: Support for multiple Gemini models (gemini-1.5-flash, gemini-2.0-flash-exp)
- **Session Management**: Flask sessions for user state management
- **API Management**: Secure storage and management of AI model API keys

## Database Schema
The application uses SQLAlchemy with the following models:
- **APIKey**: Stores encrypted API keys for different AI services
- **ChatSession**: Tracks user problem-solving sessions and responses
- **Future Models**: Template structure for expandable model support (ModelResponse, SupportedModel)

# Key Components

## FEM Solver Engine (`fem_solver.py`)
- **Multi-Model Approach**: Utilizes multiple Gemini models for cross-validation
- **Workflow Orchestration**: LangGraph-based state management for complex problem-solving pipelines
- **Expert System Prompting**: Specialized prompts designed for FEA engineering expertise
- **Response Synthesis**: Combines multiple model outputs for enhanced accuracy

## API Key Management
- **Secure Storage**: Database-backed API key storage with encryption
- **Multi-Service Support**: Extensible architecture for multiple AI providers
- **User Interface**: Web-based configuration interface for API key management

## Web Routes (`routes.py`)
- **Problem Solving Endpoint**: `/solve` for processing FEA problems
- **Profile Management**: `/profile` for API key configuration
- **CRUD Operations**: Complete API key lifecycle management

# Data Flow

1. **User Input**: User submits FEA problem through web interface
2. **API Key Retrieval**: System retrieves stored Gemini API key
3. **Multi-Model Processing**: Problem is processed by multiple Gemini models simultaneously
4. **Response Synthesis**: Individual model responses are combined and refined
5. **Result Display**: Final solution is presented to user with formatting
6. **Session Storage**: Problem and responses are stored for future reference

# External Dependencies

## AI/ML Services
- **Google Gemini**: Primary AI models for FEA problem solving
  - gemini-1.5-flash (fast processing)
  - gemini-2.0-flash-exp (advanced reasoning)
- **Future Integration**: Architecture supports OpenAI, Anthropic Claude, and other providers

## Core Libraries
- **Flask**: Web framework and application structure
- **SQLAlchemy**: Database ORM and model management
- **LangChain**: AI model integration and prompt management
- **LangGraph**: Workflow orchestration and state management
- **Gunicorn**: Production WSGI server

## Frontend Libraries
- **Bootstrap 5**: Responsive UI framework
- **Feather Icons**: Icon library for UI elements
- **Google Fonts**: Custom typography (Orbitron, Rajdhani)

# Deployment Strategy

## Container Configuration
- **Environment**: Python 3.11 with Nix package management
- **Database**: PostgreSQL support with automatic fallback to SQLite
- **Process Management**: Gunicorn with autoscaling deployment target
- **Port Configuration**: Application serves on port 5000 with automatic port detection

## Production Settings
- **WSGI Server**: Gunicorn with reuse-port and reload capabilities
- **Proxy Support**: ProxyFix middleware for reverse proxy compatibility
- **Session Security**: Environment-based secret key management
- **Database Optimization**: Connection pooling and pre-ping health checks

## Environment Variables
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `SESSION_SECRET`: Flask session encryption key
- `GEMINI_API_KEY`: Google Gemini API authentication

# User Preferences

Preferred communication style: Simple, everyday language.

# Changelog

Changelog:
- June 26, 2025. Initial setup