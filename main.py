# Import requirements
from concurrent.futures import ThreadPoolExecutor, as_completed
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from string import ascii_uppercase
from selenium import webdriver
from itertools import product
from sys import platform
import requests
import random
import time
import os


print('PeepingJack 1.4')
username = input("Username: ")
numopen = int(input("How many to find?: "))


driver = webdriver.Chrome(ChromeDriverManager().install())



# Create a list of all possible codes in a random order
print('Producing all possible combinations...')

keywords = [''.join(i) for i in product(ascii_uppercase, repeat = 4)]
random.shuffle(keywords)

print('Done')

# Initialize stats
stats={
    "good": 0,
    "bad": 0,
    "lobbies": 0,
    "checked": 0,
    "valid": []
}
driver.get("https://jackbox.tv")

done = False
def checkcode(code):
    global stats
    global username
    global done

    tempc = str(stats["checked"]) # I have no idea, but this allows me to return focus to the initial window
    if numopen <= stats["lobbies"]:
        done = True
    # Check code
    if done != True:
        r = requests.get(f'https://blobcast.jackboxgames.com/room/{code}')
        # Update user with stats and code list
        url=f"https://jackbox.tv/#/{code}"
        stats["checked"] += 1

        if r.status_code == 404:
            # Invalid
            stats["bad"] += 1

        else:
            # Valid
            stats["good"] += 1
            # If user wants lobbies only
            if r.json()["joinAs"] != "audience" and r.json()["joinAs"] != "full":
                # Lobby game
                stats["lobbies"] += 1
                stats["valid"].append(code) # Write code to list
                driver.execute_script('''let win'''+tempc+''' = window.open("'''+url+'''","_blank");''') # Open game in new tab
                
    else:
        pass


def statsUpdate():
    # Prints stats
    while numopen > stats["lobbies"]:
        print(f'All Valid: {stats["good"]}, Lobbies: {stats["lobbies"]}, Checked: {stats["checked"]}\n\n\nCodes:\n{stats["valid"]}\n\n')
        time.sleep(0.1)

processes = []

with ThreadPoolExecutor(max_workers=500) as executor:
    print('[-] Threadpool begun')
    processes.append(executor.submit(statsUpdate)) # Start status update thread
    for code in keywords:
        # Loop through all codes
        processes.append(executor.submit(checkcode, code))

print('Done!')