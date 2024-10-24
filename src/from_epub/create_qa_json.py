import os
import json
from bs4 import BeautifulSoup


def extract_question_answer_pairs(xhtml_file_path):
    with open(xhtml_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'lxml-xml')

    question = None
    answer = []
    pairs = []
    accumulating_answer = False

    paragraphs = soup.find_all('p', class_='Body')

    for p in paragraphs:
        text = p.get_text(strip=True)

        if 'དྲི་བ།' in text:
            if question and answer:
                pairs.append({
                    "question": question,
                    "answer": ' '.join(answer)
                })
            question = text
            answer = []
            accumulating_answer = False
        elif 'ལན།' in text:
            if question:
                accumulating_answer = True
                answer.append(text)
        elif accumulating_answer:
            answer.append(text)

    if question and answer:
        pairs.append({
            "question": question,
            "answer": ' '.join(answer)
        })

    return pairs


def process_xhtml_files(input_dir, output_json_path):
    all_pairs = []

    for filename in os.listdir(input_dir):
        if filename.endswith('.xhtml'):
            file_path = os.path.join(input_dir, filename)
            pairs = extract_question_answer_pairs(file_path)
            all_pairs.extend(pairs)

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_pairs, json_file, ensure_ascii=False, indent=4)

    print(f"Extracted {len(all_pairs)} question-answer pairs and saved to {output_json_path}")


input_dir = 'data/decompiled_epub/book2/OEBPS'
output_json_path = 'data/output_json/Bod-Gangchen-Gyarab-Driwa-Drilen_question_answer_pairs.json'

process_xhtml_files(input_dir, output_json_path)
