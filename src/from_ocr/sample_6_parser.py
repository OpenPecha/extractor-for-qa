import os
import re
import json

tibetan_number_pattern = r'[༠-༩][)]?'
question_end_patterns = [r'ལན་།', r'ལན་དུ།']
answer_end_pattern = re.compile(tibetan_number_pattern)
unwanted_patterns = [
    r'རྟགས་འཇུག་གི་སྐོར།',
    r'སུམ་ཅུ་པའི་སྐོར།',
    r'སུམ་རྟགས་ཀྱི་དྲིས་ལན་གསར་སྦྱོང་དགའ་བའི་བུ་རམ།',
    r'རྟགས་འཇུག་གི་སྐོར།'
]
english_numbers_pattern = re.compile(r'[0-9]+')


def clean_text(text):
    text = text.replace('\n', ' ')
    for pattern in unwanted_patterns:
        text = re.sub(pattern, '', text)
    text = re.sub(english_numbers_pattern, '', text)

    return text.strip()


def extract_question_answer_pairs(text):
    pairs = []
    sections = re.split(tibetan_number_pattern, text)

    for section in sections[1:]:
        question_end_match = None
        for question_end in question_end_patterns:
            question_end_match = re.search(question_end, section)
            if question_end_match:
                break

        if question_end_match:
            question = section[:question_end_match.start()].strip()
            answer_start = question_end_match.end()
            answer_match = answer_end_pattern.search(section[answer_start:])
            if answer_match:
                answer = section[answer_start:answer_match.start()].strip()
            else:
                answer = section[answer_start:].strip()

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
                text = file.read()

                pairs = extract_question_answer_pairs(text)
                all_pairs.extend(pairs)
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_pairs, json_file, ensure_ascii=False, indent=4)

    print(f"Extracted {len(all_pairs)} question-answer pairs and saved to {output_json_path}")


def main():
    input_dir = 'data/ocr/books/sample_6'
    output_json_path = 'data/ocr/output_q&a_pair/sample_6_questions_answers.json'

    process_txt_files(input_dir, output_json_path)


if __name__ == '__main__':
    main()
