import discord
import json
import responses
import sys
import youtube_module
from youtube_module import TO_RETURN
from discord.ext import tasks, commands

async def send_message(message, user_message, is_private):
    if "!check" in user_message:
        try:
            response = responses.get_response(user_message)
            
            
            for username, stream in youtube_module.TO_RETURN.items():
                if not is_private:
                    await message.channel.send(f"@everyone {username} is live at {stream} 😁")  # Update the status
            TO_RETURN.clear()
        except Exception as e:
            print(e)
    elif "help" in user_message:
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
        youtuber = youtube_module.YoutubeBot()
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

def pre_run_checks():
    
    #Example of checking necessary modules
    required_modules = [
        'discord', 'responses', 'json', 'youtube_module'
    ]
    missing_modules = [module for module in required_modules if module not in globals()]
    if missing_modules:
        print("Missing required modules:", ', '.join(missing_modules))
        return False
    
    # Check if necessary tokens/credentials are available
    TOKEN = ""
    if not TOKEN:
        print("Discord bot token is missing. Please provide your token.")
        return False
    
    # Check if intents are defined
    try:
        intents = discord.Intents.default()
        intents.message_content = True
    except AttributeError:
        print("discord.Intents.default() is not available. Please check your discord.py version.")
        return False
    
    # All checks passed
    return True

def main():
    check = pre_run_checks()
    if check:  
        run_discord_bot()
    else:
        sys.exit("Failed Pre Run Checks")    
    
    

if __name__ == "__main__":
    main()

    