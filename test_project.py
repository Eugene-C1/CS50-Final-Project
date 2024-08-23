from responses import get_response, word_list, magic_8ball_responses, chosen_word
from random import Random

random = Random()

def test_get_response():
    global chosen_word
    
    assert get_response("!hello") == "Hey There! 😁"
    assert get_response("!hello") != "Hello There! 😁"
    assert get_response("!hi") == "Incorrect Command. Check `help` for the commands"
    
    random.seed(666)
    assert get_response("!roll") == f"The dice rolled on {random.randint(1, 6)} 🎲"
    assert get_response("!rolls") == "Incorrect Command. Check `help` for the commands"
    
    expected_embed = get_embed()
    assert get_response("!help") == expected_embed
    assert get_response("!helps") == "Incorrect Command. Check `help` for the commands"
    
    expected_8ball_answer = get_8ball_answer()
    assert get_response("!8ball should i wear my coat today?") == expected_8ball_answer
    assert get_response("!8ball should i wear my coat today?") != "No"
    assert get_response("!notify https://www.youtube.com/@MoriCalliope") == "I'll notify you if moricalliope is online"
    assert get_response("!notify https://www.youtube.com/watch?v=gNKYCKxuud4") == "Send a youtube channel homepage"
    assert get_response("!notify https://www.twitch.tv/pgl_dota2en2") == "Send a Valid Youtube Link"
    assert get_response("!guess") == "Wordle game has not yet started! Use `!playwordle` to start a game."
    assert get_response("!playwordle") == "Wordle game started! Guess the 5-letter word. Use `!guess <word>` to guess."
    assert get_response("!guess banana") == "Your guess should be a 5-letter word."
    assert get_response("!guess zzzzz") == ":black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:"
    
    
def get_embed():
    return get_response("!help")

def get_8ball_answer():
    random.seed(42)
    return get_response("!8ball should i wear my coat today?")