
import os
import discord
import requests
import time
import asyncio
import random
import json
from guess import start_quiz, guess_pokemon
from pus import PokemonPowerOfUs
from dotenv import load_dotenv
from log import setup_logger
from damage import load_learnsets, load_moves, load_pokedex
from custom_view import CustomView
from pokemon import Pokemon


load_dotenv()
logger = setup_logger(__name__)


POKEMON_PRICES = {
    "bulbasaur": 100,
    "charmander": 150,
    "squirtle": 120,
    "ivysaur": 130,
    "venusaur": 180,
    "charmeleon": 160,
    "charizard": 200,
    "wartortle": 140,
    "blastoise": 190,
    "caterpie": 50,
}
user_inventory = {}
user_currency = 500
user_xp_level = 0

POKEMON_XP = {
    "bulbasaur": 200,
    "charmander": 210,
    "squirtle": 220,
    "ivysaur": 230,
    "venusaur": 240,
    "charmeleon": 250,
    "charizard": 260,
    "wartortle": 270,
    "blastoise": 280,
    "caterpie": 290,
}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def get_pokemon_info(name):
  url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
  response = requests.get(url)
  if response.status_code == 200:
    return response.json()
  else:
    print("Error:", response.status_code)
    return None


async def get_pokemon_list():
  url = "https://pokeapi.co/api/v2/pokemon?limit=15"  # Change the limit as needed
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    return [pokemon['name'] for pokemon in data.get('results', [])]
  else:
    print("Error:", response.status_code)
    return None


async def get_pokemon_stats(pokemon_info):
  stats = pokemon_info.get('stats', [])
  return ', '.join(
      [f"{stat['stat']['name']}: {stat['base_stat']}" for stat in stats])


async def get_pokemon_types(pokemon_info):
  types = pokemon_info.get('types', [])
  return [type_entry['type']['name'] for type_entry in types]


async def format_xp_bar(user_xp_level):
  xp_req = (user_xp_level + 1) * 100
  xp_progress = user_xp_level * 100
  xp_bar = f"XP: Level {user_xp_level} ({xp_progress}/ {xp_req})"
  return xp_bar


async def format_pokemon_list(pokemon_list):
  formatted_list = "Welcome! Here's a list of available Pokémon:\n"
  for pokemon in pokemon_list:
    pokemon_info = await get_pokemon_info(pokemon)
    if pokemon_info:
      stats = await get_pokemon_stats(pokemon_info)
      types = await get_pokemon_types(pokemon_info)
      formatted_list += f"- {pokemon.capitalize()} (Stats: {stats}, Types: {', '.join(types)})\n"
    else:
      formatted_list += f"- {pokemon.capitalize()} (Not found)\n"
  return formatted_list


async def get_pokemon_image_urls(pokemon_info):
  if not pokemon_info:
    return None
  sprites = pokemon_info.get('sprites', {})
  return {'front_default': sprites.get('front_default')}


async def buy_pokemon(message, pokemon_name):
  global user_inventory, user_currency, user_xp_level
  if pokemon_name in POKEMON_PRICES:
    if POKEMON_PRICES[pokemon_name] <= user_currency:
      user_currency -= POKEMON_PRICES[pokemon_name]
      user_inventory[pokemon_name] = user_inventory.get(pokemon_name, 0) + 1
      user_xp_level += POKEMON_XP.get(pokemon_name, 0)
      await message.channel.send(
          f"You bought {pokemon_name.capitalize()}! Your remaining currency: {user_currency}"
      )
    else:
      await message.channel.send("Not enough currency to buy this Pokémon.")
  else:
    await message.channel.send("Invalid Pokémon name.")


