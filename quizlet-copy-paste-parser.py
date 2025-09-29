import json
import argparse
import os

#turn a txt into a json file. ignoring empty lines and stuff in the case of screwed up copypastes. 
#uses utf-8
def txt_to_json(input_file, output_file):
    entries = []
    
    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]  # strip and remove empties

    #right now i'm using the format from the vocab google doc.
    for i in range(0, len(lines), 2):
        latin = lines[i]
        english = lines[i + 1] if i + 1 < len(lines) else ""
        entries.append({
            "latin": latin,
            "english": english,
            "audio": "https:totallyareallinktotheaudio"
        })
    
    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(entries, out, indent=2, ensure_ascii=False)

#a regular command should look like "python quizlet-copy-paste-parser.py vocablist.txt (vocablist.json)"
def main():
    parser = argparse.ArgumentParser(
        description="Convert alternating Latin/English vocab lines in a txt file into JSON format"
    )
    parser.add_argument("input", help="Path to the input txt file")
    parser.add_argument("output", nargs="?", help="Path to the output JSON file (optional, will use same name as the txt if none given)")
    args = parser.parse_args()

    input_file = args.input
    if args.output:
        output_file = args.output
    else:
        base, _ = os.path.splitext(input_file)
        output_file = base + ".json"

    txt_to_json(input_file, output_file)
    print(f"Conversion complete: {output_file}")


if __name__ == "__main__":
    main()
