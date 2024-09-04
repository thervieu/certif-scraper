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
