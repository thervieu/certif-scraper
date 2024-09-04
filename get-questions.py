import os, sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def extract_data_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract information (replace these examples with your actual data extraction logic)
    h1_no_class = soup.find('h1', class_=False)
    title = h1_no_class.text.strip()
    # get topic and question_nb from title
    # get question <p class="card-text">.text, get text and images and dl them
    # get question type : <div class="question-choices-container">, <li class="multi-choice-item correct-hidden">
    # must count # of correct_hidden if single of multiple choice
    # <span class="multi-choice-letter"> for Yes/No
    # no div class for click
    
    # get choices : loop li.text, or last image of p.text
    
    # get site answer
    # loop <li class="multi-choice-item correct-hidden">
    # no div class for click  ; get <span class="correct-answer"> <img src="">

    # get most voted
    # index of li where <span class="badge badge-success most-voted-answer-badge"> is next ; if multiple use pipe ; store as string
    # if click, get link of discussion

    # get vote nb
    # div class="voting-summary..."> ->  <div class="vote-bar progress-bar>.text .data-original-title.split(" ")[0].toInt() ; produit en croix entre % pr trouver le nombre de votes
    
    # Get question text
    question_text = soup.find('p', class_='card-text').text.strip()
    print(f"Question: {question_text}")

    # Download images in the question text (if any)
    question_images = soup.find_all('p', class_='card-text')[0].find_all('img')
    for idx, img in enumerate(question_images):
        img_url = img['src']
        img_name = f"question_img_{idx}.jpg"
        download_image(img_url, img_name)

    # Determine question type
    question_type_container = soup.find('div', class_='question-choices-container')
    correct_hidden_items = question_type_container.find_all('li', class_='multi-choice-item correct-hidden')
    question_type = 'Multiple Choice' if len(correct_hidden_items) > 1 else 'Single Choice'
    print(f"Question Type: {question_type}")

    # Get choices and identify correct ones
    choices = []
    for li in question_type_container.find_all('li'):
        choice_text = li.text.strip()
        choice_img = li.find('img')
        if choice_img:
            img_url = choice_img['src']
            img_name = f"choice_img_{len(choices)}.jpg"
            download_image(img_url, img_name)
            choice_text += f" [Image: {img_name}]"
        choices.append(choice_text)
    print(f"Choices: {choices}")

    # Get site-provided correct answers
    correct_answers = []
    for li in correct_hidden_items:
        correct_answer_text = li.text.strip()
        correct_answer_img = li.find('img')
        if correct_answer_img:
            img_url = correct_answer_img['src']
            img_name = f"correct_answer_img_{len(correct_answers)}.jpg"
            download_image(img_url, img_name)
            correct_answer_text += f" [Image: {img_name}]"
        correct_answers.append(correct_answer_text)
    print(f"Correct Answers: {correct_answers}")

    # Get most voted answer
    most_voted = []
    for idx, li in enumerate(question_type_container.find_all('li')):
        if li.find('span', class_='badge badge-success most-voted-answer-badge'):
            most_voted.append(choices[idx])
    most_voted_str = ' | '.join(most_voted)
    print(f"Most Voted: {most_voted_str}")

    # Get vote count
    vote_summary_div = soup.find('div', class_='voting-summary')
    total_votes = 0
    if vote_summary_div:
        vote_bars = vote_summary_div.find_all('div', class_='vote-bar progress-bar')
        for vote_bar in vote_bars:
            percent = int(vote_bar['style'].split('width: ')[1].replace('%', '').strip())
            vote_title = vote_bar['data-original-title'].split(' ')[0]
            votes_for_option = int(vote_title) * percent // 100
            total_votes += votes_for_option
    print(f"Total Votes: {total_votes}")

    ### get year and month <div class="discussion-meta-data mt-3 pt-1 border-top"> <a href user /> <i>.text ????

    page_data = {
        'topic': topic,
        'question_nb': question_nb,
        'question': question,
        'question_type': string, # single choice, multiple choice, click
        'choices': string_with_pipe_seperator,
        'site_answer': nb_or_list,
        'vote_answer':
        'vote_nb:
    }
    
    return page_data
    pass

def get_questions(args):
    print("get_questions")
    all_questions = []
    csp = args[0]
    cert_name = args[1]
    questions_map = list()
    num_questions = sum(1 for _ in open(f'./{csp}_links/{cert_name}.txt', "r"))
    print(f'total questions found for {cert_name} : {num_questions}')
    file = open(f'./{csp}_links/{cert_name}.txt', "r")
    for question_path in file:
        page = requests.get(f'https://www.examtopics.com{question_path}')
        soup = BeautifulSoup(page.text, 'html.parser')

        for a in soup.find_all('a', href=True, class_="discussion-link"):
            if "AZ-" not in a.contents[0]:
                continue

            cert_name = a.contents[0].split("Exam ")[1].split(" topic")[0]
            if cert_name not in links_map:
                links_map[cert_name] = [a['href']]
            else:
                links_map[cert_name].append(a['href'])

            href_nb += 1
        if next_exists == False:
            break
        print(f'############### PAGE {page_nb} DONE #################')
        page_nb += 1

    current_day = datetime.now().day
    current_month = datetime.now().month
    os.mkdir(f'{csp}_links_{current_day}_{current_month}')

    print(f'href_nb = {href_nb}')
    for key in links_map:
        print(key)
        with open(f'./{csp}_links_{current_day}_{current_month}/{key}.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(str(link) for link in links_map[key]))
            myfile.write('\n')


if __name__=="__main__":
    # check args
    if len(sys.argv) < 3:
        print("not enough args")
        exit()
        
    args = sys.argv[1:]

    certif_map = map({
        "microsoft": ["AZ-305", "AZ-104", "AZ-140"],
    })
    if args[0] not in ["microsoft", "amazon"]:
        print("first argument should be microsoft or amazon")
        exit()
    if args[1] not in certif_map[args[0]:
        print("wrong certification, check map in the code")
    get_questions(args[:len(args)-1])
