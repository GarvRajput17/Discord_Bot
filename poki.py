import os
import discord
import requests
import time
import asyncio
import random
import json
from guess import start_quiz, guess_pokemon
from pus import PokemonPowerOfUs
from battle import join, start_game
from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle
from discord import Embed
import aiohttp




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

POTION_PRICES = {
    "potion": 50,
    "super_potion": 100,
    "hyper_potion": 200,
}

# Prices for Berries
BERRY_PRICES = {
    "oran_berry": 20,
    "sitrus_berry": 50,
    "wiki_berry": 100,
}
user_inventory = []
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
      async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
          if response.status == 200:
            return await response.json()
          else:
            print("Error:", response.status)
            return None


def get_pokemon_list():
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


async def buy_item(message, item_name, price_dict):
  global user_inventory, user_currency, user_xp_level
  if item_name in price_dict:
    if price_dict[item_name] <= user_currency:
      user_currency -= price_dict[item_name]
      user_inventory.append(item_name)  # Add purchased item to inventory
      await update_user_data(message.author.id, user_inventory, user_currency,
                             user_xp_level)
      await message.channel.send(
          f"You bought {item_name.capitalize()}! Your remaining currency: {user_currency}"
      )
    else:
      await message.channel.send("Not enough currency to buy this item.")


async def sell_item(message, item_name, price_dict):
  global user_inventory, user_currency, user_xp_level
  if item_name in price_dict:
    if item_name in user_inventory:
      user_currency += price_dict[item_name]
      user_inventory.remove(item_name)  # Add purchased item to inventory
      await update_user_data(message.author.id, user_inventory, user_currency,
                             user_xp_level)
      await message.channel.send(
          f"You sold {item_name.capitalize()}! Your remaining currency: {user_currency}"
      )
    else:
      await message.channel.send("You do not own this pokemon.")


# Modify the spawn_random_pokemon function
async def spawn_random_pokemon():
  while True:
    await asyncio.sleep(180)  # Wait for 5 minutes

    # Replace "CHANNEL_NAME" with the name of your channel
    channel = discord.utils.get(client.get_all_channels(), name="poki2")

    if channel:
      # Select a random Pokémon
      pokemon_name = random.choice(list(POKEMON_PRICES.keys()))

      # Get Pokémon info
      pokemon_info = await get_pokemon_info(pokemon_name)
      if pokemon_info:
        # Get Pokémon image URL
        image_urls = await get_pokemon_image_urls(pokemon_info)
        if image_urls and image_urls['front_default']:
          # Send message with Pokémon name and picture
          embed = discord.Embed(
              title=f"A wild {pokemon_name.capitalize()} appeared!",
              color=discord.Color.green())
          embed.set_image(url=image_urls['front_default'])
          # Set the message to throw Pokéball
          embed.set_footer(text="Throw your Pokéball to catch the Pokémon")
          # Set Pokéball image URL
          pokéball_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"
          embed.set_thumbnail(url=pokéball_url)
          spawn_message = await channel.send(embed=embed)
          # Add the Pokéball reaction
          await spawn_message.add_reaction(
              "🤾🏻‍♂️")  # Using soccer ball as a placeholder for Pokéball

          # Allow users to react to catch the Pokémon
          def check(reaction, user):
            return user != client.user and str(
                reaction.emoji
            ) == '🤾🏻‍♂️' and reaction.message == spawn_message

          try:
            reaction, user = await client.wait_for('reaction_add',
                                                   timeout=60.0,
                                                   check=check)
          except asyncio.TimeoutError:
            await spawn_message.edit(content="The wild Pokémon fled!")
          else:
            # Add the caught Pokémon to the user's inventory
            user_inventory.append(pokemon_name)
            await update_user_data(user.id, user_inventory, user_currency,
                                   user_xp_level)
            await spawn_message.edit(
                content=
                f"Congratulations {user.mention}! You caught a {pokemon_name.capitalize()}!"
            )
        else:
          print(f"Image not found for {pokemon_name.capitalize()}")
      else:
        print(f"Pokemon {pokemon_name.capitalize()} not found")
    else:
      print("Channel not found")


