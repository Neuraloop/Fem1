from app import db
from datetime import datetime

class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<APIKey {self.service_name}>'

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_description = db.Column(db.Text, nullable=False)
    gemini_15_response = db.Column(db.Text)
    gemini_25_response = db.Column(db.Text)
    final_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatSession {self.id}>'

# Template for future model extensions (commented out for now)
"""
class ModelResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id'), nullable=False)
    model_name = db.Column(db.String(100), nullable=False)  # e.g., 'gemini-1.5', 'gpt-4', 'claude-3'
    model_version = db.Column(db.String(50))  # e.g., 'flash', 'pro', 'turbo'
    response_content = db.Column(db.Text)
    processing_time = db.Column(db.Float)  # Time taken to generate response
    token_count = db.Column(db.Integer)
    status = db.Column(db.String(20), default='pending')  # pending, complete, error
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    session = db.relationship('ChatSession', backref=db.backref('model_responses', lazy=True))

class SupportedModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)
    provider = db.Column(db.String(50), nullable=False)  # google, openai, anthropic
    model_type = db.Column(db.String(50))  # text, multimodal, code
    is_active = db.Column(db.Boolean, default=True)
    api_key_required = db.Column(db.Boolean, default=True)
    max_tokens = db.Column(db.Integer)
    supports_streaming = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
"""
