import os
import re
import json

question_start_patterns = [
    r"༄༅།།གོ་བདེའི་ཚན་རྩལ་ཤེས་བྱའི་དྲི་བ་ཁྲི་བཅུ་བྱིས་པའི་བུ་རམ།",
    r"༄༅། །གོ་བདེའི་ཚན་རྩལ་ཤེས་བྱའི་དྲི་བ་ཁྲི་བཅུ་བྱིས་པའི་བུ་རམ།"
]

keywords_to_remove = [
    r"༄༅། །གློག་ཀླད་སྐོར་གྱི་དྲི་བ་དྲིས་ལན།",
    r"༄༅། །འཕྲུལ་འཁོར་སྐོར་གྱི་དྲི་བ་དྲིས་ལན།",
    r"༄༅། །སའི་གོ་ལའི་སྐོར་གྱི་དྲི་བ་དྲིས་ལན།"
]

tibetan_chars_pattern = re.compile(r'[ༀ-࿿A-Za-z]+')

english_only_pattern = re.compile(r'^[A-Za-z\s]+$')


def clean_text(text):
    for keyword in keywords_to_remove:
        text = re.sub(keyword, '', text)
    lines = text.splitlines()

    cleaned_lines = []
    for line in lines:
        if english_only_pattern.match(line):
            continue
        cleaned_lines.append(line)

    tibetan_text = ' '.join(tibetan_chars_pattern.findall(' '.join(cleaned_lines)))
    return tibetan_text.strip()


def extract_question_answer_pairs(text):
    pairs = []
    combined_question_pattern = "|".join(question_start_patterns)
    sections = re.split(combined_question_pattern, text)

    for section in sections[1:]:
        question_match = re.search(r'([ༀ-࿿]+?།)', section)
        if question_match:
            question = question_match.group(1)
            answer_match = re.split(combined_question_pattern, section[question_match.end():], maxsplit=1)
            answer = answer_match[0].strip() if answer_match else ""
            question = clean_text(question)
            answer = clean_text(answer)

            if question and answer:
                pairs.append({
                    "question": question,
                    "answer": answer
                })

    return pairs


def process_txt_files(input_dir, output_json_path):

    all_pairs = []

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read().replace('\n', '')
                pairs = extract_question_answer_pairs(text)
                all_pairs.extend(pairs)

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_pairs, json_file, ensure_ascii=False, indent=4)

    print(f"Extracted {len(all_pairs)} question-answer pairs and saved to {output_json_path}")


def main():
    input_dir = 'data/ocr/books/sample_1'
    output_json_path = 'data/ocr/output_q&a_pair/sample_1_questions_answers.json'

    process_txt_files(input_dir, output_json_path)


if __name__ == '__main__':
    main()
