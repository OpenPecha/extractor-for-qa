import json
import os


def check_questions_answers(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    question_count = 0
    answer_count = 0
    mismatch_line = None

    for idx, entry in enumerate(data, start=1):
        if 'question' in entry:
            question_count += 1
        if 'answer' in entry:
            answer_count += 1
        if 'question' in entry and 'answer' not in entry:
            mismatch_line = idx
            print(f"Mismatch found at line {mismatch_line}: Question without answer.")
            break
        elif 'answer' in entry and 'question' not in entry:
            mismatch_line = idx
            print(f"Mismatch found at line {mismatch_line}: Answer without question.")
            break

    print(f"Total Questions: {question_count}")
    print(f"Total Answers: {answer_count}")

    if question_count != answer_count and mismatch_line is None:
        print("No exact line mismatch found, but counts differ.")


json_file_path = 'data/ocr/combined_json/q&a_pair.json'
check_questions_answers(json_file_path)
