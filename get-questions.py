import os, sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_questions(args):
    print("list_links")
    next_exists = True
    page_nb = 1
    href_nb = 0
    csp = args[0]
    links_map = {}
    while True:
        page = requests.get(f'https://www.examtopics.com/discussions/{csp}/{page_nb}/')
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
    # get just the links
    # or the questions (but questions assumed that you already searched the links)
    args = sys.argv[1:]

    if args[0] not in ["microsoft", "amazon"]:
        print("first argument should be microsoft or amazon")
        exit()
    if args[1] not in ["list", "get"]:
        print("wrong third arg, can be list or get")
    get_questions(args[:len(args)-1])
