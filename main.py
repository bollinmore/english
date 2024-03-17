import argparse
import json
import random

def read_data_from_file(file_name):
    """Read data from the input file."""
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.readlines()

def extract_data(lines):
    """Extract Chinese and English sentences from the lines."""
    skip_patterns = ["[Source]", "#", "##", "---"]
    data = []
    chinese_sentence = ""
    english_sentence = ""
    for line in lines:
        if not line.strip():
            continue
        if any(line.startswith(pattern) for pattern in skip_patterns):
            continue
        if line.startswith(">"):
            english_sentence = line.strip()[1:].strip()
        else:
            if chinese_sentence and english_sentence:
                data.append({"ch": chinese_sentence, "en": english_sentence})
                chinese_sentence = ""
                english_sentence = ""
            chinese_sentence = line.strip()
    return data

def write_data_to_json(data, output_file):
    """Write data to a JSON file with indentation for readability."""
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def convert_to_json(input_file, output_file):
    """Convert markdown data to JSON format."""
    lines = read_data_from_file(input_file)
    data = extract_data(lines)
    write_data_to_json(data, output_file)

def pick_random_sentence(data_file):
    """Pick a random sentence from the JSON file."""
    with open(data_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    random_entry = random.choice(data)
    chinese_sentence = random_entry["ch"]
    english_translation = random_entry["en"]
    print("Chinese sentence:", chinese_sentence)
    user_translation = input("Enter English translation: ")
    if user_translation.strip() == english_translation.strip():
        print("Correct!")
    else:
        print("Incorrect. The correct translation is:", english_translation)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Process markdown data.")
    parser.add_argument("--convert", metavar=("input_file", "output_file"), nargs=2, help="Convert markdown to JSON")
    parser.add_argument("--random", metavar="data_file", const="english.json", nargs="?", help="Pick random sentence")
    args = parser.parse_args()

    if args.convert:
        input_file, output_file = args.convert
        convert_to_json(input_file, output_file)
    elif args.random:
        data_file = args.random
        pick_random_sentence(data_file)
    else:
        print("Please specify either --convert or --random.")

if __name__ == "__main__":
    main()
