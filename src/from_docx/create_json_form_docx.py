import json
from docx import Document

def extract_qa_from_docx(docx_path):
    document = Document(docx_path)
    qa_pairs = []

    question = None
    answer = None

    for para in document.paragraphs:
        text = para.text.strip()

        # Check if the paragraph contains the answer marker
        if "ལན།" in text:
            # If we have a question, save the previous question and the current answer
            if question is not None:
                # Remove the answer marker from the answer
                answer = text.replace("ལན།", "").strip()
                qa_pairs.append({
                    "question": question,
                    "answer": answer
                })
                question = None  # Reset question for the next pair
            else:
                # If there's no question, just continue to next paragraph
                continue
        else:
            # If the paragraph doesn't contain the answer marker, consider it as a question
            if question is None:
                question = text  # Store the current paragraph as a question
            else:
                # If we already have a question, append this paragraph to it
                question += ' ' + text

    return qa_pairs

def save_qa_to_json(qa_pairs, json_path):
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(qa_pairs, json_file, ensure_ascii=False, indent=4)

# Replace 'your_file.docx' with the path to your .docx file
docx_path = 'data/docx/སྒྲུང་གཏམ་གསར་རྩོམ་ཐད་ཀྱི་དྲི་བ་དྲིས་ལན་སྐལ་ལྡན་ཡིད་ཀྱི་མུན་སེལ།.docx'
json_path = 'q&a_pair_output.json'

qa_pairs = extract_qa_from_docx(docx_path)
save_qa_to_json(qa_pairs, json_path)

print(f"Extracted Q&A pairs saved to {json_path}.")
