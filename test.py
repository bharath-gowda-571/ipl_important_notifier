import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pynotifier import Notification
import re
import sys
# driver = webdriver.Firefox()
# driver.get("https://www.cricbuzz.com/")
# match = driver.find_element_by_xpath("//li/a")
# match.click()

r = requests.get("https://www.cricbuzz.com/")
# print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')

li_tags = soup.find_all('li', {
                        "class": "cb-col cb-col-25 cb-mtch-blk cb-vid-sml-card-api videos-carousal-item cb-carousal-item-large cb-view-all-ga"})
link = li_tags[0].find('a').get('href')
print(link)

driver = webdriver.Firefox()
driver.get("https://www.cricbuzz.com/"+link)

previous_ball = ''
while True:
    elem_commentry = driver.find_element_by_xpath(
        "//p[@class='cb-com-ln ng-binding ng-scope cb-col cb-col-90']")
    elem_ball = driver.find_element_by_xpath(
        "//div[@class='cb-mat-mnu-wrp cb-ovr-num ng-binding ng-scope']")
    elem_score = driver.find_element_by_xpath(
        "//h2[@class='cb-font-20 text-bold inline-block ng-binding']")
    score = elem_score.text.split(" vs ")[0]
    current_ball = elem_ball.text.strip()
    commentry = elem_commentry.text
    if previous_ball == current_ball:
        time.sleep(3)
        continue
    else:
        batsman_bowler = commentry.split(",")[0]
        bowler = batsman_bowler.split(" to ")[0]
        batsman = batsman_bowler.split(" to ")[1]
        # print(current_ball, commentry)
        try:
            ball_score = re.search("\,(.*?)\,", commentry).group(1)
            if "four" in ball_score.lower():
                Notification(title=f"Four!! by {batsman}    Score:{score}", description=f" Bowler:{bowler}",
                             duration=10, urgency=Notification.URGENCY_NORMAL).send()
            elif "six" in ball_score.lower():
                Notification(
                    title=f"Six!! by {batsman}     Score:{score}", description=f" Bowler:{bowler}", duration=10, urgency=Notification.URGENCY_NORMAL).send()
        except AttributeError:
            try:
                ball_score = re.search("\,(.*)!!", commentry).group(1)
                if "run out" in ball_score.lower():
                    Notification(
                        title=f"Run Out!!    Score:{score}", description=f"", duration=10, urgency=Notification.URGENCY_NORMAL).send()
                else:
                    Notification(
                        title=f"{batsman} is Out!! {ball_score[3:]}    Score:{score}", description=f"Bowler: {bowler}", duration=10, urgency=Notification.URGENCY_NORMAL).send()
            except AttributeError:
                time.sleep(3)
                continue
        previous_ball = current_ball
        print(current_ball, batsman, bowler, ball_score, score)

    time.sleep(3)
# print(a_tags)
# for i in li_tags:
#     a_tag = i.find('a')
#     print(a_tag.get("href"))
