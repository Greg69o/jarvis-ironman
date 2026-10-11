"""
Système de tâches: commandes spécifiques et automatisations
"""

import logging
import requests
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class TaskExecutor:
    """Exécute les tâches spécifiques"""
    
    def __init__(self, config):
        self.config = config
        self.tasks = {
            "weather": self.get_weather,
            "time": self.get_time,
            "date": self.get_date,
            "news": self.get_news,
            "reminder": self.set_reminder,
            "calculate": self.calculate,
            "search": self.search,
        }
    
    def try_execute(self, user_input: str) -> Optional[str]:
        """Essaye d'exécuter une tâche"""
        user_input_lower = user_input.lower()
        
        # Détection de tâche
        if any(word in user_input_lower for word in ["météo", "weather", "temps"]):
            return self.get_weather()
        
        elif any(word in user_input_lower for word in ["heure", "time", "quelle heure"]):
            return self.get_time()
        
        elif any(word in user_input_lower for word in ["date", "aujourd'hui", "today"]):
            return self.get_date()
        
        elif any(word in user_input_lower for word in ["news", "actualités", "nouvelles"]):
            return self.get_news()
        
        elif "calcul" in user_input_lower or "=" in user_input:
            return self.calculate(user_input)
        
        elif "rappel" in user_input_lower or "reminder" in user_input_lower:
            return self.set_reminder(user_input)
        
        return None
    
    def get_weather(self) -> str:
        """Récupère la météo"""
        try:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": 48.8566,
                    "longitude": 2.3522,
                    "current": "temperature_2m,weather_code"
                }
            )
            data = response.json()
            temp = data['current']['temperature_2m']
            return f"Il fait actuellement {temp}°C à Paris."
        except Exception as e:
            logger.error(f"Erreur météo: {e}")
            return "Je n'ai pas pu récupérer la météo."
    
    def get_time(self) -> str:
        """Retourne l'heure actuelle"""
        now = datetime.now()
        hours = now.strftime("%H:%M")
        return f"Il est {hours}."
    
    def get_date(self) -> str:
        """Retourne la date actuelle"""
        now = datetime.now()
        date_str = now.strftime("%A %d %B %Y")
        return f"Nous sommes le {date_str}."
    
    def get_news(self) -> str:
        """Récupère les actualités (simulé)"""
        return "Les actualités du jour... (Intégration NewsAPI en cours)"
    
    def set_reminder(self, user_input: str) -> str:
        """Crée un rappel"""
        logger.info(f"📌 Rappel défini: {user_input}")
        return "J'ai créé un rappel pour toi."
    
    def calculate(self, expression: str) -> str:
        """Effectue un calcul"""
        try:
            # Extraire l'expression mathématique
            expr = expression.lower().replace("calcule", "").replace("combien", "").strip()
            result = eval(expr)
            return f"Le résultat est {result}."
        except Exception as e:
            logger.error(f"Erreur calcul: {e}")
            return "Je n'ai pas pu calculer."
    
    def search(self, query: str) -> str:
        """Effectue une recherche web"""
        # Placeholder pour recherche web
        return f"Résultats de recherche pour '{query}'..."
