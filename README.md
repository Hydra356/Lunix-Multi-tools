# 🔴 LUNIX - Multi-Tools OSINT

```
 ██▓     █    ██  ███▄    █  ██▓▒██   ██▒
▓██▒     ██  ▓██▒ ██ ▀█   █ ▓██▒▒▒ █ █ ▒░
▒██░    ▓██  ▒██░▓██  ▀█ ██▒▒██▒░░  █   ░
▒██░    ▓▓█  ░██░▓██▒  ▐▌██▒░██░ ░ █ █ ▒ 
░██████▒▒▒█████▓ ▒██░   ▓██░░██░▒██▒ ▒██▒
░ ▒░▓  ░░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ ░▓  ▒▒ ░ ░▓ ░
░ ░ ▒  ░░░▒░ ░ ░ ░ ░░   ░ ▒░ ▒ ░░░   ░▒ ░
  ░ ░    ░░░ ░ ░    ░   ░ ░  ▒ ░ ░    ░  
    ░  ░   ░              ░  ░   ░    ░  
                                         
```
## 📦 Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install requests pillow beautifulsoup4 pywin32 mss
```

Ou utilisez le fichier requirements.txt :

```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

### Lancement du programme

```bash
python Lunix.py
```

### Navigation dans le menu

1. Lancez le programme avec la commande ci-dessus
2. Sélectionnez une option en tapant le numéro correspondant (01-10)
3. Suivez les instructions à l'écran pour chaque module
4. Tapez `00` pour quitter le programme

## 📁 Structure du projet

```
Lunix/
│
├── Lunix.py                 # Script principal du multi-tools
├── README.md                # Documentation (ce fichier)
│
├── config/                  # Dossier contenant tous les modules
│   ├── username_tracker.py  # Module de recherche de username
│   ├── email_tracker.py     # (À venir)
│   ├── phone_info.py        # (À venir)
│   └── ...                  # Autres modules
│
└── results/                 # Dossier créé automatiquement pour les résultats
    └── *.txt                # Fichiers de résultats
```

## 🔴 Caractéristiques de l'interface

- **Couleur principale**: Rouge vif (#FF0000)
- **Style**: Interface CMD/Terminal pure
- **ASCII Art**: Logo personnalisé LUNIX
- **Navigation**: Menu numéroté simple et intuitif

## ⚙️ Configuration des modules

Chaque module est un fichier Python indépendant dans le dossier `config/`. Pour ajouter un nouveau module:

1. Créez un nouveau fichier `.py` dans le dossier `config/`
2. Utilisez le même format de couleurs (RED = '\033[91m')
3. Ajoutez l'option correspondante dans le menu principal (`Lunix.py`)

## 🛡️ Avertissement légal

**IMPORTANT**: Ce logiciel est destiné à des fins éducatives et de recherche uniquement. L'utilisation de cet outil pour des activités illégales est strictement interdite. L'auteur n'est pas responsable de l'utilisation abusive de ce programme.

**Respectez toujours**:
- Les conditions d'utilisation des plateformes
- Les lois sur la protection des données (RGPD, etc.)
- La vie privée des individus
- Les règles d'utilisation équitable (rate limiting)

## 💻 Compatibilité

- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, Kali, etc.)
- ✅ macOS

## 🔧 Dépannage

### Le texte ne s'affiche pas en rouge
- Vérifiez que votre terminal supporte les codes ANSI
- Sur Windows, utilisez Windows Terminal ou CMD moderne

### Erreur "Module not found"
```bash
pip install requests
```

### Permission denied
- Linux/Mac: `chmod +x Lunix.py`
- Ou utilisez: `python Lunix.py`

 `username_[username]_[date]_[heure].txt`

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 👤 Auteur

**[HYDRA]**
BTC : bc1pudrc5py4waggeyve324unmjjl0y2sj7lx8tycqq6d4dcucnuhcrszzw20v
ETC : 0xc185B4B9Fd235580265b2De70C77EE4b4Db4862d
SLN : HeVi2E9JfATEjmbN4wRKnAFN4nzHk9jRpkPQ1tLxyM84

---

⭐ Si vous aimez ce projet, n'hésitez pas à lui donner une étoile sur GitHub!

**Version**: 1.0 
**Dernière mise à jour**: 31/01/2026