async def sell_pokemon(message, pokemon_name):
  global user_inventory, user_currency
  if pokemon_name in user_inventory and user_inventory[pokemon_name] > 0:
    user_currency += POKEMON_PRICES.get(pokemon_name, 0) // 2
    user_inventory[pokemon_name] -= 1
    await message.channel.send(
        f"You sold {pokemon_name.capitalize()}! Your updated currency: {user_currency}"
    )
  else:
    await message.channel.send("You don't have this Pokémon in your inventory."
                               )


async def handle_lootbox(message):
  global user_inventory, user_currency, user_xp_level
  reward_type = random.choice(["xp", "currency", "rare"])
  if reward_type == "xp":
    reward = random.choice([50, 100, 150, 200])
    user_xp_level += reward
    await message.channel.send(
        f"You received {reward} XP! Your XP level is now {user_xp_level}.")
  elif reward_type == "currency":
    reward = random.choice([50, 100, 150, 200])
    user_currency += reward
    await message.channel.send(
        f"You received {reward} currency! Your total currency is now {user_currency}."
    )
  elif reward_type == "rare":
    rare_rewards = ["Squirtle", "Charmander", "Pikachu"]
    rare_probabilities = [0.1, 0.1, 0.1]
    if random.random() < sum(rare_probabilities):
      rare_reward = random.choices(rare_rewards, weights=rare_probabilities)[0]
      user_inventory[rare_reward.lower()] = user_inventory.get(
          rare_reward.lower(), 0) + 1
      user_xp_level += POKEMON_XP.get(rare_reward.lower(), 0)
      await message.channel.send(
          f"Congratulations! You caught a rare {rare_reward}! Check your inventory."
      )
    else:
      await message.channel.send("You received a common reward.")


async def register_user(ctx):
  user_id = ctx.author.id
  username = ctx.author.name
  user_data = {
      "id": user_id,
      "username": username,
      "profile_id":
      random.randint(1, 10)  # Generate a random profile ID between 1 and 10
  }
  with open("user_data.json", "r+") as file:
    data = json.load(file)
    if str(user_id) not in data:
      data[str(user_id)] = user_data
      file.seek(0)
      json.dump(data, file, indent=4)
      await ctx.send(
          f"Hello {username}! Your profile has been registered with profile ID {user_data['profile_id']}."
      )


async def get_user_profile(ctx):
  user_id = str(ctx.author.id)
  if not os.path.exists("user_data.json"):
    with open("user_data.json", "w") as file:
      json.dump({}, file)
    await register_user(ctx)
  else:
    with open("user_data.json", "r") as file:
      data = json.load(file)
      return data.get(user_id, {}).get("username", None)


async def gamest(message):
  game = PokemonPowerOfUs(message)
  game.loop = asyncio.get_event_loop()
  await game.power_of_us_intro()




API_URL = "https://pokemontrivia-1-c0774976.deta.app/trivia?endpoint=images"


def get_trivia_question():
  response = requests.get(API_URL)
  data = response.json()
  specific_data = data.get("specific", {})
  return specific_data.get("image"), specific_data.get(
      "imageText"), specific_data.get("word"), specific_data.get("hints")


# Function to check if the user's answer is correct
def is_correct_answer(user_answer, correct_answer):
  return user_answer.lower() == correct_answer.lower()


# Function to play the trivia game
async def play_trivia_game(message):
  image_url, question, answer, hints = get_trivia_question()
  await message.channel.send(
      f"Question: {question}\n\n{image_url}\n\nWhat is your answer? (Type '$hint' for a hint)"
  )

  try:
    user_response = await client.wait_for(
        "message", check=lambda m: m.author == message.author, timeout=30)
  except asyncio.TimeoutError:
    await message.channel.send("Time's up! Better luck next time.")
    return

  if user_response.content.lower() == "$hint":
    await message.channel.send(f"Hints: {', '.join(hints)}")
    try:
      user_response = await client.wait_for(
          "message", check=lambda m: m.author == message.author, timeout=30)
    except asyncio.TimeoutError:
      await message.channel.send("Time's up! Better luck next time.")
      return

  if is_correct_answer(user_response.content, answer):
    await message.channel.send("Yay, you're right!")
  else:
    await message.channel.send(
        f"Sorry, the correct answer was {answer}. Better luck next time.")
    
    
