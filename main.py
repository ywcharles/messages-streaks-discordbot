# File: main.py
# Purpose: bot that keeps counts of the ohio messages
# Author: Charles Wu

# imports
import discord
from datetime import date, timedelta, datetime

TOKEN = 'INSERT TOKEN HERE'
client = discord.Client()
highestScoreHash = {}
currentScoreHash = {}

@client.event
async def on_ready():
    '''
    Makes the bot online
    '''
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.channel.id == "INSERT CHANNEL ID HERE":
        user = str(message.author)
        userID = user.split('#')[1]
        user_message = str(message.content)
        channel = str(message.channel.name)
        messageDay = date.today()
        td = timedelta(1)
        yesterdayDate = messageDay - td
        print(f'{userID}: {user_message} ({channel}) / {messageDay}')
        
        # Do not count the messages from the bit
        if message.author == client.user:
            return

        elif userID not in highestScoreHash and userID not in currentScoreHash:
            highestScoreHash[userID] = [1, user]
            currentScoreHash[userID] = [1, messageDay]

        elif currentScoreHash[userID][1] == yesterdayDate:
            currentScoreHash[userID][0] += 1
            currentScoreHash[userID][1] = messageDay
            if highestScoreHash[userID][0] <= currentScoreHash[userID][0]:
                highestScoreHash[userID][0] = currentScoreHash[userID][0]
                highestScoreHash[userID][1] = user

        elif currentScoreHash[userID][1] != yesterdayDate and currentScoreHash[userID][1] != date.today():
            if highestScoreHash[userID][0] <= currentScoreHash[userID][0]:
                highestScoreHash[userID][0] = currentScoreHash[userID][0]
                highestScoreHash[userID][1] = user
            currentScoreHash[userID][0] = 1
            currentScoreHash[userID][1] = messageDay

        print(f'highest {highestScoreHash}, current {currentScoreHash}')

        if user_message == '/current':
            await message.channel.send(f'@{user} current streak is {currentScoreHash[userID][0]} days')

        elif user_message == '/personal-best':
            await message.channel.send(f'@{user} highest streak is {highestScoreHash[userID]} days')

        elif user_message == '/leaderboard':
            sorted(highestScoreHash, key = highestScoreHash.get, reverse=True)
            counter = 1
            leaderboardMsg = ''
            for value in highestScoreHash.values():
                user = value[1]
                score = value[0]
                leaderboardMsg += f'{counter}. {user}: {score} days\n'
                counter += 1
            await message.channel.send(leaderboardMsg)

        elif user_message == '/help':
            await message.channel.send('/current: Check current score \n/personal-best: Check personal highest score \n/leaderboard: Check top 10 leaderboard')

    with open('currentStreaks', 'w') as file:
            file.write(str(currentScoreHash))

    with open('HighestStreaks', 'w') as file:
            file.write(str(highestScoreHash))


client.run(TOKEN)