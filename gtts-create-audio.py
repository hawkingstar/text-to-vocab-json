import json
import os
from gtts import gTTS

INPUT_JSON = "daily-phrases.json"     # Your input file
OUTPUT_DIR = "daily_phrases_audio"          #Where audio files will go
OUTPUT_JSON = "daily_phrases_with_audio.json"

# Create directory if not already existing
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)



# tweak to fix filenames
def sanitize_filename(text):
    # Remove punctuation and spaces for a clean filename
    return "".join(c for c in text if c.isalnum() or c in ('_', '-')).strip("-_")[:40]

# audio for each entry
for i, entry in enumerate(data):
    latin_text = entry["latin"]

    # handle parentheses and extra spaces
    clean_text = latin_text.replace("(", "").replace(")", "").strip()

    # Generate file name
    filename = sanitize_filename(clean_text or f"latin_{i}") + ".mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Generate and save TTS audio
    try:
        tts = gTTS(text=clean_text, lang="la")
        tts.save(filepath)
        entry["audio"] = filepath  # replace placeholder with actual file path
        print(f"Saved: {filepath}")
    except Exception as e:
        print(f"Error generating audio for \"{latin_text}\": {e}")
        entry["audio"] = None

# save updated JSON with audio paths
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nJSON with audio file paths saved to: ", OUTPUT_JSON, "!")  # Please tell me the exclamation point won't break the string