async def battle(message):
  


# Event handler for when a message is received
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.lower() == "$exit":
    await message.channel.send("Thanks for playing! Goodbye.")
    await client.close()
    return

  await play_trivia_game(message)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  #await load_user_profiles()


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    #await register_user(message)
    await message.channel.send("Hello")

  if message.content.startswith('$help'):
    await message.channel.send(
        'Hello! I am a bot that can help you with your Discord server. I can do a lot of things.'
    )

  if message.content.startswith('$list'):
    pokemon_list = await get_pokemon_list()
    if pokemon_list:
      formatted_list = await format_pokemon_list(pokemon_list)
      await message.channel.send(formatted_list)
    else:
      await message.channel.send("Error fetching Pokémon list.")

  if message.content.startswith('$pokemon'):
    pokemon_name = message.content.split(' ', 1)[1]
    pokemon_info = await get_pokemon_info(pokemon_name)
    if pokemon_info:
      await message.channel.send(f"Pokemon Info for {pokemon_name}:")
      await message.channel.send(f"Name: {pokemon_info['name']}")
      await message.channel.send(f"Height: {pokemon_info['height']}")
      await message.channel.send(f"Weight: {pokemon_info['weight']}")
      abilities = [
          ability['ability']['name'] for ability in pokemon_info['abilities']
      ]
      await message.channel.send(f"Abilities: {', '.join(abilities)}")
      image_urls = await get_pokemon_image_urls(pokemon_info)
      if image_urls:
        await message.channel.send(
            f"Front Sprite URL: {image_urls['front_default']}")
    else:
      await message.channel.send(f"Pokemon {pokemon_name} not found.")

  if message.content.startswith('$marketplace'):
    await message.channel.send(
        "Welcome to the Pokémon Marketplace! Use the following commands:")
    await message.channel.send(
        "- `$buy <pokemon>`: Buy a Pokémon from the marketplace.")
    await message.channel.send(
        "- `$sell <pokemon>`: Sell a Pokémon to the marketplace.")
    await message.channel.send("- `$inventory`: View your Pokémon inventory.")
    await message.channel.send("- `$lootbox`: Open a lootbox.")

  if message.content.startswith('$buy'):
    pokemon_name = message.content.split(' ', 1)[1].lower()
    await buy_pokemon(message, pokemon_name)

  if message.content.startswith('$sell'):
    pokemon_name = message.content.split(' ', 1)[1].lower()
    await sell_pokemon(message, pokemon_name)

  if message.content.startswith('$inventory'):
    if user_inventory:
      inventory_list = "Your Pokémon Inventory:\n"
      for pokemon, count in user_inventory.items():
        inventory_list += f"- {pokemon.capitalize()} (Count: {count})\n"
      await message.channel.send(inventory_list)
    else:
      await message.channel.send("Your inventory is empty.")

  if message.content.startswith('$lootbox'):
    await handle_lootbox(message)

  if message.content.startswith('$startquiz'):
    await start_quiz(message)

  if message.content.startswith('$guess'):
    await guess_pokemon(message)

  if message.content.startswith('$Sign_in'):
    await register_user(message)

  if message.content.startswith('$Info'):
    username = await get_user_profile(message)
    if username:
      await message.channel.send(f"User's username: {username}")
    else:
      await message.channel.send("User not found in user_data.json")

  if message.content.startswith('$story_mode'):
    await message.channel.send(
        "Welcome to the game based on The Movie : Pokemon: The Power Of Us")
    await gamest(message)

  if message.content.startswith("$Trivia"):
    await play_trivia_game(message)


try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
  if e.status == 429:
    print(
        "The Discord servers denied the connection for making too many requests"
    )



