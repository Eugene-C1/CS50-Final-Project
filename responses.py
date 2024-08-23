from random import Random
from youtube_module import YoutubeBot, TO_RETURN
import re

import discord
from discord.ext import commands

# List of possible words for the game
word_list = [
    "About", "Alert", "Argue", "Beach",
    "Above", "Alike", "Arise", "Began",
    "Abuse", "Alive", "Array", "Begin",
    "Actor", "Allow", "Aside", "Begun",
    "Acute", "Alone", "Asset", "Being",
    "Admit", "Along", "Audio", "Below",
    "Adopt", "Alter", "Audit", "Bench",
    "Adult", "Among", "Avoid", "Billy",
    "After", "Anger", "Award", "Birth",
    "Again", "Angle", "Aware", "Black",
    "Agent", "Angry", "Badly", "Blame",
    "Agree", "Apart", "Baker", "Blind",
    "Ahead", "Apple", "Bases", "Block",
    "Alarm", "Apply", "Basic", "Blood",
    "Album", "Arena", "Basis", "Board",
    "Boost", "Buyer", "China", "Cover",
    "Booth", "Cable", "Chose", "Craft",
    "Bound", "Calif", "Civil", "Crash",
    "Brain", "Carry", "Claim", "Cream",
    "Brand", "Catch", "Class", "Crime",
    "Bread", "Cause", "Clean", "Cross",
    "Break", "Chain", "Clear", "Crowd",
    "Breed", "Chair", "Click", "Crown",
    "Brief", "Chart", "Clock", "Curve",
    "Bring", "Chase", "Close", "Cycle",
    "Broad", "Cheap", "Coach", "Daily",
    "Broke", "Check", "Coast", "Dance",
    "Brown", "Chest", "Could", "Dated",
    "Build", "Chief", "Count", "Dealt",
    "Built", "Child", "Court", "Death",
    "Debut", "Entry", "Forth", "Group",
    "Delay", "Equal", "Forty", "Grown",
    "Depth", "Error", "Forum", "Guard",
    "Doing", "Event", "Found", "Guess",
    "Doubt", "Every", "Frame", "Guest",
    "Dozen", "Exact", "Frank", "Guide",
    "Draft", "Exist", "Fraud", "Happy",
    "Drama", "Extra", "Fresh", "Harry",
    "Drawn", "Faith", "Front", "Heart",
    "Dream", "False", "Fruit", "Heavy",
    "Dress", "Fault", "Fully", "Hence",
    "Drill", "Fibre", "Funny", "Night",
    "Drink", "Field", "Giant", "Horse",
    "Drive", "Fifth", "Given", "Hotel",
    "Drove", "Fifty", "Glass", "House",
    "Dying", "Fight", "Globe", "Human",
    "Eager", "Final", "Going", "Ideal",
    "Early", "First", "Grace", "Image",
    "Earth", "Fixed", "Grade", "Index",
    "Eight", "Flash", "Grand", "Inner",
    "Elite", "Fleet", "Grant", "Input",
    "Empty", "Floor", "Grass", "Issue",
    "Enemy", "Fluid", "Great", "Irony",
    "Enjoy", "Focus", "Green", "Juice",
    "Enter", "Force", "Gross", "Joint",
    "Judge", "Metal", "Media", "Newly",
    "Known", "Local", "Might", "Noise",
    "Label", "Logic", "Minor", "North",
    "Large", "Loose", "Minus", "Noted",
    "Laser", "Lower", "Mixed", "Novel",
    "Later", "Lucky", "Model", "Nurse",
    "Laugh", "Lunch", "Money", "Occur",
    "Layer", "Lying", "Month", "Ocean",
    "Learn", "Magic", "Moral", "Offer",
    "Lease", "Major", "Motor", "Often",
    "Least", "Maker", "Mount", "Order",
    "Leave", "March", "Mouse", "Other",
    "Legal", "Music", "Mouth", "Ought",
    "Level", "Match", "Movie", "Paint",
    "Light", "Mayor", "Needs", "Paper",
    "Limit", "Meant", "Never", "Party",
    "Peace", "Power", "Radio", "Round",
    "Panel", "Press", "Raise", "Route",
    "Phase", "Price", "Range", "Royal",
    "Phone", "Pride", "Rapid", "Rural",
    "Photo", "Prime", "Ratio", "Scale",
    "Piece", "Print", "Reach", "Scene",
    "Pilot", "Prior", "Ready", "Scope",
    "Pitch", "Prize", "Refer", "Score",
    "Place", "Proof", "Right", "Sense",
    "Plain", "Proud", "Rival", "Serve",
    "Plane", "Prove", "River", "Seven",
    "Plant", "Queen", "Quick", "Shall",
    "Plate", "Sixth", "Stand", "Shape",
    "Point", "Quiet", "Roman", "Share",
    "Pound", "Quite", "Rough", "Sharp",
    "Sheet", "Spare", "Style", "Times",
    "Shelf", "Speak", "Sugar", "Tired",
    "Shell", "Speed", "Suite", "Title",
    "Shift", "Spend", "Super", "Today",
    "Shirt", "Spent", "Sweet", "Topic",
    "Shock", "Split", "Table", "Total",
    "Shoot", "Spoke", "Taken", "Touch",
    "Short", "Sport", "Taste", "Tough",
    "Shown", "Staff", "Taxes", "Tower",
    "Sight", "Stage", "Teach", "Track",
    "Since", "Stake", "Teeth", "Trade",
    "Sixty", "Start", "Texas", "Treat",
    "Sized", "State", "Thank", "Trend",
    "Skill", "Steam", "Theft", "Trial",
    "Sleep", "Steel", "Their", "Tried",
    "Slide", "Stick", "Theme", "Tries",
    "Small", "Still", "There", "Truck",
    "Smart", "Stock", "These", "Truly",
    "Smile", "Stone", "Thick", "Trust",
    "Smith", "Stood", "Thing", "Truth",
    "Smoke", "Store", "Think", "Twice",
]

