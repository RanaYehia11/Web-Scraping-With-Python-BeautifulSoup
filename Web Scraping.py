import os
import requests
from bs4 import BeautifulSoup
import csv

date = input("Please Enter a Date in the following format MM/DD/YYYY: ")
page = requests.get(f"https://www.yallakora.com/match-center/%d9%85%d8%b1%d9%83%d8%b2-%d8%a7%d9%84%d9%85%d8%a8%d8%a7%d8%b1%d9%8a%d8%a7%d8%aa?date={date}")

def main(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []

    championships = soup.find_all("div", {'class': 'matchCard'})

    def get_match_info(championship):
        championship_title = championship.contents[1].find("h2").text.strip()
        all_matches = championship.find_all("div", {'class': "item future liItem"})
        no_of_matches = len(all_matches)

        for i in range(no_of_matches):
            # get teams names
            team_A = all_matches[i].find('div', {"class": "teamA"}).text.strip()
            team_B = all_matches[i].find('div', {"class": "teamB"}).text.strip()
            
            # get teams scores
            match_result = all_matches[i].find('div', {"class": "MResult"}).find_all('span', {'class': 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

            # get match time
            time = all_matches[i].find('div', {"class": "MResult"}).find('span', {'class': 'time'}).text.strip()

            # add match info into match_details
            matches_details.append({
                "نوع البطولة": championship_title,
                "الفريق الاول": team_A,
                "الفريق الثاني": team_B,
                "ميعاد المباراه": time,
                "النتيجة": score
            })

    for i in range(len(championships)):
        get_match_info(championships[i])

    # Check if matches_details is empty
    if not matches_details:
        print("No matches found for the given date.")
        return

    # Ensure directory exists
    output_dir = r'E:\iti training\python projects\Web Scraping'
    os.makedirs(output_dir, exist_ok=True)

    # csv file
    keys = matches_details[0].keys()
    output_file_path = os.path.join(output_dir, 'matches_details.csv')
    
    with open(output_file_path, 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("file created")

main(page)
