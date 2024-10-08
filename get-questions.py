import os
import sys
from requests_html import HTMLSession
import json
import time

# Function to log in and maintain the session
def login_or_set_session(session, login_url=None, credentials=None, sessionid=None):
    if login_url and credentials:
        try:
            # Perform login if credentials and login URL are provided
            response = session.post(login_url, data=credentials)
            if response.status_code == 200:
                print("Login successful!")

                # Extract session ID from cookies
                session_id = session.cookies.get('sessionid')  # Replace 'sessionid' with the actual cookie name
                if session_id:
                    print(f"Session ID: {session_id}")
            else:
                print(f"Login failed with status code {response.status_code}")
                return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    return True


# Function to extract question data
def extract_question(session, i, max_retries=3, timeout_duration=8):
    retries = 0  # Initialize retry count

    while retries < max_retries:
        try:
            response = session.get(f'https://www.examtopics.com/exams/amazon/aws-certified-developer-associate-dva-c02/view/{i}', timeout=timeout_duration)
            print(f'https://www.examtopics.com/exams/amazon/aws-certified-developer-associate-dva-c02/view/{i}')
            
            # Check for valid response status
            if response.status_code != 200:
                print(f'Error {response.status_code}')
                return  # Exit if the page doesn't exist or returns an error

            response.html.render(timeout=timeout_duration)
            
            soup = response.html  # Use the HTML object from requests_html

            # Find all <div class="card exam-question-card"> elements
            question_cards = soup.find('div.card.exam-question-card')
            if not question_cards:
                print("No question cards found on the page.")
                return

            # Loop over each question card
            for _ in question_cards:
            
                # Extract the question text within each card
                h1_no_class = soup.find('h1', first=True)
                if not h1_no_class:
                    print("No title found!")
                    return

                title = h1_no_class.text.strip()
                print('title', title)

                # Get question text
                question_text = soup.find('p.card-text', first=True).text.strip()
                print(f"Question: {question_text}")

                # Determine question type
                question_type_container = soup.find('div.question-choices-container', first=True)
                if not question_type_container:
                    print("No question type container found!")
                    return

                correct_hidden_items = question_type_container.find('li.multi-choice-item.correct-hidden')
                question_type = 'multiple' if len(correct_hidden_items) > 1 else 'single'
                print(f"Question Type: {question_type}")

                # Get choices
                choices = [li.text.strip() for li in question_type_container.find('li')]
                print(f"Choices: {choices}")

                # Get site-provided correct answers
                site_answers = [li.text.strip() for li in correct_hidden_items]
                print(f"Correct Answers: {site_answers}")

                # Extract vote and answers
                votes_and_answers = []
                vote_progress_bar = soup.find('div.voting-summary', first=True)
                if vote_progress_bar:
                    vote_bars = vote_progress_bar.find('div.vote-bar.progress-bar')[:2]
                    for vote_bar in vote_bars:
                        data_original_title = vote_bar.attrs.get("data-original-title")
                        if data_original_title:
                            # Add data-original-title and the text of the div to the list
                            votes_and_answers.append((data_original_title, vote_bar.text.strip()))

                print(f"Total Votes: {votes_and_answers}")

                # Create a dictionary to store question data
                page_data = {
                    'question_text': question_text,
                    'question_type': question_type,
                    'choices': choices,
                    'site_answers': site_answers,
                    'vote_and_answers': votes_and_answers
                }
                
                # Append the result to the global question list
                questions_list.append(page_data)

                # Exit loop if the request is successful
            break
        
        except Exception as e:
            retries += 1
            print(f"Error processing page {i}: {e}, retrying... ({retries}/{max_retries})")
            time.sleep(2)  # Wait before retrying

            if retries == max_retries:
                print(f"Failed to process page {i} after {max_retries} retries.")


# Function to handle all questions from the file
def get_list_questions(session, args):
    i = 0
    file = open(f'{args[0]}_links/{args[1]}.txt', "r")
    
    for i in range(1, 45, 1):
        extract_question(session, i)  # Directly extract questions without threading

    # Output the extracted questions
    for question in questions_list:
        print('question_type:', question["question_type"])
        print('question_text:', question["question_text"])
        print('choices:', question["choices"])


if __name__ == "__main__":
        
    global questions_list
    questions_list = []

    # Create a persistent session
    session = HTMLSession()

    # Example credentials or session ID (modify as needed)
    login_url = 'https://www.examtopics.com/login/'  # Replace with actual login URL
    credentials = {
        'username': 'soflaim',
        'password': '16031999Zef92.'
    }
    sessionid = None  # Set this if you need to use a session ID directly

    # Attempt to log in or set the session
    if not login_or_set_session(session, login_url=login_url, credentials=credentials, sessionid=sessionid):
        print("Failed to establish session.")
        exit()

    # Start scraping questions using the persistent session
    get_list_questions(session)
    
    # Optionally, save the results to a JSON file
    with open(f'dva-c02_questions.json', 'w') as outfile:
        json.dump(questions_list, outfile, indent=2)
