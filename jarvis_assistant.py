import os
import requests
import json
import time
import sys
import pyaudio
import wave
import whisper
import numpy as np
import threading

try:
    stderr_fileno = sys.stderr.fileno()
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull_fd, stderr_fileno)
except:
    pass

print("Chargement de la matrice vocale optimisée...")
try:
    modele_vocal = whisper.load_model("small", device="cuda")
except Exception:
    modele_vocal = whisper.load_model("small", device="cpu")

est_mute = False
execution_en_cours = True
en_reflexion = False
au_clavier_local = False
verrou_systeme = threading.Lock()

def afficher_interface():
    os.system("clear")
    print("\033[38;5;198m" + r"""
     ██████  ██    ██  ██████  ███████ ██████
    ██       ▀██  ██▀  ██   ██ ██      ██   ██
    ██        ▀████▀   ██████  █████   ██████
    ██         ██      ██   ██ ██      ██   ██
     ██████    ██      ██████  ███████ ██   ██
""" + "\033[0m")
    print("\033[38;5;51m┌────────────────────────────────────────────────┐\033[0m")
    print("\033[38;5;226m │ MATRIX LINK: NEURAL INTERFACE // RTX 2070       │\033[0m")
    print("\033[38;5;51m├────────────────────────────────────────────────┤\033[0m")
    status_micro = "\033[38;5;198m[ IMPLANT MUTED // KEYBOARD FEED ]\033[0m" if est_mute else "\033[38;5;46m[ LINK ACTIVE // MIC FEED ]\033[0m"
    print(f"\033[38;5;51m │ LOG LINK   :\033[0m {status_micro}")
    print("\033[38;5;51m │ CORE SYSTEM:\033[0m \033[38;5;13mQwen 2.5 14B Matrix (Light)\033[0m")
    print("\033[38;5;51m │ NEURAL CHIP:\033[0m \033[38;5;13mCyberlink Kestrel v4.26\033[0m")
    print("\033[38;5;51m │ PROTOCOLS  :\033[0m 'un/mute' | 'relance' | 'quitter'")
    print("\033[38;5;51m└────────────────────────────────────────────────┘\033[0m")

def animer_reflexion():
    global en_reflexion
    frames = [
        "▖ [ COMPUTING MATRIX DATA ]",
        "▘ [ COMPUTING MATRIX DATA ]",
        "▝ [ COMPUTING MATRIX DATA ]",
        "▗ [ COMPUTING MATRIX DATA ]"
    ]
    idx = 0
    while en_reflexion:
        sys.stdout.write(f"\r\033[K\033[38;5;13m{frames[idx]}\033[0m")
        sys.stdout.flush()
        idx = (idx + 1) % len(frames)
        time.sleep(0.1)

def parler(texte):
    sys.stdout.write("\r\033[K")
    print(f"\033[38;5;198mCyber >\033[0m {texte}")
    nettoye = texte.replace('"', ' ').replace("'", ' ')
    nettoye = nettoye.lower().replace("choom", "choum")
    os.system(f'espeak-ng -v fr+m3 -s 165 -p 40 "{nettoye}" > /dev/null 2>&1')

def interroger_ollama(prompt):
    global en_reflexion
    url = "http://localhost:11434/api/generate"
    instruction_role = (
        "Tu t'appelles Cyber. Tu es une IA de bord issue d'une puce cybernétique nommée Kestrel, intégrée au système de l'utilisateur. "
        "Ton univers est celui de Cyberpunk 2077. Ton ton est direct, technique, professionnel, mais tu utilises l'argot de Night City. "
        "Appelle régulièrement l'utilisateur 'choom' (qui signifie ami/pote) ou parle de eddies, corpos, fixer, braindance si le contexte s'y prête. "
        "Évite le jeu de rôle excessif ou théâtral. Va droit au but. Fais des réponses très courtes et percutantes."
    )
    payload = {
        "model": "qwen2.5:14b",
        "prompt": f"{instruction_role}\n\nUtilisateur: {prompt}\nCyber:",
        "stream": False,
        "options": {"keep_alive": -1}
    }

    en_reflexion = True
    thread_anim = threading.Thread(target=animer_reflexion, daemon=True)
    thread_anim.start()

    try:
        response = requests.post(url, json=payload, timeout=30)
        en_reflexion = False
        time.sleep(0.15)
        return response.json()["response"]
    except:
        en_reflexion = False
        time.sleep(0.15)
        return "Erreur de connexion avec le serveur central Ollama."

def relancer_serveur():
    sys.stdout.write("\r\033[K\033[38;5;226m[ REBOOTING OLLAMA SERVICE... ]\033[0m\n")
    sys.stdout.flush()
    os.system("sudo systemctl restart ollama")
    time.sleep(1)
    try:
        url = "http://localhost:11434/api/generate"
        payload = {"model": "qwen2.5:14b", "prompt": "Bonjour", "stream": False, "options": {"keep_alive": -1}}
        requests.post(url, json=payload, timeout=15)
    except:
        pass

