# messages-streaks-discordbot
A discord bot that counts the amount of days an user texted on a discord channel. The bot counts the current streak and the max streak and it also includes a leaderboard.

Intructions:

1. Install the discord and python3-dotenv modules for python
2. Open https://discord.com/developers/docs and create a new application
3. Click on the bot tab and create a new bot
4. Copy the bot's token and assign the variable TOKEN as a string
4. Create a .env file at the root of this repository
4. Copy the bot's token as `TOKEN=myBotTokenHere` in the .env file 
5. Turn on the developer mode on Discord and copy the channel's ID as `CHANNEL_ID=myChannelIDHere` in the .env file 
6. You are all set!!

Bot commands:
- Use "/current" to check your current streak
- Use "/personal-best" to check your highest streak
- Use "/leaderboard" to check the leaderboard
- Use "/help" to check the commands
