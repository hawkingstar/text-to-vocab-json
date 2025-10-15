from TTS.api import TTS
import json, os, re

INPUT_JSON  = "insula-romana.json"
OUTPUT_JSON = "insula-romana-with-audio.json"
AUDIO_DIR   = "insula-romana-audio"

os.makedirs(AUDIO_DIR, exist_ok=True)

# load multilingual model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False)

def safe_name(text):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", text)

# read json
with open(INPUT_JSON, encoding="utf-8") as f:
    vocab = json.load(f)

#generate audio for each entry's latin field
for entry in vocab:
    latin = entry["latin"]
    filename = os.path.join(AUDIO_DIR, safe_name(latin) + ".wav")

    # tts to file
    tts.tts_to_file(text=latin, file_path=filename, speaker=tts.speakers[0], language="it")

    entry["audio"] = filename
    print(f"Generated {filename}")

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(vocab, f, indent=2, ensure_ascii=False)

print(f"Finished {len(vocab)} entries.")
