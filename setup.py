#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script d'installation pour l'outil de test de sécurité Outlook
"""

import os
import sys
import json
from pathlib import Path

# Configuration par défaut
DEFAULT_CONFIG = {
    "azure_ad": {
        "client_id": "",
        "client_secret": "",
        "authority": "https://login.microsoftonline.com/common",
        "scopes": ["https://graph.microsoft.com/.default"]
    },
    "app": {
        "user_agent": "OutlookSecurityTester/1.0",
        "timeout": 30,
        "max_retries": 3
    }
}

def create_config_file():
    """Crée le fichier de configuration avec les valeurs par défaut"""
    config_path = Path("config.json")
    
    if config_path.exists():
        print("⚠️  Le fichier de configuration existe déjà.")
        overwrite = input("Voulez-vous le remplacer ? (o/n): ").lower()
        if overwrite != 'o':
            print("Installation annulée.")
            return
    
    print("\n🔧 Configuration de l'application Azure AD")
    print("=" * 50)
    print("Pour configurer l'application Azure AD :")
    print("1. Allez sur https://portal.azure.com")
    print("2. Créez une nouvelle inscription d'application")
    print("3. Notez l'ID client et créez un secret client")
    print("4. Configurez les autorisations pour Microsoft Graph")
    print("5. Ajoutez les URI de redirection si nécessaire\n")
    
    config = DEFAULT_CONFIG.copy()
    
    # Demande des informations de configuration
    config['azure_ad']['client_id'] = input("Entrez l'ID client de l'application Azure AD : ").strip()
    config['azure_ad']['client_secret'] = input("Entrez le secret client de l'application : ").strip()
    
    # Écriture du fichier de configuration
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"\n✅ Configuration enregistrée dans {config_path}")

def install_dependencies():
    """Installe les dépendances requises"""
    print("\n📦 Installation des dépendances...")
    os.system("pip install -r requirements.txt")
    print("✅ Dépendances installées avec succès")

def main():
    print("\n" + "=" * 50)
    print("🔐 Installation de l'outil de test de sécurité Outlook")
    print("=" * 50)
    
    # Création du fichier de configuration
    create_config_file()
    
    # Installation des dépendances
    install_dependencies()
    
    print("\n✨ Installation terminée avec succès !")
    print("\nPour commencer à utiliser l'outil, exécutez :")
    print("python hack_outlook.py --help")

if __name__ == "__main__":
    main()
