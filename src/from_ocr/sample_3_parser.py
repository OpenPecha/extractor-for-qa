import re
import json


def clean_text(text):
    text = re.sub(r'\d+', '', text)
    text = text.replace('\n', '')
    return text.strip()


def extract_questions_answers(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    sections = re.split(r'ལན\s*--', content)

    qa_pairs = []

    for i in range(1, len(sections)):
        question = clean_text(sections[i-1].strip())
        answer = clean_text(sections[i].strip())
        qa_pairs.append({
            "question": question,
            "answer": answer
        })

    return qa_pairs


def save_to_json(qa_pairs, output_filepath):
    with open(output_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(qa_pairs, json_file, ensure_ascii=False, indent=4)


def main():
    input_txt = 'data/ocr/books/sample_3/དྲི་བ་དྲིས་ལན་འགའ་ཞིག་ཕྱོགས་གཅིག་ཏུ་བཏུས་པ།.txt'
    output_json = 'data/ocr/output_q&a_pair/sample_3_questions_answers.json'

    qa_pairs = extract_questions_answers(input_txt)
    save_to_json(qa_pairs, output_json)
    print(f"JSON file saved as {output_json}")


if __name__ == "__main__":
    main()
