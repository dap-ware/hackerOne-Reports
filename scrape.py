#!/usr/bin/env python3
import argparse
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from termcolor import colored

def send_to_webhook(webhook_url, title, link):
    data = {
        "text": f"Title: {title}\nLink: {link}"
    }
    requests.post(webhook_url, json=data)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

parser = argparse.ArgumentParser(
    description='This script scrapes publicly disclosed vulnerability reports from HackerOne\'s Hacktivity feed and writes the title and link of each report to a file.'
)
parser.add_argument('-o', '--output', type=str, default='h1Scrape.txt', help='Specify the file to write output to')
parser.add_argument('--slack-webhook', type=str, default=None, help='Specify a Slack webhook URL to send data to')
parser.add_argument('--discord-webhook', type=str, default=None, help='Specify a Discord webhook URL to send data to')

args = parser.parse_args()

clear_console()
print(colored("Starting script", 'green'))

driver = webdriver.Firefox()
print(colored("Initialized WebDriver", 'green'))

driver.get('https://hackerone.com/hacktivity')
print(colored("Opened URL: https://hackerone.com/hacktivity", 'green'))

time.sleep(5)

links = set()

while True:
    clear_console()
    print(colored("Starting new iteration", 'cyan'))

    elements = driver.find_elements(By.CSS_SELECTOR, '.daisy-link.routerlink.daisy-link.hacktivity-item__publicly-disclosed.spec-hacktivity-item-title')

    for e in elements:
        link = e.get_attribute('href')
        title = e.text
        if link not in links:
            links.add(link)

            print(colored(f"Processing link: {link}", 'cyan'))
            print(colored(f"Title: {title}", 'green'))
            print(colored(f'Link: {link}', 'blue'))

            with open(args.output, 'a') as f:
                f.write(f"Title: {title}\nLink: {link}\n\n")

            if args.slack_webhook:
                send_to_webhook(args.slack_webhook, title, link)

            if args.discord_webhook:
                send_to_webhook(args.discord_webhook, title, link)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
driver.quit()
