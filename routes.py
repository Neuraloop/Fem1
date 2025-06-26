import json
import logging
from flask import render_template, request, jsonify, Response, redirect, url_for, flash, session
from app import app, db
from models import APIKey, ChatSession
from fem_solver import FEMSolver

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    api_keys = APIKey.query.all()
    return render_template('profile.html', api_keys=api_keys)

@app.route('/save_api_key', methods=['POST'])
def save_api_key():
    service_name = request.form.get('service_name')
    api_key = request.form.get('api_key')
    
    if not service_name or not api_key:
        flash('Service name and API key are required', 'error')
        return redirect(url_for('profile'))
    
    # Check if API key already exists for this service
    existing_key = APIKey.query.filter_by(service_name=service_name).first()
    
    if existing_key:
        existing_key.api_key = api_key
        flash(f'{service_name} API key updated successfully', 'success')
    else:
        new_key = APIKey(service_name=service_name, api_key=api_key)
        db.session.add(new_key)
        flash(f'{service_name} API key saved successfully', 'success')
    
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/delete_api_key/<int:key_id>', methods=['POST'])
def delete_api_key(key_id):
    api_key = APIKey.query.get_or_404(key_id)
    service_name = api_key.service_name
    db.session.delete(api_key)
    db.session.commit()
    flash(f'{service_name} API key deleted successfully', 'success')
    return redirect(url_for('profile'))

@app.route('/solve', methods=['POST'])
def solve_problem():
    try:
        data = request.get_json()
        problem = data.get('problem', '').strip()
        
        if not problem:
            return jsonify({'error': 'Problem description is required'}), 400
        
        # Get Gemini API key from database
        gemini_key = APIKey.query.filter_by(service_name='gemini').first()
        if not gemini_key:
            return jsonify({'error': 'Gemini API key not configured. Please add it in your profile.'}), 400
        
        def generate():
            try:
                with app.app_context():
                    # Initialize solver with API key
                    solver = FEMSolver(api_key=gemini_key.api_key)
                    
                    # Store session in database
                    chat_session = ChatSession(problem_description=problem)
                    db.session.add(chat_session)
                    db.session.commit()
                    
                    gemini_response = ""
                    openai_response = ""
                    final_response = ""
                    
                    # Stream the solving process
                    for update in solver.solve_streaming(problem):
                        # Send update to frontend
                        yield f"data: {json.dumps(update)}\n\n"
                        
                        # Store responses for database
                        if update['type'] == 'gemini_response':
                            gemini_response = update['content']
                        elif update['type'] == 'openai_response':
                            openai_response = update['content']
                        elif update['type'] == 'final_chunk':
                            final_response += update['content']
                    
                    # Update database with responses
                    chat_session.gemini_15_response = gemini_response
                    chat_session.gemini_25_response = openai_response
                    chat_session.final_response = final_response
                    db.session.commit()
                
            except Exception as e:
                logging.error(f"Error in solve_problem: {str(e)}")
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        
        return Response(generate(), mimetype='text/plain')
        
    except Exception as e:
        logging.error(f"Error in solve_problem route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat_history')
def chat_history():
    sessions = ChatSession.query.order_by(ChatSession.created_at.desc()).limit(20).all()
    return render_template('chat_history.html', sessions=sessions)

# Template routes for future model extensions (commented out for now)
"""
@app.route('/models')
def list_models():
    # List all available models and their status
    pass

@app.route('/model_config')
def model_config():
    # Configure which models to use for solving
    pass

@app.route('/solve_with_models', methods=['POST'])
def solve_with_selected_models():
    # Solve using user-selected models
    pass
"""

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
