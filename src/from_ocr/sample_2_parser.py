import os
import re
import json


def extract_question_answer_pairs(text):
    pairs = []

    qa_pattern = re.compile(r'(\d+\.)\s*(.*?)།(.*?)(?=\d+\.)', re.DOTALL)

    matches = qa_pattern.findall(text)

    for match in matches:
        question_num = match[0]
        question = match[1].strip()
        answer = match[2].strip()
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
    input_dir = 'data/ocr/books/sample_2'
    output_json_path = 'data/ocr/output_q&a_pair/sample_2_questions_answers.json'

    process_txt_files(input_dir, output_json_path)


if __name__ == '__main__':
    main()
