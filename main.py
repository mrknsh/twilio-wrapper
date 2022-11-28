# NOTES
# if using a CSV, don't use UTF-8
# make sure you replace the weird curly commas with normal commas

import os
import time
from twilio.rest import Client
from dotenv import load_dotenv

# get environment variables
load_dotenv()
account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
from_number = os.getenv('from_number')
numbers_file = os.getenv('numbers_file')
messages_file = os.getenv('messages_file')
mode = os.getenv('mode') # 0 is send each message line seperate, 1 is send all messages in one message with the last message line seperate, 2 is send all messages in one message


# make twilio client
client = Client(account_sid, auth_token)

# load in numbers and messages
with open(numbers_file, 'r') as f:
    numbers = f.read().splitlines()
with open(messages_file, 'r') as f:
    messages = f.read().splitlines()

# clean up numbers
numbers = [number.replace(' ', '') for number in numbers]
numbers = [number.replace('-', '') for number in numbers]
numbers = [number.replace('(', '') for number in numbers]
numbers = [number.replace(')', '') for number in numbers]
# add country code
numbers = ['+1' + number for number in numbers]
# remove duplicates
numbers = list(set(numbers))
# make sure numbers are valid
numbers = [number for number in numbers if len(number) == 12]

# make message array based on mode
message_array = []
if mode == '0':
    message_array = messages
elif mode == '1':
    main_message = ''
    for i in range(len(messages) - 1):
        main_message += messages[i] + '\n'
    link_message = messages[-1]
    message_array = [main_message, link_message]
elif mode == '2':
    main_message = ''
    for message in messages:
        main_message += message + '\n'
    message_array = [main_message]

print("Sending Messages...")
# send each message to each number
for number in numbers:
    print("Sending to " + number)
    # wait 5 seconds here to avoid rate limiting
    time.sleep(5)
    for message in message_array:
        # wait one second here to avoid rate limiting
        time.sleep(1)
        client.messages.create(
            to=number,
            from_=from_number,
            body=message
        )