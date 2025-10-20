import subprocess, json, os, re

# where your vocab JSON is
INPUT_JSON  = "daily-phrases.json"
OUTPUT_JSON = "daily-phrases_with_audio.json"
AUDIO_DIR   = "audio/daily-phrases/"

os.makedirs(AUDIO_DIR, exist_ok=True)

def safe_name(text):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", text)

with open(INPUT_JSON, encoding="utf-8") as f:
    data = json.load(f)

for entry in data:
    latin = entry["latin"]
    filename = os.path.join(AUDIO_DIR, safe_name(latin) + ".wav")

    # generate audio with the Latin voice
    subprocess.run(["espeak-ng", "-v", "la", latin, "-w", filename], check=True)
    entry["audio"] = filename

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Created {len(data)} audio files in \'{AUDIO_DIR}\' and updated JSON saved to \'{OUTPUT_JSON}\'")
