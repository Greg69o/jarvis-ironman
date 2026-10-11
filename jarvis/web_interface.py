"""
Interface web pour contrôler JARVIS
"""

import logging
from flask import Flask, render_template, request, jsonify
import json

logger = logging.getLogger(__name__)

def create_app(jarvis_instance=None):
    """Crée l'application Flask"""
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/command', methods=['POST'])
    def handle_command():
        """Traite une commande via l'API"""
        data = request.json
        user_input = data.get('command', '')
        
        if not jarvis_instance:
            return jsonify({'error': 'JARVIS non initialisé'}), 500
        
        response = jarvis_instance.process_command(user_input)
        
        return jsonify({
            'command': user_input,
            'response': response,
            'timestamp': str(datetime.now())
        })
    
    @app.route('/api/profile', methods=['GET'])
    def get_profile():
        """Récupère le profil utilisateur"""
        if not jarvis_instance:
            return jsonify({'error': 'JARVIS non initialisé'}), 500
        
        profile = jarvis_instance.memory.get_profile()
        return jsonify(profile)
    
    @app.route('/api/profile', methods=['POST'])
    def update_profile():
        """Met à jour le profil utilisateur"""
        data = request.json
        if jarvis_instance:
            jarvis_instance.memory.update_profile(data)
            return jsonify({'success': True})
        return jsonify({'error': 'JARVIS non initialisé'}), 500
    
    @app.route('/api/history', methods=['GET'])
    def get_history():
        """Récupère l'historique"""
        limit = request.args.get('limit', 10, type=int)
        if jarvis_instance:
            history = jarvis_instance.memory.get_history(limit)
            return jsonify(history)
        return jsonify({'error': 'JARVIS non initialisé'}), 500
    
    return app
