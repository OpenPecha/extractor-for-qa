import json

def remove_first_word_from_question(json_file, output_file):
    # Load the JSON data from the file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Process each question in the JSON data
    for item in data:
        question = item.get('question', '').strip()
        # Split the question into words and remove the first word
        words = question.split()
        if len(words) > 1:
            item['question'] = ' '.join(words[1:])  # Remove the first word

    # Save the updated data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Usage
json_file = 'q&a_pair_output.json'  # Replace with your actual input JSON file path
output_file = 'updated_output_file.json'  # Output JSON file with updated questions

remove_first_word_from_question(json_file, output_file)

print(f"Updated questions have been saved to {output_file}")