# List of responses for the Magic 8-Ball
magic_8ball_responses = [
    "Yes",
    "No",
    "Maybe",
    "Ask again later",
    "It is certain",
    "Without a doubt",
    "Cannot predict now",
    "Don't count on it",
    "Most likely",
    "Outlook not so good"
]

chosen_word = str()
active_games = False

class Wordle:
    def __init__(self, word):
        self.word = word
        self.guesses = []
        self._tries = 0

    def get_feedback(self, guess):
        feedback = ""
        correct_word = self.word
        self.add_attempts()
        
        for i in range(len(correct_word)):
            if guess[i] == correct_word[i]:
                green_square = ":green_square:"
                feedback += green_square
            elif guess[i] in correct_word:
                yellow_square = ":yellow_square:"
                feedback += yellow_square
            else:
                black_square = ":black_large_square:"
                feedback += black_square
                
        return feedback
        
    @property
    def get_attempts(self):
        return self._tries
    
    @property
    def get_word(self):
        return self.word
    
    def add_attempts(self):
        self._tries += 1



def get_response(message: str) -> str:
    global chosen_word
    global wordle
    global active_games
    
    random = Random()
    p_message = message.lower()
    
    if p_message == "!hello":
        return "Hey There! 😁"
    
    if p_message == "!roll":
        random.seed(666)
        return f"The dice rolled on {random.randint(1, 6)} 🎲"
    
    if p_message == "!help":
        embed = discord.Embed(title="Command List", description="List of available commands and their descriptions:")
        
        embed.add_field(name="`!8ball`", value="A magic 8 ball that will answer your question.", inline=False)
        embed.add_field(name="`!guess`", value="Guess the 5-letter word.", inline=False)
        embed.add_field(name="`!hello`", value="The bot will reply with a greeting.", inline=False)
        embed.add_field(name="`!help`", value="Shows a list of available commands and their descriptions.", inline=False)
        embed.add_field(name="`!notify`", value="Notifies the user using a link from a YouTube channel homepage. Example: `https://www.youtube.com/@NinomaeInanis`", inline=False)
        embed.add_field(name="`!playwordle`", value="Starts a game of Wordle.", inline=False)
        embed.add_field(name="`!roll`", value="Rolls a number from 1 to 6.", inline=False)
        embed.add_field(name=" ", value=" ", inline=False)
        
        embed.set_footer(text="Feel free to reach out to me @klake regarding any bugs or glitches, and I will promptly work to address and resolve them.")
            
        return embed

    if "!8ball" in p_message:
        question = p_message
        new_question = question.replace("!8ball", "")
        random.seed(42)
        answer = random.choice(magic_8ball_responses)
        
        return f'Answer: `{answer}`'
        
        
    if p_message == "!check":
        youtuber = YoutubeBot()
        list_name = youtuber.is_online()
        return str(list_name)
    
    if "!notify" in p_message:
        
        temp = p_message.replace("!notify", "")
        try:
            if url := re.search(r"https://www.youtube.com/@?(.+)", temp).group(1):
                if "watch" in url:
                    return "Send a youtube channel homepage"
                
                channel_url = f"https://www.youtube.com/@{url}/live"
        except AttributeError:
            return "Send a Valid Youtube Link"
        
        ### calls YoutubeBot class, checks if online and gets link
        print(channel_url)
        youtuber = YoutubeBot()
        youtuber.notif_save(channel_url)
        
        return f"I'll notify you if {youtuber.get_name} is online"
    
    if p_message.startswith("!playwordle"):
        
        chosen_word = random.choice(word_list).lower()
        wordle = Wordle(chosen_word)
        active_games = True
        return "Wordle game started! Guess the 5-letter word. Use `!guess <word>` to guess."

    
    if p_message.startswith("!guess"):
        if not active_games:
            return f"Wordle game has not yet started! Use `!playwordle` to start a game."

        tries = wordle.get_attempts
        guess = p_message.replace("!guess", "").strip()
        
        print(f"correct answer is {wordle.get_word}")
        
        if len(guess) != 5:
            return "Your guess should be a 5-letter word."
        
        if guess == str(wordle.get_word):
            wordle.add_attempts()
            active_games = False
            return f"Congratulations! You guessed the word `{guess}` in {wordle.get_attempts} attempts."
        elif tries == 6:
            active_games = False
            return f"Game Over! The correct word is `{wordle.get_word}`"
        else:
            result = wordle.get_feedback(guess)
            return f"{result}"

    return "Incorrect Command. Check `help` for the commands"