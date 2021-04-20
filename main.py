#!/usr/bin/python3
from selenium import webdriver
import time
from pynotifier import Notification
import re
import sys

# print(sys.argv)

# enter command:
# python3 main.py "link-to-cricbuzz-match"
if len(sys.argv) >= 2:
    print(sys.argv)
    driver = webdriver.Firefox()
    driver.get(sys.argv[1])

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
