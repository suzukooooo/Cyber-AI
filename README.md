# Matrix Cyber — Spécifications Techniques & Installation

Matrix Cyber est un outil d'assistance hybride (vocal et textuel) s'exécutant en architecture locale sous environnement Linux (CachyOS). Ce logiciel fournit une interface de traitement de requêtes connectée à un modèle de langage (LLM) et un moteur de transcription de flux audio (STT), sans dépendance réseau externe.

---

## 🛠️ Composants et Stack Logicielle

*   **Traitement de Langage (LLM) :** Interconnexion via API REST locale avec le moteur Ollama, exploitant le modèle Qwen 2.5 14B maintenu en mémoire vive persistante (`keep_alive: -1`).
*   **Reconnaissance Vocale (STT) :** Intégration de la bibliothèque OpenAI Whisper (modèle Small). Les calculs d'inférence sont assignés au processeur graphique via l'API NVIDIA CUDA en mode de précision demi-flottante (FP16).
*   **Gestions du Flux Audio :** Capture continue du signal d'entrée matérielle par PyAudio, échantillonné à 16 000 Hz en mono (format PCM Int16).
*   **Mécanisme d'Isolation Clavier :** Implémentation d'un indicateur d'état partagé bloquant temporairement la lecture du flux audio lors des phases de saisie utilisateur (`input`), évitant les collisions de threads et les injections concurrentes.
*   **Filtre de Traitement Textuel :** Module de nettoyage post-transcription interceptant les structures syntaxiques itératives caractéristiques des hallucinations du modèle Whisper sur les signaux à faible rapport signal/bruit.

---

## 🖥️ Protocoles du Système de Bord

L'interface intercepte et exécute en priorité les requêtes d'administration système suivantes (vocale ou texte) :
*   `mute` / `silence` : Désactive l'acquisition du microphone et bascule sur l'interface texte exclusive.
*   `unmute` / `parle` : Réactive le flux d'entrée du microphone.
*   `relance` / `reboot` : Redémarre à chaud le service système Ollama et réinjecte immédiatement un ping réseau pour recharger le modèle Qwen 14B dans la VRAM de la carte graphique.
*   `quitter` / `exit` : Provoque la déconnexion de l'interface Kestrel et l'arrêt propre des processus Python.

---

## 📄 Licence

Ce projet est distribué sous les termes de la **Licence MIT en français**. Vous êtes libre de copier, modifier, distribuer et adapter ce code sous réserve de conserver la mention de copyright d'origine.