async def register_user(ctx):
  user_id = ctx.author.id
  username = ctx.author.name
  user_data = {
      "id": user_id,
      "username": username,
      "profile_id":
      random.randint(1, 10)  # Generate a random profile ID between 1 and 10
  }
  with open("user_data.json", "r+") as file:
    data = json.load(file)
    if str(user_id) not in data:
      data[str(user_id)] = user_data
      file.seek(0)
      json.dump(data, file, indent=4)
      await ctx.send(
          f"Hello {username}! Your profile has been registered with profile ID {user_data['profile_id']}."
      )


async def get_user_profile(ctx):
  user_id = str(ctx.author.id)
  if not os.path.exists("user_data.json"):
    with open("user_data.json", "w") as file:
      json.dump({}, file)
    await register_user(ctx)
  else:
    with open("user_data.json", "r") as file:
      data = json.load(file)
      return data.get(user_id, {}).get("username", None)


async def gamest(message):
  game = PokemonPowerOfUs(message)
  game.loop = asyncio.get_event_loop()
  await game.power_of_us_intro()

async def load_pokemon(battle):
  for i in range(3):
    pokemon_id = random.randit(1,400)
    pokemon_Data = requests.get(f"{POKEMON_URL}/{pokemon_id}").json()
    battle["pokemons1"].append(pokemon_data)
    
  for j in range(3):   
    pokemon_id = random.randint(1, 400)
    pokemon_data = requests.get(f"{POKEAPI_URL}/pokemon/{pokemon_id}").json()
    battle["pokemons2"].append(pokemon_data)

async def start_battle(battle):
  while battle["round"] < 3:
    await battle_round(battle)
    battle["round"] += 1
    
async def battle_round(battle):
  player1 = battle["player1"]
  player2 = battle["player2"]
  round_num = battle["round"]
    






API_URL = "https://pokemontrivia-1-c0774976.deta.app/trivia?endpoint=images"


def get_trivia_question():
  response = requests.get(API_URL)
  data = response.json()
  specific_data = data.get("specific", {})
  return specific_data.get("image"), specific_data.get(
      "imageText"), specific_data.get("word"), specific_data.get("hints")


# Function to check if the user's answer is correct
def is_correct_answer(user_answer, correct_answer):
  return user_answer.lower() == correct_answer.lower()


# Function to play the trivia game
async def play_trivia_game(message):
  image_url, question, answer, hints = get_trivia_question()
  await message.channel.send(
      f"Question: {question}\n\n{image_url}\n\nWhat is your answer? (Type '$hint' for a hint)"
  )

  try:
    user_response = await client.wait_for(
        "message", check=lambda m: m.author == message.author, timeout=30)
  except asyncio.TimeoutError:
    await message.channel.send("Time's up! Better luck next time.")
    return

  if user_response.content.lower() == "$hint":
    await message.channel.send(f"Hints: {', '.join(hints)}")
    try:
      user_response = await client.wait_for(
          "message", check=lambda m: m.author == message.author, timeout=30)
    except asyncio.TimeoutError:
      await message.channel.send("Time's up! Better luck next time.")
      return

  if is_correct_answer(user_response.content, answer):
    await message.channel.send("Yay, you're right!")
  else:
    await message.channel.send(
        f"Sorry, the correct answer was {answer}. Better luck next time.")


