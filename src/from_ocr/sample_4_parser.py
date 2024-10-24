import os
import re
import json

tibetan_number_pattern = re.compile(r'[༠-༩]+\s')

year_pattern = re.compile(r'ཕྱི་ལོ་[༠-༩]+')


def clean_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'[0-9]', '', text)
    text = re.sub(r'རོོ་ཟན་གྱིིས་བརྩམས།|སུམ་ཅུ་པའི་དྲི་བ་ཐ་སྙད་པའི་བླང་དོར་ལམ་སྟོོན།|རོ་ཟན་གྱིས་བཙུམས།', '', text)
    return text.strip()


def extract_question_answer_pairs(text):
    pairs = []
    sections = re.split(tibetan_number_pattern, text)

    for section in sections[1:]:
        question_match = re.search(r'(.+?)ལན།', section, re.DOTALL)
        if question_match:
            question = question_match.group(1).strip()
            answer_start = section.find('ལན།') + len('ལན།')
            answer = section[answer_start:].strip()

            next_question_match = re.search(tibetan_number_pattern, answer)
            while next_question_match:
                possible_year = answer[next_question_match.start()-10:next_question_match.end()]
                if year_pattern.search(possible_year):
                    next_question_match = re.search(tibetan_number_pattern, answer[next_question_match.end():])
                else:
                    answer = answer[:next_question_match.start()].strip()
                    break

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
    input_dir = 'data/ocr/books/sample_4'
    output_json_path = 'data/ocr/output_q&a_pair/sample_4_questions_answers.json'

    process_txt_files(input_dir, output_json_path)


if __name__ == '__main__':
    main()