def traiter_commande(commande, source="clavier"):
    global est_mute, execution_en_cours

    commande_clean = commande.lower().strip().replace(",", "").replace(".", "").replace("!", "").replace("?", "")

    mots_cles_quitter = [
        "quitter", "ferme le système", "close", "exit", "stop", "éteindre",
        "deconnexion", "déconnexion", "quitte", "fermer"
    ]
    if any(mot in commande_clean for mot in mots_cles_quitter):
        parler("Fermeture de l'interface Kestrel. Déconnexion, choom.")
        execution_en_cours = False
        os._exit(0)

    if "relance" in commande_clean or "reboot" in commande_clean or "réveille" in commande_clean:
        relancer_serveur()
        afficher_interface()
        parler("Matrice Ollama réinitialisée et modèle rechargé en VRAM, choom.")
        return

    hallucinations_whisper = [
        "merci d'avoir regardé", "merci d'avoir regardé la vidéo",
        "sous-titres", "regardé la vidéo", "merci de votre attention"
    ]
    if any(h in commande_clean for h in hallucinations_whisper) and len(commande_clean) < 35:
        afficher_interface()
        return

    if source == "vocal":
        sys.stdout.write("\r\033[K")
        print(f"\033[38;5;46mUser_Voice //\033[0m {commande}")

    if "unmute" in commande_clean or "active le micro" in commande_clean or "parle" in commande_clean:
        est_mute = False
        afficher_interface()
        parler("Lien audio restauré. Flux vocal actif, choom.")
        return

    if "mute" in commande_clean or "silence" in commande_clean or "désactive le micro" in commande_clean:
        est_mute = True
        afficher_interface()
        parler("Microphone coupé. Mode texte activé, choom.")
        return

    if len(commande_clean) > 1:
        reponse = interroger_ollama(commande).strip()
        parler(reponse)

def boucle_audio():
    global est_mute, execution_en_cours, au_clavier_local
    p = pyaudio.PyAudio()
    try:
        index_micro = p.get_default_input_device_info()['index']
    except:
        index_micro = None

    stream = None
    audio_buffer = []
    seuil_voix = 600
    parle_en_cours = False
    blocs_silence = 0

    while execution_en_cours:
        try:
            if stream is None:
                try:
                    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, input_device_index=index_micro, frames_per_buffer=1024)
                except:
                    time.sleep(1)
                    continue

            if est_mute or au_clavier_local or verrou_systeme.locked():
                time.sleep(0.1)
                audio_buffer = []
                parle_en_cours = False
                blocs_silence = 0
                continue

            try:
                donnees = stream.read(1024, exception_on_overflow=False)
            except IOError:
                continue

            audio_data = np.frombuffer(donnees, dtype=np.int16)
            amplitude = np.max(np.abs(audio_data))

            if amplitude > seuil_voix:
                if not parle_en_cours:
                    parle_en_cours = True
                audio_buffer.append(donnees)
                blocs_silence = 0
            elif parle_en_cours:
                audio_buffer.append(donnees)
                blocs_silence += 1

                if blocs_silence > 25:
                    if au_clavier_local or verrou_systeme.locked():
                        audio_buffer = []
                        parle_en_cours = False
                        blocs_silence = 0
                        continue

                    sys.stdout.write("\r\033[K\033[38;5;226m[ PROCESSING AUDIO STREAM... ]\033[0m")
                    sys.stdout.flush()

                    chemin_temp = "/home/suzukogmd/AssistantJarvis/temp_voice.wav"
                    wf = wave.open(chemin_temp, 'wb')
                    wf.setnchannels(1)
                    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                    wf.setframerate(16000)
                    wf.writeframes(b''.join(audio_buffer))
                    wf.close()

                    audio_buffer = []
                    parle_en_cours = False
                    blocs_silence = 0

                    with verrou_systeme:
                        resultat = modele_vocal.transcribe(chemin_temp, language="fr", temperature=0.0, fp16=True)
                        commande_vocale = resultat["text"].strip()
                        if len(commande_vocale) > 1:
                            traiter_commande(commande_vocale, source="vocal")
                        else:
                            afficher_interface()

        except Exception:
            if stream is not None:
                try:
                    stream.close()
                except:
                    pass
                stream = None
            time.sleep(0.5)

thread_audio = threading.Thread(target=boucle_audio, daemon=True)
thread_audio.start()

afficher_interface()
parler("Système Cyber initialisé. Prêt à griller du ICE, choom.")

while execution_en_cours:
    try:
        au_clavier_local = False
        texte_clavier = input("\n\033[38;5;226mUser_Text //\033[0m ")
        if texte_clavier.strip():
            au_clavier_local = True
            with verrou_systeme:
                traiter_commande(texte_clavier, source="clavier")
    except (KeyboardInterrupt, EOFError):
        break
