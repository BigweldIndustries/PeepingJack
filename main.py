# Import requirements
from concurrent.futures import ThreadPoolExecutor, as_completed
from string import ascii_uppercase
from itertools import product
import requests
import random
import time
import os


print('PeepingJack 1.4')
audience = input('Show just games in lobbies? (y or n, defaults to y): ')

if audience.lower() == "n":
    audience = False
else:
    audience = True


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

def checkcode(code):
    global stats

    # Check code
    r = requests.get(f'https://ecast.jackboxgames.com/api/v2/rooms/{code}')
    stats["checked"] += 1

    if r.status_code == 404:
        # Invalid
        stats["bad"] += 1

    else:
        # Valid
        stats["good"] += 1

        if audience == True:
            # If user wants lobbies only
            if r.json()["body"]["audienceEnabled"] == False:
                # Lobby game
                stats["lobbies"] += 1
                stats["valid"].append(code) # Write code to list

        else:
            # User wants all found codes, write code to list
            stats["valid"].append(code)


processes = []

with ThreadPoolExecutor(max_workers=500) as executor:
    print('[-] Threadpool begun')

    for code in keywords:
        # Loop through all codes
        processes.append(executor.submit(checkcode, code))
        # Update user with stats and code list
        print(f'All Valid: {stats["good"]}, Lobbies: {stats["lobbies"]}, Checked: {stats["checked"]}\n\n\nCodes:\n{stats["valid"]}\n\n')

# Write final stats and write to file
print(f'Bad codes: {stats["bad"]}, Good codes: {stats["good"]}, Checked total: {stats["checked"]}')
with open('valid.txt', 'w') as f:
    for code in stats["valid"]:
        f.writeline(code)
print("Wrote all codes to a file!")