# Event handler for when a message is received
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.lower() == "$exit":
    await message.channel.send("Thanks for playing! Goodbye.")
    await client.close()
    return

  await play_trivia_game(message)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  #await load_user_profiles()


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    #await register_user(message)
    await message.channel.send("Hello")

  if message.content.startswith('$help'):
    await message.channel.send(
        'Hello! I am a bot that can help you with your Discord server. I can do a lot of things.'
    )

  if message.content.startswith('$list'):
    pokemon_list = await get_pokemon_list()
    if pokemon_list:
      formatted_list = await format_pokemon_list(pokemon_list)
      await message.channel.send(formatted_list)
    else:
      await message.channel.send("Error fetching Pokémon list.")

  if message.content.startswith('$pokemon'):
    pokemon_name = message.content.split(' ', 1)[1]
    pokemon_info = await get_pokemon_info(pokemon_name)
    if pokemon_info:
      await message.channel.send(f"Pokemon Info for {pokemon_name}:")
      await message.channel.send(f"Name: {pokemon_info['name']}")
      await message.channel.send(f"Height: {pokemon_info['height']}")
      await message.channel.send(f"Weight: {pokemon_info['weight']}")
      abilities = [
          ability['ability']['name'] for ability in pokemon_info['abilities']
      ]
      await message.channel.send(f"Abilities: {', '.join(abilities)}")
      image_urls = await get_pokemon_image_urls(pokemon_info)
      if image_urls:
        await message.channel.send(
            f"Front Sprite URL: {image_urls['front_default']}")
    else:
      await message.channel.send(f"Pokemon {pokemon_name} not found.")

  if message.content.startswith('$marketplace'):
    await message.channel.send(
        "Welcome to the Pokémon Marketplace! Use the following commands:")
    await message.channel.send(
        "- `$buy <pokemon>`: Buy a Pokémon from the marketplace.")
    await message.channel.send(
        "- `$sell <pokemon>`: Sell a Pokémon to the marketplace.")
    await message.channel.send("- `$inventory`: View your Pokémon inventory.")
    await message.channel.send("- `$lootbox`: Open a lootbox.")

  if message.content.startswith('$buy'):
    pokemon_name = message.content.split(' ', 1)[1].lower()
    await buy_pokemon(message, pokemon_name)

  if message.content.startswith('$sell'):
    pokemon_name = message.content.split(' ', 1)[1].lower()
    await sell_pokemon(message, pokemon_name)

  if message.content.startswith('$inventory'):
    if user_inventory:
      inventory_list = "Your Pokémon Inventory:\n"
      for pokemon, count in user_inventory.items():
        inventory_list += f"- {pokemon.capitalize()} (Count: {count})\n"
      await message.channel.send(inventory_list)
    else:
      await message.channel.send("Your inventory is empty.")

  if message.content.startswith('$lootbox'):
    await handle_lootbox(message)

  if message.content.startswith('$startquiz'):
    await start_quiz(message)

  if message.content.startswith('$guess'):
    await guess_pokemon(message)

  if message.content.startswith('$Sign_in'):
    await register_user(message)

  if message.content.startswith('$Info'):
    username = await get_user_profile(message)
    if username:
      await message.channel.send(f"User's username: {username}")
    else:
      await message.channel.send("User not found in user_data.json")

  if message.content.startswith('$story_mode'):
    await message.channel.send(
        "Welcome to the game based on The Movie : Pokemon: The Power Of Us")
    await gamest(message)

  if message.content.startswith("$Trivia"):
    await play_trivia_game(message)
    
  if message.content.startswith("$battle"):
    if message.author.id in battles:
      await message.channel.send("You are already in a battle!")
      return
    
    battles[message.author.id] = {
      "player1": message.author,
      "player2": None,
      "round":0,
      "pokemons1":[],
      "pokemons2":[],
      "timeout": 60
    }
    
    await message.channel.send(f"{message.author.mention} has started a battle!\n Waiting for the opponent to tjoin...")
    
  elif message.content.startswith("join"):
    if message.author.id not in battle:
      await message.channel.send("You are not in a battle!")
      return
    
    if battles[message.author.id]["player2"]:
            await message.channel.send("This battle already has two players!")
            return

        
    battles[message.author.id]["player2"] = message.author
    await message.channel.send(f"{message.author.mention} has joined the battle!")

        
    await load_pokemons(battles[message.author.id])

    
    await start_battle(battles[message.author.id])
    

try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
  if e.status == 429:
    print(
        "The Discord servers denied the connection for making too many requests"
    )