# Add this coroutine function to your client's event loop


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
      random.randint(1, 50),  # Generate a random profile ID between 1 and 10
      "inventory": [],
      "currency": 500,
      "collectibles": {
          "Poke Balls": ["poke_ball", "great_ball", "ultra_ball"],
          "Potions": ["potion", "super_potion", "hyper_potion"],
          "Berries": ["oran_berry", "sitrus_berry", "wiki_berry"],
      },
      "badges_count": 0,
      "badges": []
  }
  await update_user_data(user_id, user_data["inventory"],
                         user_data["currency"], user_xp_level)
  await ctx.send(
      f"Hello {username}! Your profile has been registered with profile ID {user_data['profile_id']}."
  )


async def update_user_data(user_id, inventory, currency, xp_level):
  with open("user_data.json", "r+") as file:
    data = json.load(file)
    if str(user_id) not in data:
      data[str(user_id)] = {}
    data[str(user_id)]["inventory"] = inventory
    data[str(user_id)]["currency"] = currency
    data[str(user_id)]["xp_level"] = xp_level
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()


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


async def gamest(message, bot):
  game = PokemonPowerOfUs(message, bot)
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

      embed = discord.Embed(title="Trivia Game", color=discord.Color.gold())
      embed.add_field(name="Question", value=question, inline=False)
      embed.set_image(url=image_url)

      await message.channel.send(embed=embed)
      await message.channel.send("What is your answer? (Type '$hint' for a hint)")

      try:
          user_response = await client.wait_for(
              "message", check=lambda m: m.author == message.author, timeout=30)
      except asyncio.TimeoutError:
          await message.channel.send("Time's up! Better luck next time.")
          return

      if user_response.content.lower() == "$hint":
          hint_embed = discord.Embed(title="Hints",
                                     description=', '.join(hints),
                                     color=discord.Color.blue())
          await message.channel.send(embed=hint_embed)
          try:
              user_response = await client.wait_for(
                  "message", check=lambda m: m.author == message.author, timeout=30)
          except asyncio.TimeoutError:
              await message.channel.send("Time's up! Better luck next time.")

      if is_correct_answer(user_response.content, answer):
          await message.channel.send("Yay, you're right!")
      else:
          await message.channel.send(
              f"Sorry, the correct answer was {answer}. Better luck next time.")

      if user_response.content.lower() == "$exit":
          await message.channel.send("Thanks for playing! Goodbye.")
          
          return
      else:
          await play_trivia_game(message)


TCGDEX_API_URL = "https://api.tcgdex.net/v2/en/cards"
DECKS_FILE = "decks.json"


# Function to fetch a random Pokémon card
async def get_random_pokemon_card(message):
          try:
              response = requests.get(TCGDEX_API_URL)
              response.raise_for_status()  # Raise an exception for HTTP errors
              card_data = response.json()
              max_local_id = 400
              random_local_id = random.randint(1, max_local_id)
              for card in card_data:
                  if card.get("localId") == str(random_local_id):
                      card_name = card.get("name")
                      image_url = card.get("image") + "/high.webp"
                      user_id = str(message.author.id)
                      if user_id not in decks:
                          decks[user_id] = []
                      card_id = card.get("localId")
                      decks[user_id].append({
                          "name": card_name,
                          "image_url": image_url,
                          "card_id": card_id
                      })
                      save_decks(decks)
                      embed = discord.Embed(title="Added to Your Deck!", description=f"Added {card_name} to your deck!", color=discord.Color.green())
                      embed.set_image(url=image_url)
                      await message.channel.send(embed=embed)
                      return  # Exit the function after processing
              await message.channel.send("No Pokémon card found for the specified local ID.")
          except (requests.RequestException, KeyError) as e:
              print("Error fetching random Pokémon card:", e)
              await message.channel.send("An error occurred while fetching a Pokémon card.")




# Function to create a button row for a card
def create_card_button(card):
  return Button(style=discord.ButtonStyle.green,
                label=card["name"],
                custom_id=str(card["id"]))


# Load existing decks from the JSON file
def load_decks():
  if os.path.exists(DECKS_FILE):
    with open(DECKS_FILE, "r") as file:
      return json.load(file)
  return {}


# Save decks to the JSON file
def save_decks(decks):
  with open(DECKS_FILE, "w") as file:
    json.dump(decks, file, indent=4)


decks = load_decks()


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


