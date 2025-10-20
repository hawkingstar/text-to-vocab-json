import subprocess, json, os, re, argparse



def safe_name(text):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", text)

#a regular command should look like "python espeak-create-audio.py insula-romana.json (insula-romana_with_audio.json) (audio/insula-romana/)"
#parentheses means they're not required but can be filled in with the pattern that you see
def main():
    parser = argparse.ArgumentParser(
        description="Convert alternating Latin/English vocab lines in a txt file into JSON format"
    )
    parser.add_argument("input", help="Path to the input json file")
    parser.add_argument("output", nargs="?", help="Path to the output JSON file (optional, will use name but adding \"_with_audio\" as the name if none given)")
    parser.add_argument("audio_dir", nargs="?", help="Directory to save audio files (optional, will use 'audio/insert-name' if none given)")
    
    #look at arguments
    args = parser.parse_args()
    input_file = args.input

    #fill in other arguments if need be
    output_file = args.output if args.output else f"{os.path.splitext(input_file)[0]}_with_audio.json"
    audio_dir = args.audio_dir if args.audio_dir else f"audio/{os.path.splitext(input_file)[0]}/"
    os.makedirs(audio_dir, exist_ok=True)

    with open(input_file, encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        latin = entry["latin"]
        filename = os.path.join(audio_dir, safe_name(latin) + ".wav")

        # generate audio with the Latin voice
        #thank you GIAC for teaching me subprocesses
        subprocess.run(["espeak-ng", "-v", "la", "-w", filename, "--", latin], check=True)

        entry["audio"] = filename

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Created {len(data)} audio files in \'{audio_dir}\' and updated JSON saved to \'{output_file}\'")


if __name__ == "__main__":
    main()