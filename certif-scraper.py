import os, sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def list_links(args):
    href_nb = 0
    csp = args[0]
    total_pages = 0
    if csp == "microsoft:
        total_pages = 1279
    else:
        total_pages = 506
    links_map = {}
    for page_nb in list(range(1, total_pages)):
        page = requests.get(f'https://www.examtopics.com/discussions/{csp}/{page_nb}/')
        soup = BeautifulSoup(page.text, 'html.parser')

        for a in soup.find_all('a', href=True, class_="discussion-link"):

            # skip uninteresting certifs
            if csp == "microsoft" and "AZ-" not in a.contents[0]:
                continue

            cert_name = ""
            if csp == "microsoft:
                cert_name = a.contents[0].split("Exam ")[1].split(" topic")[0]
            if csp == "amazon":
                split_on_topic = a.contents[0].split(" topic")[0]
                cert_name = split_on_topic.split(" ", len(split_on_topic)-1)
                print(f'amazon: certification name: {cert_name}')

            if cert_name not in links_map:
                links_map[cert_name] = [a['href']]
            else:
                links_map[cert_name].append(a['href'])
                    

            href_nb += 1
        print(f'############### PAGE {page_nb} DONE #################')

    current_day = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year
    os.mkdir(f'{csp}_links')
    os.mkdir(f'{csp}_links_{current_year}_{current_month}_{current_day}')

    print(f'total Azure questions found : {href_nb}')
    for key in links_map:
        print(key)
        with open(f'./{csp}_links_{current_year}_{current_month}_{current_day}/{key}.txt', mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(str(link) for link in links_map[key]))
            myfile.write('\n')


if __name__=="__main__":
    # check args
    if len(sys.argv) < 2:
        print("not enough args")
        exit()

    args = sys.argv[1:]

    if args[0] not in ["microsoft", "amazon"]:
        print("argument should be microsoft or amazon")
        exit()
    list_links(args)
