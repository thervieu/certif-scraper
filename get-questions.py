import os
import re
import sys
import json
from bs4 import BeautifulSoup


# Function to extract question data
def extract_question(filename):
    try:
        # Open and read the local HTML file
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the file with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Find all <div class="card exam-question-card">
        question_cards = soup.find_all('div', class_='card exam-question-card')
        if not question_cards:
            print("No question cards found in the file.")
            return

        # Loop over each question card
        for question_card in question_cards:

            # Get question text
            question_text = question_card.find('p', class_='card-text').text.strip()
            # Regex pattern to find any character followed by an uppercase letter
            pattern = r'(\.)([A-Z])'

            # Replacement pattern to insert two newlines before the uppercase letter
            replacement = r'.\n\n\2'

            # Perform the substitution
            question_text = re.sub(pattern, replacement, question_text)
            # print(f"Question: {question_text}")

            # Determine question type by looking for multiple correct answers
            question_type_container = question_card.find('div', class_='question-choices-container')
            if not question_type_container:
                print("No question type container found for this question!")
                continue

            correct_hidden_items = question_type_container.find_all('li', class_='multi-choice-item correct-hidden')
            question_type = 'multiple' if len(correct_hidden_items) > 1 else 'single'
            # print(f"Question Type: {question_type}")

            # Get all choices
            choices = [li.text.strip() for li in question_type_container.find_all('li')]
            for i in range(len(choices)):
                choices[i] = choices[i].replace('\n', '')
                choices[i] = choices[i].replace('   ', '')
                choices[i] = choices[i][3:]
            # print(f"Choices: {choices}")

            # Get the correct answers (provided by the site)
            site_answers = [li.text.strip() for li in correct_hidden_items]
            for i in range(len(site_answers)):
                site_answers[i] = site_answers[i].replace('\n', '')
                site_answers[i] = site_answers[i].replace('   ', '')
                site_answers[i] = site_answers[i][3:]
            # print(f"Site Answers: {site_answers}")

            # Create a dictionary to store question data (optional)
            question_data = {
                'question_text': question_text,
                'question_type': question_type,
                'choices': choices,
                'site_answers': site_answers
            }

            # You can append this dictionary to a list if you want to store all questions
            questions_list.append(question_data)

    except Exception as e:
        print(f"Error processing file {filename}: {e}")


# Function to handle all questions from the file
def get_list_questions(cert):
    file_list = sorted(os.listdir(cert))
    for file in file_list:
        extract_question(f"{cert}/{file}")

    # Output the extracted questions
    # for question in questions_list[0:1]:
    #     print(f"Question Type: {question['question_type']}")
    #     print(f"Question Text: {question['question_text']}")
    #     print('Choices :')
    #     for choice in question['choices']:
    #         print(f'{choice}')
    #     print(f"Site Answers: {question['site_answers']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("wrong number of args")
        exit()

    global questions_list
    questions_list = []

    get_list_questions(sys.argv[1])
    
    # Optionally, save the results to a JSON file
    with open(f'{sys.argv[1]}_questions.json', 'w') as outfile:
        json.dump(questions_list, outfile, indent=2)