client = commands.Bot(command_prefix="$", intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  client.loop.create_task(spawn_random_pokemon())


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
      # Create an interactive and friendly greeting message
      greeting_message = f"Hello there, {message.author.mention}! 😊"
      greeting_message += "\n\nWelcome to our Pokémon Discord server! 🌟"
      greeting_message += "\n\nI'm here to assist you with all your Pokémon needs. If you have any questions or need help, just let me know!"
      greeting_message += "\n\nHere are some things I can do for you:"
      greeting_message += "\n- Use `$pokemon <name>` to get detailed information about a specific Pokémon."
      greeting_message += "\n- Use `$marketplace` to explore the Pokémon Marketplace."
      greeting_message += "\n- Use `$startquiz` to start a Pokémon quiz."
      greeting_message += "\n- Use `$guess` to guess the name of a Pokémon."
      greeting_message += "\n- Use `$start_game` to start a Pokémon battle game."
      greeting_message += "\n- Use `$story_mode` to play a Pokémon story-based game."
      greeting_message += "\n\nFeel free to explore and have fun! If you need assistance, just ask. Enjoy your time here! 🎉"

      # Create an embed with the greeting message
      embed = discord.Embed(title="Welcome to the Pokémon Discord Server! 🌟", description=greeting_message, color=discord.Color.green())

      # Add a thumbnail image
      embed.set_thumbnail(url="https://cdn2.bulbagarden.net/upload/thumb/9/98/Pok%C3%A9_Ball_PMS.png/1200px-Pok%C3%A9_Ball_PMS.png")

      # Send the embedded greeting message
      await message.channel.send(embed=embed)
    

  if message.content.startswith('$help'):
      # Create an embed
      embed = discord.Embed(
          title="Bot Commands",
          description="Hello! I am a bot that can help you with your Discord server. I can do a lot of things.",
          color=discord.Color.blue()  # You can change the color if you want
      )

      # Add fields for each command
      embed.add_field(name="$hello", value="Displays a friendly greeting message.", inline=False)
      embed.add_field(name="$marketlist", value="Displays a list of Pokémon in the marketplace.", inline=False)
      embed.add_field(name="$pokemon <name>", value="Get detailed information about a specific Pokémon.", inline=False)
      embed.add_field(name="$marketplace", value="Explore the Pokémon Marketplace.", inline=False)
      embed.add_field(name="$buy <pokemon>", value="Buy a Pokémon from the marketplace.", inline=False)
      embed.add_field(name="$buy_potion <potion_name>", value="Buy a potion from the marketplace.", inline=False)
      embed.add_field(name="$buy_berry <berry_name>", value="Buy a berry from the marketplace.", inline=False)
      embed.add_field(name="$sell <pokemon>", value="Sell a Pokémon to the marketplace.", inline=False)
      embed.add_field(name="$inventory", value="View your Pokémon inventory.", inline=False)
      embed.add_field(name="$lootbox", value="Open a lootbox.", inline=False)
      embed.add_field(name="$startquiz", value="Start a Pokémon quiz.", inline=False)
      embed.add_field(name="$guess", value="Guess the name of a Pokémon.", inline=False)
      embed.add_field(name="$Sign_in", value="Register your profile.", inline=False)
      embed.add_field(name="$Info", value="Get information about your profile.", inline=False)
      embed.add_field(name="$Trivia", value="Start a trivia game.", inline=False)
      embed.add_field(name="$story_mode", value="Play a Pokémon story-based game.", inline=False)
      embed.add_field(name="$join", value="Join a Pokémon battle game.", inline=False)
      embed.add_field(name="$start_game", value="Start a Pokémon battle game.", inline=False)
      embed.add_field(name="$draw", value="Draw a random Pokémon card.", inline=False)
      embed.add_field(name="$show_deck", value="Show your Pokémon card deck.", inline=False)
      embed.add_field(name="$trade <@mention> <card_name>", value="Trade a Pokémon card with another user.", inline=False)

      # Send the embed
      await message.channel.send(embed=embed)

  if message.content.startswith('$marketlist'):
              pokemon_list = get_pokemon_list()
              if pokemon_list:
                  for pokemon in pokemon_list:
                      pokemon_info = await get_pokemon_info(pokemon)
                      if pokemon_info:
                          stats = await get_pokemon_stats(pokemon_info)
                          types = await get_pokemon_types(pokemon_info)

                          # Extract HP and Speed stats
                          hp_stat = next((stat['base_stat']
                                          for stat in pokemon_info.get('stats', [])
                                          if stat['stat']['name'] == 'hp'), None)
                          speed_stat = next((stat['base_stat']
                                             for stat in pokemon_info.get('stats', [])
                                             if stat['stat']['name'] == 'speed'), None)

                          # Format the info
                          formatted_info = f"HP: {hp_stat} | Speed: {speed_stat} | Types: {', '.join(types)}"

                          # Determine the color based on the Pokémon's type
                          color = discord.Color.red()  # Default color
                          for type in types:
                                if type == 'water':
                                  color = discord.Color.blue()
                                elif type == 'bug':
                                  color = discord.Color(0x8B4513)  # Brown color
                                elif type == 'fire':
                                  color = discord.Color.orange()
                                elif type == 'grass':
                                  color = discord.Color.green()
                                elif type == 'electric':
                                  color = discord.Color.yellow()
                                elif type == 'poison':
                                  color = discord.Color.purple()

                              # Create and send the embed
                          embed = discord.Embed(title=f"{pokemon.capitalize()}",
                                                    description=formatted_info,
                                                    color=color)
                          await message.channel.send(embed=embed)
                      else:
                              await message.channel.send(
                                  f"Pokemon {pokemon.capitalize()} not found.")
                  # Add potion listings
                  embed = discord.Embed(title="Pokémon Marketplace", color=0xFFD700)  # Gold color
                  embed.add_field(name="Potions:",
                                  value="\n".join([f"{potion.capitalize()}: ${price}" for potion, price in POTION_PRICES.items()]),
                                  inline=False)

                  # Add berry listings
                  embed.add_field(name="Berries:",
                                  value="\n".join([f"{berry.capitalize()}: ${price}" for berry, price in BERRY_PRICES.items()]),
                                  inline=False)

                  # Set footer with attribution or any other information
                  embed.set_footer(text="Explore the marketplace and become the ultimate Pokémon trainer!")

                  # Send the embedded message
                  await message.channel.send(embed=embed)
              else:
                  await message.channel.send("Error fetching Pokémon list.")




  if message.content.startswith('$pokemon'):
                        pokemon_name = message.content.split(' ', 1)[1]
                        pokemon_info = await get_pokemon_info(pokemon_name)  # Await here
                        if pokemon_info:
                            embed = discord.Embed(
                                title=f"Pokemon Info for {pokemon_name.capitalize()}",
                                color=discord.Color.green())
                            embed.add_field(name="Name", value=pokemon_info['name'], inline=False)
                            embed.add_field(name="Height", value=pokemon_info['height'], inline=False)
                            embed.add_field(name="Weight", value=pokemon_info['weight'], inline=False)
                            abilities = ', '.join([ability['ability']['name'] for ability in pokemon_info['abilities']])
                            embed.add_field(name="Abilities", value=abilities, inline=False)
                            image_urls = await get_pokemon_image_urls(pokemon_info)  # Await here
                            if image_urls:
                                # Use a bigger image for Charmander
                                if pokemon_name.lower() == 'charmander':
                                    embed.set_thumbnail(
                                        url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/4.png"
                                    )
                                else:
                                    embed.set_thumbnail(url=image_urls['front_default'])
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send(f"Pokemon {pokemon_name.capitalize()} not found.")

  if message.content.startswith('$marketplace'):
      # Create the embedded message
      embed = Embed(title="Welcome to the Pokémon Marketplace!",
                    description="Use the following commands to interact with the marketplace:",
                    color=0xFFD700)  # Gold color

      # Add command descriptions
      embed.add_field(name="Marketplace Commands:",
                      value="- `$market_list`: Displays list of Pokémon in the marketplace.\n"
                            "- `$buy <pokemon>`: Buy a Pokémon from the marketplace.\n"
                            "- `$buy_potion <potion_name>`: Buy a potion from the marketplace.\n"
                            "- `$buy_berry <berry_name>`: Buy a berry from the marketplace.\n"
                            "- `$sell <pokemon>`: Sell a Pokémon to the marketplace.\n"
                            "- `$inventory`: View your Pokémon inventory.\n"
                            "- `$lootbox`: Open a lootbox.",
                      inline=False)

      # Set footer with attribution or any other information
      embed.set_footer(text="Explore the marketplace and become the ultimate Pokémon trainer!")

      # Send the embedded message
      await message.channel.send(embed=embed)

  if message.content.startswith('$buy'):
    item_name = message.content.split(' ', 1)[1].lower()
    await buy_item(message, item_name, POKEMON_PRICES)

  if message.content.startswith('$buy_potion'):
    item_name = message.content.split(' ', 1)[1].lower()
    await buy_item(message, item_name, POTION_PRICES)

  if message.content.startswith('$buy_berry'):
    item_name = message.content.split(' ', 1)[1].lower()
    await buy_item(message, item_name, BERRY_PRICES)

  if message.content.startswith('$sell'):
    item_name = message.content.split(' ', 1)[1].lower()
    await sell_item(message, item_name, POKEMON_PRICES)

  if message.content.startswith('$inventory'):
                            if user_inventory:
                                # Create an embedded inventory
                                embed = discord.Embed(title="Your Inventory", color=discord.Color.blue())

                                # Add items to the inventory
                                inventory_list = "\n".join([f"\u2022 {pokemon.capitalize()}" for pokemon in user_inventory])
                                embed.add_field(name="List", value=inventory_list, inline=False)

                                # Send the embedded inventory
                                await message.channel.send(embed=embed)
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
  if message.content.startswith("$Trivia"):
    await play_trivia_game(message)
  if message.content.startswith('$story_mode'):
    await message.channel.send(
        "Welcome to the game based on The Movie : Pokemon: The Power Of Us")
    await gamest(message, client)

  if message.content.startswith("$join"):
    await join(message)
  if message.content.startswith("$start_game"):
    await start_game(message)

  if message.content.startswith("$start_trade"):
    await message.channel.send("Welcome to the Pokémon Trading Card Game!")

  if message.content.startswith("$draw"):
    await get_random_pokemon_card(message)
    # if card:
    # print("Card", card)
    # await message.channel.send(f"You drew a {card['name']}: {card['image_url']}")

  if message.content.startswith("$show_deck"):
                user_id = str(message.author.id)
                if user_id in decks:
                    for card in decks[user_id]:
                        card_name = card["name"]
                        card_image_url = card["image_url"]
                        embed = discord.Embed(title=card_name, color=discord.Color.blue())
                        embed.set_image(url=card_image_url)
                        await message.channel.send(embed=embed)
                else:
                    await message.channel.send("Your deck is empty.")




  if message.content.startswith("$trade"):

    user_mention, name = message.content.split(" ", 2)[1:]
    ctx = await client.get_context(message)
    member_converter = commands.MemberConverter()
    mentioned_user = await member_converter.convert(ctx, user_mention)

    # Get the ID of the trading user and the mentioned user
    user_id = str(message.author.id)
    mentioned_user_id = str(mentioned_user.id)

    # Check if the trading user has the card in their deck
    if user_id in decks:

      # Convert the searched card name to lowercase
      name_lower = name.lower()

      for card in decks[user_id]:

        # Convert the card name in the deck to lowercase
        card_name_lower = card["name"].lower()

        if card_name_lower == name_lower:

          # Confirm trade with mentioned user
          await message.channel.send(
              f"{mentioned_user.display_name}, {message.author.display_name} wants to trade a card with you. Type '!yes' to confirm or '!no' to decline."
          )

          def check(m):

            return m.author == mentioned_user and m.content.lower() in (
                "!yes",
                "!no",
            )

          try:

            msg = await client.wait_for("message", check=check, timeout=30)
            if msg.content.lower() == "!yes":
              # Remove the card from the trading user's deck
              decks[user_id].remove(card)

              # Add the card to the mentioned user's deck
              if mentioned_user_id not in decks:
                decks[mentioned_user_id] = []
              decks[mentioned_user_id].append(card)

              # Save the updated decks
              save_decks(decks)

              await message.channel.send(
                  f"{message.author.display_name} traded a card to {mentioned_user.display_name}."
              )
            else:
              await message.channel.send(
                  f"{mentioned_user.display_name} declined the trade.")
          except asyncio.TimeoutError:
            await message.channel.send(
                f"{mentioned_user.display_name} did not respond in time. Trade request cancelled."
            )
          return
    await message.channel.send("No card found in your deck with that name.")


@client.event
async def on_button_click(interaction):
  await interaction.response.defer(
  )  # Acknowledge the button click immediately
  if isinstance(interaction, discord.Interaction):
    card_id = int(interaction.data["custom_id"])
    card = requests.get(f"{TCGDEX_API_URL}/cards/{card_id}").json()["data"]
    await interaction.followup.send(f"Selected card: {card['name']}")


# Command to create a button row for a card
@client.command()
async def show_card(ctx, card_id):
  card = requests.get(f"{TCGDEX_API_URL}/cards/{card_id}").json()["data"]
  if card:
    row = create_card_button(card)
    await ctx.send("Select a card:", view=View(row))


try:
  token = os.getenv("DISCORD_TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
  if e.status == 429:
    print(
        "The Discord servers denied the connection for making too many requests"
    )
    print(
        "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
    )
