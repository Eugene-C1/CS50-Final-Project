import discord
from discord.ext import tasks, commands
import responses
import json
import youtube
from youtube import TO_RETURN




async def send_message(message, user_message, is_private):
    if "!check" in user_message:
        try:
            response = responses.get_response(user_message)
            
            
            for username, stream in youtube.TO_RETURN.items():
                if not is_private:
                    await message.channel.send(f"@everyone {username} is live at {stream} 😁")  # Update the status
            TO_RETURN.clear()
        except Exception as e:
            print(e)
    if "help" in user_message:
        response = responses.get_response(user_message)
        await message.reply(embed=response)   
    else:
        try:
            response = responses.get_response(user_message)
            await message.author.send(response) if is_private else await message.reply(response)
     
        except Exception as e:
            print(e)
            

    
def run_discord_bot():
    TOKEN = ""
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = discord.Client(intents=intents)
    
    
    @tasks.loop(minutes=1)
    async def mytask():
        youtuber = youtube.YoutubeBot()
        check = youtuber.is_online()
        channel = client.get_channel(1146349848371666955)
        
  
        for username, stream in TO_RETURN.items():
            await channel.send(f"@everyone {username} is live at {stream} 😁")  # Update the status
    
        TO_RETURN.clear()
        
        
    @client.event
    async def on_ready():
        print(f"{client.user} is now running!")
        mytask.start()
        
        
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
    
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        print(f"{username} said: '{user_message}' ({channel})")
        
        if user_message[0] == "?":
            #user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
            
        elif user_message[0] == "!":
            await send_message(message, user_message, is_private=False)
     
  
    client.run(TOKEN)