# Matrice Cyber-AI — Assistant Personnel Local

**Cyber-AI** est un assistant de bord hybride (vocal et textuel) fonctionnant localement. Il est conçu pour s'intégrer au système afin d'agir comme un assistant de bord.

L'IA s'isole automatiquement dès que vous tapez au clavier pour éviter les faux déclenchements et intègre des filtres contre les hallucinations auditives.

> ⚠️ **Note :** Ce projet a été **en majorité vibecodé** au cours de sessions de développement, mêlant scripts Python et ajustements en temps réel.

---

## 🛠️ Guide d'Installation Rapide

### Étape 1 : Dépendances Système
Installez les outils requis pour la capture audio et la synthèse vocale native :
```fish
sudo pacman -S portaudio espeak-ng fastfetch --noconfirm
```

### Étape 2 : Matrice d'IA Locale (Ollama)
1. Installez et activez le démon Ollama si nécessaire :
   ```fish
   sudo pacman -S ollama --noconfirm
   sudo systemctl enable --now ollama
   ```
2. Téléchargez et initialisez la matrice Qwen 14B dans un terminal séparé :
   ```fish
   ollama run qwen2.5:14b
   ```

### Étape 3 : Environnement Python & Modules
Initialisez votre environnement virtuel et injectez les packages de décodage :
```fish
cd /home/suzukogmd/AssistantJarvis/
python -m venv venv
source venv/bin/activate.fish
pip install pyaudio wave whisper numpy requests
```

### Étape 4 : Injection du raccourci de démarrage
Créez la fonction Fish native pour démarrer l'assistant instantanément via la commande `cyber` :
```fish
echo 'function cyber; /home/suzukogmd/AssistantJarvis/venv/bin/python /home/suzukogmd/AssistantJarvis/jarvis_assistant.py; end' > ~/.config/fish/functions/cyber.fish
```

---

## 📄 Licence
Ce code est distribué sous les termes de la **Licence MIT en français** (incluse dans le dépôt). Vous êtes libre de cloner, modifier et adapter ce projet.
