import random
from youtube import YoutubeBot, TO_RETURN
import re

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
    
    p_message = message.lower()
    
    if p_message == "!hello":
        return "Hey There! 😁"
    
    if p_message == "!roll":
        return f"The dice rolled on {random.randint(1, 6)} 🎲"
    
    if p_message == "!help":
        return "`YOUR MESSAGE IN HERE`"
    
    if p_message == "?wordle":
        return "Start of Wordle Game"
    
    if p_message == "!check":
        youtuber = YoutubeBot()
        list_name = youtuber.is_online()
        return str(list_name)
    
    if "!notify" in p_message:
        
        temp = p_message.replace("!notify", "")
        if url := re.search(r"https://www.youtube.com/@?(.+)", temp).group(1):
            if "watch" in url:
                return "Send a youtube channel homepage"
            
            channel_url = f"https://www.youtube.com/@{url}/live"
        else:
            return "Send a Valid Youtube Link"
        
        ### calls YoutubeBot class, checks if online and gets link
        youtuber = YoutubeBot()
        youtuber.notif_save(channel_url)
        
        return f"I'll notify you if {youtuber.get_name} is online"
    
    if p_message.startswith("!playwordle"):
        chosen_word = random.choice(word_list).lower()
        wordle = Wordle(chosen_word)
        active_games = True
        return f"Wordle game started! Guess the 5-letter word. Use `!guess <word>` to guess."

    
    if p_message.startswith("!guess"):
        if not active_games:
            return f"Wordle game has not yet started! Use `!playwordle` to start a game."

        tries = wordle.get_attempts
        guess = p_message.replace("!guess", "").strip()
        
        print(f"{chosen_word} and the guess is {guess}")
        
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

    return "Incorrect Command. Check 'help' for the commands"