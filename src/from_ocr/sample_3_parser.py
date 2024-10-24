import os
import re
import json

question_pattern = re.compile(r'(.+?)\s*ལན --')
answer_pattern = re.compile(r'ལན --(.+?)(?=\n|$)', re.DOTALL)


def extract_question_answer_pairs(text):

    pairs = []
    answer_sections = re.split(answer_pattern, text)

    for i in range(0, len(answer_sections) - 1, 2):
        question_match = answer_sections[i].strip()
        answer_match = answer_sections[i + 1].strip()

        if question_match and answer_match:
            pairs.append({
                "question": question_match,
                "answer": answer_match
            })

    return pairs


def process_txt_files(input_dir, output_json_path):
    all_pairs = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                pairs = extract_question_answer_pairs(text)
                all_pairs.extend(pairs)

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_pairs, json_file, ensure_ascii=False, indent=4)

    print(f"Extracted {len(all_pairs)} question-answer pairs and saved to {output_json_path}")


def main():
    input_dir = 'data/ocr/books/sample_3'
    output_json_path = 'data/ocr/output_q&a_pair/sample_3_questions_answers.json'

    process_txt_files(input_dir, output_json_path)


if __name__ == '__main__':
    main()
