"""
File: main.py
Purpose: bot that keeps counts of the days that users texted in a row on a discord channel
Author: Charles Wu
"""

# imports
from datetime import date, timedelta

import discord
from dotenv import dotenv_values

config = dotenv_values(".env")

TOKEN = config["TOKEN"]
CHANNEL_ID = int(config["CHANNEL_ID"])
client = discord.Client()
highest_score_hash = {}
current_score_hash = {}


@client.event
async def on_ready():
    """
    Makes the bot online
    """
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    """
    Reads messages and checks for commands
    """
    if message.channel.id == CHANNEL_ID:
        user = str(message.author)
        user_id = user.split("#")[1]
        user_message = str(message.content)
        channel = str(message.channel.name)
        message_day = date.today()
        day_t = timedelta(1)
        yesterday_date = message_day - day_t
        print(f"{user_id}: {user_message} ({channel}) / {message_day}")

        # Do not count the messages from the bit
        if message.author == client.user:
            return

        if user_id not in highest_score_hash and user_id not in current_score_hash:
            highest_score_hash[user_id] = [1, user]
            current_score_hash[user_id] = [1, message_day]

        elif current_score_hash[user_id][1] == yesterday_date:
            current_score_hash[user_id][0] += 1
            current_score_hash[user_id][1] = message_day
            if highest_score_hash[user_id][0] <= current_score_hash[user_id][0]:
                highest_score_hash[user_id][0] = current_score_hash[user_id][0]
                highest_score_hash[user_id][1] = user

        elif (
            current_score_hash[user_id][1] != yesterday_date
            and current_score_hash[user_id][1] != date.today()
        ):
            if highest_score_hash[user_id][0] <= current_score_hash[user_id][0]:
                highest_score_hash[user_id][0] = current_score_hash[user_id][0]
                highest_score_hash[user_id][1] = user
            current_score_hash[user_id][0] = 1
            current_score_hash[user_id][1] = message_day

        print(f"highest {highest_score_hash}, current {current_score_hash}")

        if user_message == "/current":
            await message.channel.send(
                f"@{user} current streak is {current_score_hash[user_id][0]} days"
            )

        elif user_message == "/personal-best":
            print(highest_score_hash)
            await message.channel.send(
                f"@{user} highest streak is {highest_score_hash[user_id][0]} days"
            )

        elif user_message == "/leaderboard":
            sorted(highest_score_hash, key=highest_score_hash.get, reverse=True)
            counter = 1
            leaderboard_msg = ""
            for value in highest_score_hash.values():
                user = value[1]
                score = value[0]
                leaderboard_msg += f"{counter}. {user}: {score} days\n"
                counter += 1
            await message.channel.send(leaderboard_msg)

        elif user_message == "/help":
            await message.channel.send(
                "/current: Check current score\n"
                "/personal-best: Check personal highest score\n"
                "/leaderboard: Check top 10 leaderboard\n"
            )

    with open("currentStreaks", "w", encoding="utf-8") as file:
        file.write(str(current_score_hash))

    with open("HighestStreaks", "w", encoding="utf-8") as file:
        file.write(str(highest_score_hash))


client.run(TOKEN)
