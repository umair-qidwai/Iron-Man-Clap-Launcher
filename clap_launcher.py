# /// script
# dependencies = ["pyaudio", "numpy"]
# ///

import pyaudio
import numpy as np
import subprocess
import time

CLAP_THRESHOLD = 30000
DOUBLE_CLAP_GAP = 0.6
CLAP_MIN_GAP = 0.1         # claps must be at least 0.1s apart
COOLDOWN = 2.0

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1,
                rate=44100, input=True, frames_per_buffer=1024)

print("Listening for double clap...")

last_clap_time = 0
clap_count = 0

def open_vscode():
    subprocess.Popen(["open", "-a", "Visual Studio Code"])
    print("VS Code opened!")

try:
    while True:
        data = np.frombuffer(stream.read(1024, exception_on_overflow=False), dtype=np.int16)
        peak = np.max(np.abs(data))

        if peak > CLAP_THRESHOLD:
            now = time.time()
            gap = now - last_clap_time
            if gap > CLAP_MIN_GAP and gap < DOUBLE_CLAP_GAP:
                clap_count += 1
                if clap_count >= 2:
                    open_vscode()
                    clap_count = 0
                    time.sleep(COOLDOWN)
            elif gap > DOUBLE_CLAP_GAP:
                clap_count = 1
            last_clap_time = now

except KeyboardInterrupt:
    print("Stopped.")
    stream.stop_stream()
    stream.close()
    p.terminate()
