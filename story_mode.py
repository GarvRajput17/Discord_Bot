import asyncio
import discord
import os
from discord import Embed
from discord import File


class PokemonPowerOfUs:

  def __init__(self, message, bot):
    self.character = None
    self.message = message
    self.bot = bot

  async def send_image(self, image_path):
    try:
      with open(image_path, 'rb') as f:
        picture = File(f)
        await self.message.channel.send(file=picture)
    except FileNotFoundError:
      print("File not found!")

  async def power_of_us_intro(self):
    # Welcome message
    welcome_embed = Embed(
        title="Welcome to Pokémon: The Power of Us game!",
        description=
        "You find yourself in the bustling seaside town of Fula City during the annual Wind Festival.",
        color=discord.Color.blue())
    await self.send_image("intro.jpeg")
    # Send the welcome message
    await self.message.channel.send(embed=welcome_embed)
    await asyncio.sleep(1)

    # About the city message
    city_info_embed = Embed(
        title="About Fula City",
        description=
        ("This festival celebrates the legendary Pokémon Lugia, said to bring the wind that powers the city.\n"
         "As you explore the city, you encounter various characters and hear whispers of excitement in the air."
         ),
        color=discord.Color.green())

    # Send the city info message
    await self.message.channel.send(embed=city_info_embed)
    await asyncio.sleep(2)

    # Last part of the intro
    final_part_embed = Embed(title="Are you ready to embark on an adventure?",
                             description="Let's get started!",
                             color=discord.Color.gold())

    # Send the final part message
    await self.message.channel.send(embed=final_part_embed)

    # Prompt the user to choose a character
    await self.choose_character()

  async def input_with_timeout(self, prompt, timeout):
    try:
      return await asyncio.wait_for(self.loop.run_in_executor(
          None, input, prompt),
                                    timeout=timeout)
    except asyncio.TimeoutError:
      await self.message.channel.send("\nTime's up! Game terminated.")
      exit()

  async def choose_character(self):
    await self.message.channel.send("Choose your character:")
    await self.message.channel.send("1. Ash Ketchum")

    def check(m):
      return m.author == self.message.author and m.channel == self.message.channel and m.content.isdigit(
      )

    try:
      response = await self.bot.wait_for('message', check=check, timeout=30.0)
      choice = int(response.content)
      self.user_input = choice
      if choice == 1:
        self.character = "Ash Ketchum"
        await self.ash_intro()
      # Add additional conditions for other characters here
      else:
        await self.message.channel.send(
            "Invalid choice. Please enter the number")
        await self.choose_character()
    except asyncio.TimeoutError:
      await self.message.channel.send("\nTime's up! Please try again.")

  async def ash_intro(self):
    # URL of the image

    # Send the message with the imag

    first_part_text = (
        "**You've chosen to play as Ash Ketchum.**\n\n"
        "As Ash, you're excited to explore Fula City and participate in the Wind Festival.\n\n"
        "You decide to head towards the center of the city where the festivities are in full swing.\n\n"
        "Along the way, you encounter various Pokémon trainers and enthusiasts, all buzzing with excitement."
    )

    # Second part of the text with formatting
    second_part_text = (
        "Suddenly, you hear a commotion nearby. You rush to the scene and find a Pokémon in distress.\n\n"
        "**What will you do?**\n\n"
        "1. Approach the Pokémon cautiously.\n"
        "2. Call out to the Pokémon and try to calm it down.")

    # Create the first embedded message
    first_embed = Embed(
        description=first_part_text,
        color=0xFFA500  # Orange color
    )

    # Create the second embedded message
    second_embed = Embed(
        description=second_part_text,
        color=0x00FF00  # Green color
    )
    await self.send_image("ash.jpeg")
    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)

    # Send the second embedded message
    await self.message.channel.send(embed=second_embed)

    def check(m):

      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.approach_pokemon()
      elif choice == '2':
        await self.call_out_to_pokemon()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def approach_pokemon(self):
    first_part_text = (
        "**You cautiously approach the distressed Pokémon.**\n\n"
        "It seems scared and defensive, but you try to convey your friendly intentions.\n\n"
        "Slowly, the Pokémon begins to calm down and allows you to get closer."
    )

    # Second part of the text with formatting
    second_part_text = (
        "As you reach out to help the Pokémon, you notice something glimmering nearby.\n\n"
        "**What will you do?**\n\n"
        "1. Investigate the glimmering object.\n"
        "2. Focus on comforting the Pokémon.")

    # Create the first embedded message
    first_embed = Embed(
        description=first_part_text,
        color=0xFFA500  # Orange color
    )

    # Create the second embedded message
    second_embed = Embed(
        description=second_part_text,
        color=0x00FF00  # Green color
    )

    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)

    # Send the second embedded message
    await self.message.channel.send(embed=second_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.investigate_glimmering_object()
      elif choice == '2':
        await self.focus_on_comforting_pokemon()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def call_out_to_pokemon(self):
    first_part_text = (
        "**You call out to the distressed Pokémon in a soothing voice.**\n\n"
        "Your gentle approach seems to have an effect as the Pokémon starts to calm down.\n\n"
        "Suddenly, you notice something glimmering nearby.")

    # Second part of the text with the question
    second_part_text = ("**What will you do?**\n\n"
                        "1. Investigate the glimmering object.\n"
                        "2. Keep focusing on calming the Pokémon.")

    # Create the first embedded message
    first_embed = Embed(
        description=first_part_text,
        color=0xFFA500  # Orange color
    )

    # Create the second embedded message
    second_embed = Embed(
        description=second_part_text,
        color=0x00FF00  # Green color
    )

    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)

    # Send the second embedded message
    await self.message.channel.send(embed=second_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.investigate_glimmering_object()
      elif choice == '2':
        await self.keep_focusing_on_calming_pokemon()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def investigate_glimmering_object(self):
    first_part_text = (
        "**You approach the glimmering object and discover a valuable item.**\n\n"
        "It could be useful on your journey.\n\n"
        "As you pick up the item, you hear a voice calling out for help from further ahead."
    )

    # Second part of the text with the question
    second_part_text = ("**Will you investigate?**\n\n"
                        "1. Proceed cautiously towards the voice.\n"
                        "2. Stay where you are and observe the surroundings.")

    # Create the first embedded message
    first_embed = Embed(
        description=first_part_text,
        color=0xFFA500  # Orange color
    )

    # Create the second embedded message
    second_embed = Embed(
        description=second_part_text,
        color=0x00FF00  # Green color
    )

    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)

    # Send the second embedded message
    await self.message.channel.send(embed=second_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.proceed_towards_voice()
      elif choice == '2':
        await self.stay_and_observe()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def focus_on_comforting_pokemon(self):

    # First part of the text with formatting
    first_part_text = (
        "**You focus on comforting the distressed Pokémon.**\n\n"
        "Your gentle approach seems to work as the Pokémon starts to relax.\n\n"
        "Suddenly, you notice something glimmering nearby.")

    # Second part of the text with the question
    second_part_text = ("**What will you do?**\n\n"
                        "1. Investigate the glimmering object.\n"
                        "2. Keep comforting the Pokémon.")

    # Create the first embedded message
    first_embed = Embed(
        description=first_part_text,
        color=0xFFA500  # Orange color
    )

    # Create the second embedded message
    second_embed = Embed(
        description=second_part_text,
        color=0x00FF00  # Green color
    )

    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)

    # Send the second embedded message
    await self.message.channel.send(embed=second_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.investigate_glimmering_object()
      elif choice == '2':
        await self.keep_focusing_on_calming_pokemon()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def keep_focusing_on_calming_pokemon(self):

    # First part of the text with formatting
    first_part_text = (
        "**You continue to focus on calming the distressed Pokémon.**\n\n"
        "Your soothing voice and gestures seem to be working.\n\n"
        "Suddenly, you notice something glimmering nearby.")

    # Second part of the text with the question
    second_part_text = ("**What will you do?**\n\n"
                        "1. Investigate the glimmering object.\n"
                        "2. Keep your attention on the Pokémon.")

    # Create the first embedded message
    first_embed = Embed(
        description=first_part_text,
        color=0xFFA500  # Orange color
    )

    # Create the second embedded message
    second_embed = Embed(
        description=second_part_text,
        color=0x00FF00  # Green color
    )

    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)

    # Send the second embedded message
    await self.message.channel.send(embed=second_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.investigate_glimmering_object()
      elif choice == '2':
        await self.stay_and_observe()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def proceed_towards_voice(self):

    # Define the text for the first message
    first_message_text = (
        "**You cautiously proceed towards the direction of the voice.**\n\n"
        "As you get closer, you see a group of Pokémon cornered by a group of wild Pokémon.\n\n"
        "Without hesitation, you jump into action to help the trapped Pokémon."
    )

    # Define the text for the second message
    second_message_text = (
        "**What will you do?**\n\n"
        "1. Engage in battle to defeat the wild Pokémon.\n"
        "2. Try to distract the wild Pokémon to give the trapped Pokémon a chance to escape."
    )

    # Create the first embedded message with a blue color
    first_embed = Embed(description=first_message_text, color=0x0000FF)

    # Create the second embedded message with a green color
    second_embed = Embed(description=second_message_text, color=0x00FF00)

    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)

    # Send the second embedded message
    await self.message.channel.send(embed=second_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.engage_in_battle()
      elif choice == '2':
        await self.distract_wild_pokemon()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def stay_and_observe(self):

    # Define the text for the first message
    first_message_text = (
        "**You decide to stay where you are and observe the surroundings.**\n\n"
        "From your vantage point, you notice a group of Pokémon cornered by a group of wild Pokémon.\n\n"
        "You realize they're in trouble and need your help.")

    # Define the text for the second message
    second_message_text = (
        "**What will you do?**\n\n"
        "1. Rush in to engage in battle and help the trapped Pokémon.\n"
        "2. Try to come up with a plan to distract the wild Pokémon and aid the trapped Pokémon."
    )

    # Create the first embedded message with a blue color
    first_embed = Embed(description=first_message_text, color=0x0000FF)

    # Create the second embedded message with a green color
    second_embed = Embed(description=second_message_text, color=0x00FF00)

    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)

    # Send the second embedded message
    await self.message.channel.send(embed=second_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.engage_in_battle()
      elif choice == '2':
        await self.distract_wild_pokemon()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def engage_in_battle(self):
    from discord import Embed

    # Define the text for the first message
    first_message_text = (
        "**You decide to engage in battle to defeat the wild Pokémon and help the trapped Pokémon.**\n\n"
        "Your Pokémon leap into action, ready to fight alongside you.\n\n"
        "The battle is intense, but with your skill and determination, you manage to defeat the wild Pokémon."
    )

    # Create the embedded message for the first part with a purple color
    first_embed = Embed(description=first_message_text, color=0x800080)

    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)
    await self.send_image("wild_pok.jpeg")
    # Define the text for the second message
    second_message_text = (
        "The trapped Pokémon are grateful for your help and express their thanks.\n\n"
        "You feel a sense of accomplishment as you continue your journey through Fula City."
    )

    # Create the embedded message for the second part with a different color
    second_embed = Embed(description=second_message_text, color=0xFFD700)

    # Send the second embedded message
    await self.message.channel.send(embed=second_embed)
    # await self.send_image("zeroara.jpeg")
    # await asyncio.sleep(2)
    await self.original_story_continuation()

  async def distract_wild_pokemon(self):
    from discord import Embed

    # Define the text for the first message
    first_message_text = (
        "**You come up with a plan to distract the wild Pokémon and aid the trapped Pokémon.**\n\n"
        "You gather some nearby items and make noise to get the attention of the wild Pokémon."
    )

    # Create the embedded message for the first part with a blue color
    first_embed = Embed(description=first_message_text, color=0x0000FF)

    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)

    # Define the text for the second message
    second_message_text = (
        "Your plan works, and the wild Pokémon are momentarily distracted, allowing the trapped Pokémon to escape.\n\n"
        "The trapped Pokémon express their gratitude and flee to safety.\n\n"
        "You feel satisfied with your quick thinking and resourcefulness as you continue exploring Fula City."
    )

    # Create the embedded message for the second part with a green color
    second_embed = Embed(description=second_message_text, color=0x00FF00)

    # Send the second embedded message
    await self.message.channel.send(embed=second_embed)

    await asyncio.sleep(2)
    await self.original_story_continuation()

  async def original_story_continuation(self):
    await self.message.channel.send(
        "\nAs you continue your journey through Fula City, you come across a group of trainers gathered around."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "They seem to be discussing something exciting, and you decide to join them."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "It turns out they're planning a Pokémon battle tournament as part of the Wind Festival celebrations."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "This is your chance to show off your skills as a Pokémon Trainer!")
    await asyncio.sleep(2)
    await self.message.channel.send("Will you participate in the tournament?")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "1. Yes, I'm ready for some exciting battles!")
    await self.message.channel.send(
        "2. Maybe later, I want to explore more of Fula City first.")

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.participate_in_tournament()
      elif choice == '2':
        await self.explore_more_of_fula_city()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  # async def participate_in_tournament(self):
  #   await self.message.channel.send(
  #       "\nYou decide to participate in the Pokémon battle tournament.")
  #   await asyncio.sleep(1)
  #   await self.message.channel.send(
  #       "Your Pokémon are ready, and you're eager to showcase your skills.")
  #   await asyncio.sleep(2)
  #   await self.message.channel.send(
  #       "The battles are intense, but you manage to win several rounds and make it to the final match."
  #   )
  #   await asyncio.sleep(2)
  #   await self.message.channel.send(
  #       "In the final match, you face off against a formidable opponent.")
  #   await asyncio.sleep(2)
  #   await self.message.channel.send(
  #       "It's a tough battle, but with determination and teamwork, you emerge victorious!"
  #   )
  #   await asyncio.sleep(2)
  #   await self.message.channel.send(
  #       "The crowd cheers for your impressive performance, and you feel proud of your accomplishments."
  #   )
  #   await asyncio.sleep(2)
  #   await self.message.channel.send(
  #       "With the tournament over, you continue your exploration of Fula City, eager for more adventures."
  #   )
  #   await asyncio.sleep(2)
  #   await explore_more_of_fula_city()

  async def explore_more_of_fula_city(self):
    first_message_text = (
        "**As you continue your journey through Fula City, you come across a group of trainers gathered around.**\n\n"
        "They seem to be discussing something exciting, and you decide to join them.\n\n"
        "It turns out they're planning a Pokémon battle tournament as part of the Wind Festival celebrations.\n\n"
        "This is your chance to show off your skills as a Pokémon Trainer!")

    # Create the embedded message for the first part with a blue color
    first_embed = Embed(description=first_message_text, color=0x0000FF)

    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)

    # Define the text for the second message
    second_message_text = (
        "**Will you participate in the tournament?**\n\n"
        "1. Yes, I'm ready for some exciting battles!\n"
        "2. Maybe later, I want to explore more of Fula City first.")

    # Create the embedded message for the second part with a green color
    second_embed = Embed(description=second_message_text, color=0x00FF00)

    # Send the second embedded message
    await self.send_image("abondened_building_actual.jpeg")
    await self.message.channel.send(embed=second_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.investigate_abandoned_building()
      elif choice == '2':
        await self.continue_exploring_city()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def investigate_abandoned_building(self):
    # Define the text for the first message
    first_message_text = (
        "**You decide to investigate the abandoned building.**\n\n"
        "As you enter, you're greeted by darkness and silence.\n\n"
        "You cautiously explore the interior, discovering old equipment and remnants of past experiments.\n\n"
        "Suddenly, you hear a strange noise coming from deeper within the building."
    )

    # Create the embedded message for the first part with a blue color
    first_embed = Embed(description=first_message_text, color=0x0000FF)

    # Send the first embedded message
    await self.message.channel.send(embed=first_embed)

    # Define the text for the second message
    second_message_text = (
        "**What will you do?**\n\n"
        "1. Investigate the source of the noise.\n"
        "2. Leave the building and come back later with backup.")

    # Create the embedded message for the second part with a green color
    second_embed = Embed(description=second_message_text, color=0x00FF00)

    # Send the second embedded message
    await self.message.channel.send(embed=second_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.investigate_source_of_noise()
      elif choice == '2':
        await self.leave_building_and_come_back()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def continue_exploring_city(self):
    from discord import Embed

    # Define the text for the first part of the message
    first_part_text = (
        "**You decide to continue exploring the city.**\n\n"
        "There's still so much to see and do!\n\n"
        "As you wander through the streets, you come across a bustling marketplace.\n\n"
        "Merchants are selling all kinds of goods, including rare Pokémon items."
    )

    # Create the embedded message for the first part with a blue color
    first_part_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Define the text for the second part of the message
    second_part_text = ("**Will you browse the marketplace?**\n\n"
                        "1. Yes, I'm curious to see what they have.\n"
                        "2. Maybe later, I'll keep exploring for now.")

    # Create the embedded message for the second part with a green color
    second_part_embed = Embed(description=second_part_text, color=0x00FF00)

    # Send the second part of the message
    await self.send_image("marketplace.jpeg")
    await self.message.channel.send(embed=second_part_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.browse_marketplace()
      elif choice == '2':
        await self.decide_not_to_purchase_artifact()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def browse_marketplace(self):
    from discord import Embed

    # Define the text for the first part of the message
    first_part_text = (
        "**You decide to browse the marketplace.**\n\n"
        "There are so many interesting items for sale, including rare Pokémon items.\n\n"
        "As you examine the goods, you come across a vendor selling ancient artifacts."
    )

    # Create the embedded message for the first part with a blue color
    first_part_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Define the text for the second part of the message
    second_part_text = ("**Will you purchase the artifact?**\n\n"
                        "1. Yes, it could be valuable or hold some secrets.\n"
                        "2. No, it seems too risky.")

    # Create the embedded message for the second part with a green color
    second_part_embed = Embed(description=second_part_text, color=0x00FF00)

    # Send the second part of the message
    await self.message.channel.send(embed=second_part_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.purchase_artifact()
      elif choice == '2':
        await self.decide_not_to_purchase_artifact()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def purchase_artifact(self):
    from discord import Embed

    # Define the text for the first part of the message
    first_part_text = (
        "**You decide to purchase the mysterious artifact.**\n\n"
        "The vendor accepts your offer, and you acquire the artifact.\n\n"
        "As you hold it in your hands, you feel a strange energy emanating from it."
    )

    # Create the embedded message for the first part with a blue color
    first_part_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Define the text for the second part of the message
    second_part_text = (
        "**You're not sure what its purpose is, but you're excited to find out!**\n\n"
        "With the artifact in your possession, you continue your exploration of Fula City."
    )

    # Create the embedded message for the second part with a green color
    second_part_embed = Embed(description=second_part_text, color=0x00FF00)

    # Send the second part of the message
    await self.message.channel.send(embed=second_part_embed)

    await asyncio.sleep(2)
    # Continue with the rest of the storyline

  async def decide_not_to_purchase_artifact(self):
    first_part_text = (
        "**You decide not to purchase the mysterious artifact.**\n\n"
        "It seems too risky to acquire something with unknown powers."
        "You thank the vendor but politely decline the offer.")

    # Create the embedded message for the first part with a red color
    first_part_embed = Embed(description=first_part_text, color=0xFF0000)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Define the text for the second part of the message
    second_part_text = (
        "**With caution in mind, you continue your exploration of Fula City, wary of any potential dangers.**"
    )

    # Create the embedded message for the second part with a yellow color
    second_part_embed = Embed(description=second_part_text, color=0xFFFF00)

    # Send the second part of the message
    await self.message.channel.send(embed=second_part_embed)
    # Continue with the rest of the storyline
    await self.original_story_continuation()

  async def investigate_source_of_noise(self):
    first_part_text = (
        "**You decide to investigate the source of the noise.**\n\n"
        "As you venture deeper into the building, the noise grows louder.\n\n"
        "You finally reach the source—a hidden laboratory with strange equipment.\n\n"
        "Inside, you find a group of researchers conducting experiments on Pokémon.\n\n"
        "They seem surprised by your presence but welcome you nonetheless.")

    # Create the embedded message for the first part with a blue color
    first_part_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)
    options_text = (
        "**What will you do?**\n"
        "1. Offer to help with their research.\n"
        "2. Express concern about the experiments and suggest safer alternatives."
    )

    # Create the embedded message for the options with a green color
    options_embed = Embed(description=options_text, color=0x00FF00)

    # Send the embedded message for the options
    await self.message.channel.send(embed=options_embed)

    def check(m):
      # Check if the message author is the same as the user who triggered the command
      # Check if the message is sent in the same channel as the prompt message
      # Check if the message content is either '1' or '2'
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for a message from the user that satisfies the check function
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.offer_to_help_with_research()
      elif choice == '2':
        await self.express_concern_and_suggest_alternatives()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def leave_building_and_come_back(self):
    # Define the text for the first part of the message
    first_part_text = (
        "Leaves the abandoned building and plans to return later with backup."
        "\n\nYou decide to leave the building and come back later with backup."
        "\n\nIt's better to approach the situation with caution and not take any unnecessary risks."
    )

    # Create the embedded message for the first part with a blue color
    first_part_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Wait for a moment
    await asyncio.sleep(2)

    # Define the text for the second part of the message
    second_part_text = (
        "You make a mental note to return to the abandoned building when you're better prepared."
        "\n\nFor now, you'll continue your exploration of Fula City, keeping an eye out for any other mysteries."
    )

    # Create the embedded message for the second part with a blue color
    second_part_embed = Embed(description=second_part_text, color=0x0000FF)

    # Send the second part of the message
    await self.message.channel.send(embed=second_part_embed)
    await asyncio.sleep(2)
    await self.original_story_continuation()

  # async def original_story_continuation(self):
  #   """
  #       Continues the original storyline after leaving the abandoned building.
  #       """
  #   first_part_text = (
  #     "As you continue your journey through Fula City, you come across a group of trainers gathered around."
  #     "\n\nThey seem to be discussing something exciting, and you decide to join them."
  #     "\n\nIt turns out they're planning a Pokémon battle tournament as part of the Wind Festival celebrations."
  #   )

  #   # Create the embedded message for the first part with a blue color
  #   first_part_embed = Embed(description=first_part_text, color=0x0000FF)

  #   # Send the first part of the message
  #   await self.message.channel.send(embed=first_part_embed)

  #   # Wait for a moment
  #   await asyncio.sleep(2)

  #   # Define the text for the second part of the message
  #   second_part_text = (
  #     "This is your chance to show off your skills as a Pokémon Trainer!"
  #     "\n\nWill you participate in the tournament?"
  #     "\n\n1. Yes, I'm ready for some exciting battles!"
  #     "\n2. Maybe later, I want to explore more of Fula City first."
  #   )

  #   # Create the embedded message for the second part with a blue color
  #   second_part_embed = Embed(description=second_part_text, color=0x0000FF)

  #   # Send the second part of the message
  #   await self.message.channel.send(embed=second_part_embed)

  #       # Define a check function to validate the user's respons

  #   def check(m):
  #         # Check if the message author is the same as the user who triggered the command
  #         # Check if the message is sent in the same channel as the prompt message
  #         # Check if the message content is either '1' or '2'
  #         return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

  #   try:
  #         # Wait for a message from the user that satisfies the check function
  #         response = await self.bot.wait_for('message', check=check, timeout=20.0)
  #         choice = response.content

  #         # Process the user's choice
  #         if choice == '1':
  #             await self.participate_in_tournament()
  #         elif choice == '2':
  #             await self.explore_more_of_fula_city()

  #   except asyncio.TimeoutError:
  #         # Handle timeout if no response is received within the specified timeout duration
  #         await self.message.channel.send("Time's up! Please try again.")

  async def participate_in_tournament(self):
    """
        Participates in the Pokémon battle tournament.
        """
    first_part_text = (
        "**You decide to participate in the Pokémon battle tournament.**\n\n"
        "Your Pokémon are ready, and you're eager to showcase your skills.\n\n"
        "The battles are intense, but you manage to win several rounds and make it to the final match."
    )

    # Create the embedded message for the first part with a blue color
    first_part_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Await for the final battle
    await asyncio.sleep(2)
    await self.send_image("tournament.jpeg")
    # Define the text for the second part of the message
    second_part_text = (
        "**In the final match, you face off against a formidable opponent.**\n\n"
        "It's a tough battle, but with determination and teamwork, you emerge victorious!\n\n"
        "The crowd cheers for your impressive performance, and you feel proud of your accomplishments.\n\n"
        "With the tournament over, you continue your exploration of Fula City, eager for more adventures."
    )

    # Create the embedded message for the second part with a green color
    second_part_embed = Embed(description=second_part_text, color=0x00FF00)

    # Send the second part of the message
    await self.message.channel.send(embed=second_part_embed)

    # Continue exploration
    await asyncio.sleep(2)
    await self.explore_more_of_fula_city()

  # async def explore_more_of_fula_city(self):
  #   """
  #       Explores more of Fula City.
  #       """
  #   first_part_text = (
  #     "**You decide to explore more of Fula City before participating in the tournament.**\n\n"
  #     "There are so many interesting places to see and people to meet!\n\n"
  #     "As you wander around, you stumble upon a mysterious-looking building.\n\n"
  #     "It seems abandoned, but there's something intriguing about it."
  #   )

  #   # Create the embedded message for the first part with a blue color
  #   first_part_embed = Embed(description=first_part_text, color=0x0000FF)

  #   # Send the first part of the message
  #   await self.message.channel.send(embed=first_part_embed)

  #   # Await for the user's response
  #   await asyncio.sleep(2)

  #   # Define the text for the second part of the message
  #   second_part_text = (
  #     "**Will you investigate the building?**\n\n"
  #     "1. Yes, I'm curious to see what's inside.\n"
  #     "2. Maybe later, I'll continue exploring the city for now."
  #   )

  #   # Create the embedded message for the second part with a green color
  #   second_part_embed = Embed(description=second_part_text, color=0x00FF00)
  #   self.send_image("abondened_building.jpeg")
  #   # Send the second part of the message
  #   await self.message.channel.send(embed=second_part_embed)

  #       # Define a check function to validate the user's response
  #   def check(m):
  #           return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

  #   try:
  #           # Wait for the user's response with a timeout of 20 seconds
  #           response = await self.bot.wait_for('message', check=check, timeout=20.0)
  #           choice = response.content

  #           # Process the user's choice
  #           if response == '1':
  #               await self.investigate_abandoned_building()
  #           elif response == '2':
  #               await self.continue_exploring_city()

  #   except asyncio.TimeoutError:
  #           # Handle timeout if no response is received within the specified timeout duration
  #           await self.message.channel.send("Time's up! Please try again.")

  async def investigate_abandoned_building(self):
    """
        Investigates the abandoned building.
        """
    first_part_text = (
        "**You decide to investigate the abandoned building.**\n\n"
        "As you enter, you're greeted by darkness and silence.\n\n"
        "You cautiously explore the interior, discovering old equipment and remnants of past experiments.\n\n"
        "Suddenly, you hear a strange noise coming from deeper within the building."
    )

    # Create the embedded message for the first part with a blue color
    first_part_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Await for a moment before sending the second part of the message
    await asyncio.sleep(2)

    # Define the text for the second part of the message
    second_part_text = (
        "**What will you do?**\n\n"
        "1. Investigate the source of the noise.\n"
        "2. Leave the building and come back later with backup.\n"
        "3. Ignore the noise and continue exploring.")

    # Create the embedded message for the second part with a green color
    second_part_embed = Embed(description=second_part_text, color=0x00FF00)

    # Send the second part of the message
    await self.message.channel.send(embed=second_part_embed)

    # Define a check function to validate the user's response
    def check(m):
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2', '3'
      ]

    try:
      # Wait for the user's response with a timeout of 20 seconds
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.investigate_source_of_noise()
      elif choice == '2':
        await self.leave_building_and_come_back_with_backup()
      elif choice == '3':
        await self.ignore_noise_and_continue_exploring()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def investigate_source_of_noise(self):
    """
        Investigates the source of the noise in the abandoned building.
        """
    first_part_text = (
        "**You decide to investigate the source of the noise.**\n\n"
        "As you venture deeper into the building, the noise grows louder.\n\n"
        "You finally reach the source—a hidden laboratory with strange equipment.\n\n"
        "Inside, you find a group of researchers conducting experiments on Pokémon.\n\n"
        "They seem surprised by your presence but welcome you nonetheless.")

    # Create the embedded message for the first part with a blue color
    first_part_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Await for a moment before sending the second part of the message
    await asyncio.sleep(2)
    await self.send_image("laboraorty.jpeg")

    # Define the text for the second part of the message
    second_part_text = (
        "**What will you do?**\n\n"
        "1. Offer to help with their research.\n"
        "2. Express concern about the experiments and suggest safer alternatives.\n"
        "3. Leave the laboratory and inform the authorities.")

    # Create the embedded message for the second part with a green color
    second_part_embed = Embed(description=second_part_text, color=0x00FF00)

    # Send the second part of the message
    await self.message.channel.send(embed=second_part_embed)

    # Define a check function to validate the user's response
    def check(m):
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2', '3'
      ]

    try:
      # Wait for the user's response with a timeout of 20 seconds
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.offer_to_help_with_research()
      elif choice == '2':
        await self.express_concern_and_suggest_alternatives()
      elif choice == '3':
        await self.leave_lab_and_inform_authorities()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def offer_to_help_with_research(self):
    """
        Offers to help with the research in the laboratory.
        """
    first_part_text = (
        "**You offer to help with their research, intrigued by the experiments.**\n\n"
        "The researchers gladly accept your offer and invite you to assist them.\n\n"
        "Together, you work on various experiments, learning new things about Pokémon."
    )

    # Create the embedded message for the first part with a blue color
    first_part_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Await for a moment before sending the second part of the message
    await asyncio.sleep(2)

    # Define the text for the second part of the message
    second_part_text = (
        "**Your contributions are valuable, and the researchers appreciate your assistance.**\n\n"
        "You feel proud to be a part of such important work.")

    # Create the embedded message for the second part with a green color
    second_part_embed = Embed(description=second_part_text, color=0x00FF00)

    # Send the second part of the message
    await self.message.channel.send(embed=second_part_embed)
    await self.final_encounter()

  async def express_concern_and_suggest_alternatives(self):
    """
        Expresses concern about the experiments and suggests safer alternatives.
        """
    # Define the text for the message
    message_text = (
        "**You express concern about the experiments and suggest safer alternatives.**\n\n"
        "The researchers listen to your suggestions and agree to consider them.\n\n"
        "They appreciate your input and assure you that they'll prioritize the safety and well-being of Pokémon.\n\n"
        "You feel relieved that your concerns were heard and respected.")

    # Create the embedded message with a purple color
    embed = Embed(description=message_text, color=0x800080)

    # Send the embedded message
    await self.message.channel.send(embed=embed)

    await self.participate_in_tournament()

  async def leave_lab_and_inform_authorities(self):
    """
        Leaves the laboratory and decides to inform the authorities about the experiments.
        """
    message_text = (
        "**You decide to leave the laboratory and inform the authorities about the experiments.**\n\n"
        "It's important to ensure the safety and well-being of Pokémon.\n\n"
        "You make your way to the authorities and report what you witnessed.\n\n"
        "They assure you that they'll investigate the matter further.\n\n"
        "With your duty fulfilled, you continue your exploration of Fula City."
    )

    # Create the embedded message with a green color
    embed = Embed(description=message_text, color=0x008000)

    # Send the embedded message
    await self.message.channel.send(embed=embed)
    await asyncio.sleep(2)
    await self.original_story_continuation()

  async def leave_building_and_come_back_with_backup(self):
    """
        Leaves the abandoned building and plans to return later with backup.
        """
    first_part_text = (
        "**You decide to leave the building and come back later with backup.**\n\n"
        "It's better to approach the situation with caution and not take any unnecessary risks."
    )
    first_part_embed = Embed(description=first_part_text, color=0xFF0000)

    await self.message.channel.send(embed=first_part_embed)
    await asyncio.sleep(2)

    # Second part of the message
    second_part_text = (
        "You make a mental note to return to the abandoned building when you're better prepared.\n\n"
        "For now, you'll continue your exploration of Fula City, keeping an eye out for any other mysteries."
    )
    second_part_embed = Embed(description=second_part_text, color=0x00FF00)

    await self.message.channel.send(embed=second_part_embed)
    await asyncio.sleep(2)
    await self.original_story_continuation()

  async def ignore_noise_and_continue_exploring(self):
    """
        Ignores the strange noise in the abandoned building and continues exploring.
        """
    message_text = (
        "**You decide to ignore the noise and continue exploring.**\n\n"
        "Perhaps it's best not to get involved in something that might be dangerous.\n\n"
        "You focus on other parts of Fula City, searching for more clues and adventures."
    )

    # Create an embedded message with the defined text and a color
    embedded_message = Embed(description=message_text, color=0xFFA500)

    # Send the embedded message
    await self.message.channel.send(embed=embedded_message)
    await asyncio.sleep(2)
    await self.original_story_continuation()

  async def original_story_continuation(self):
    """
        Continues the original storyline after leaving the abandoned building or laboratory.
        """
    first_part_text = (
        "**As you continue your journey through Fula City, you come across a group of trainers gathered around.**\n\n"
        "They seem to be discussing something exciting, and you decide to join them.\n\n"
        "It turns out they're planning a Pokémon battle tournament as part of the Wind Festival celebrations."
    )

    # Create the embedded message for the first part with a blue color
    first_part_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Define the text for the second part of the message
    second_part_text = (
        "**This is your chance to show off your skills as a Pokémon Trainer!**\n\n"
        "1. Yes, I'm ready for some exciting battles!\n"
        "2. Maybe later, I want to explore more of Fula City first.")

    # Create the embedded message for the second part with a green color
    second_part_embed = Embed(description=second_part_text, color=0x00FF00)

    # Send the second part of the message
    await self.message.channel.send(embed=second_part_embed)

    # Define a check function to validate the user's response
    def check(m):
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for the user's response with a timeout of 20 seconds
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.participate_in_tournament()
      elif choice == '2':
        await self.explore_more_of_fula_city()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def participate_in_tournament(self):
    before_final_match_text = (
        "**Participates in the Pokémon battle tournament.**\n\n"
        "You decide to participate in the Pokémon battle tournament.\n\n"
        "Your Pokémon are ready, and you're eager to showcase your skills.\n\n"
        "The battles are intense, but you manage to win several rounds and make it to the final match."
    )

    # Create the embedded message for before the final match with a purple color
    before_final_match_embed = Embed(description=before_final_match_text,
                                     color=0x800080)

    # Send the embedded message for before the final match
    await self.message.channel.send(embed=before_final_match_embed)

    # Wait for a moment before sending the message about the final match
    await asyncio.sleep(2)
    await self.send_image("tournament.jpeg")

    # Define the text for after the final match
    after_final_match_text = (
        "In the final match, you face off against a formidable opponent.\n\n"
        "It's a tough battle, but with determination and teamwork, you emerge victorious!\n\n"
        "The crowd cheers for your impressive performance, and you feel proud of your accomplishments.\n\n"
        "With the tournament over, you continue your exploration of Fula City, eager for more adventures."
    )

    # Create the embedded message for after the final match with a purple color
    after_final_match_embed = Embed(description=after_final_match_text,
                                    color=0x800080)

    # Send the embedded message for after the final match
    await self.message.channel.send(embed=after_final_match_embed)

    await asyncio.sleep(2)
    await self.final_encounter()

  async def explore_more_of_fula_city(self):
    """
        Explores more of Fula City before participating in the tournament.
        """
    first_part_text = (
        "**Explores more of Fula City before the tournament.**\n\n"
        "You decide to explore more of Fula City before participating in the tournament.\n\n"
        "There are so many interesting places to see and people to meet!\n\n"
        "As you wander around, you stumble upon a mysterious-looking building.\n\n"
        "It seems abandoned, but there's something intriguing about it.")

    # Create the embedded message for the first part with a green color
    first_part_embed = Embed(description=first_part_text, color=0x008000)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Wait for a moment before sending the second part
    await asyncio.sleep(2)

    # Define the text for the second part of the message
    second_part_text = (
        "Will you investigate the building?\n\n"
        "1. Yes, I'm curious to see what's inside.\n"
        "2. Maybe later, I'll continue exploring the city for now.")

    # Create the embedded message for the second part with a green color
    second_part_embed = Embed(description=second_part_text, color=0x008000)

    # Send the second part of the message
    await self.message.channel.send(embed=second_part_embed)

    # Define a check function to validate the user's response
    def check(m):
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for the user's response with a timeout of 20 seconds
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.investigate_abandoned_building()
      elif choice == '2':
        await self.continue_exploring_city()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def final_encounter(self):
    """
        Concludes the storyline with a final encounter or event.
        """
    first_part_text = (
        "**With your victory in the tournament, you've become a local hero in Fula City.**\n\n"
        "As you bask in the glory, you receive news of a disturbance at the outskirts of the city.\n\n"
        "Rumors of a powerful Legendary Pokémon causing trouble spread like wildfire."
    )

    # Create the embedded message for the first part with a blue color
    first_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_embed)
    await asyncio.sleep(2)

    # Define the text for the second part of the message
    second_part_text = (
        "Will you investigate and confront the Legendary Pokémon?\n"
        "1. Yes, I'll face the Legendary Pokémon and protect Fula City!\n"
        "2. No, I'll leave it to the authorities.")

    # Create the embedded message for the second part with a blue color
    second_embed = Embed(description=second_part_text, color=0x0000FF)

    # Send the second part of the message
    await self.message.channel.send(embed=second_embed)

    # Define a check function to validate the user's response
    def check(m):
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for the user's response with a timeout of 20 seconds
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.confront_legendary_pokemon()
      elif choice == '2':
        await self.leave_it_to_authorities()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def confront_legendary_pokemon(self):
    """
    Confronts the Legendary Pokémon causing trouble at the outskirts of Fula City.
    """
    part1_text = (
        "**You bravely decide to confront the Legendary Pokémon.**\n\n"
        "With your trusted Pokémon by your side, you head towards the outskirts of Fula City."
    )

    part2_text = (
        "The Legendary Pokémon appears before you, its power overwhelming.\n\n"
        "It's a fierce battle, but you refuse to back down.\n\n"
        "With determination and strategy, you manage to weaken the Legendary Pokémon."
    )

    part3_text = (
        "As it retreats, Fula City is safe once again, thanks to your heroism.\n\n"
        "You're hailed as a true Pokémon Champion, admired by all.\n\n"
        "With your adventure in Fula City coming to a close, you bid farewell to new friends and head towards your next destination."
        "\n\nBut the memories of your journey in Fula City will always remain with you."
    )

    # Create embedded messages for each part with different colors
    part1_embed = Embed(description=part1_text, color=0xFFA500)  # Orange
    part2_embed = Embed(description=part2_text, color=0x00FF00)  # Green
    part3_embed = Embed(description=part3_text, color=0x0000FF)  # Blue

    # Send each part of the message with a delay between them
    await self.message.channel.send(embed=part1_embed)
    await asyncio.sleep(2)  # Wait for 2 seconds before sending the next part
    await self.message.channel.send(embed=part2_embed)
    await asyncio.sleep(2)  # Wait for 2 seconds before sending the final part
    await self.send_image("legendary_pokemon.jpeg")
    await self.message.channel.send(embed=part3_embed)
    await self.send_image("end.jpeg")
    await self.message.channel.send("\n--- The End ---")

  async def continue_exploring_city(self):
    """
        Continues exploring Fula City after deciding not to investigate the abandoned building immediately.
        """
    first_part_text = (
        "**You decide to continue exploring Fula City.**\n\n"
        "With your victory in the tournament, you've become a local hero in Fula City."
    )

    # Create the embedded message for the first part with a blue color
    first_part_embed = Embed(description=first_part_text, color=0x0000FF)

    # Send the first part of the message
    await self.message.channel.send(embed=first_part_embed)

    # Wait for a moment before sending the second part
    await asyncio.sleep(2)

    # Define the text for the second part of the message
    second_part_text = (
        "As you bask in the glory, you receive news of a disturbance at the outskirts of the city.\n\n"
        "Rumors of a powerful Legendary Pokémon causing trouble spread like wildfire.\n\n"
        "Will you investigate and confront the Legendary Pokémon?\n\n"
        "1. Yes, I'll face the Legendary Pokémon and protect Fula City!\n"
        "2. No, I'll leave it to the authorities.")

    # Create the embedded message for the second part with a green color
    second_part_embed = Embed(description=second_part_text, color=0x008000)

    # Send the second part of the message
    await self.message.channel.send(embed=second_part_embed)

    # Define a check function to validate the user's response
    def check(m):
      return m.author == self.message.author and m.channel == self.message.channel and m.content in [
          '1', '2'
      ]

    try:
      # Wait for the user's response with a timeout of 20 seconds
      response = await self.bot.wait_for('message', check=check, timeout=20.0)
      choice = response.content

      # Process the user's choice
      if choice == '1':
        await self.confront_legendary_pokemon()
      elif choice == '2':
        await self.leave_it_to_authorities()

    except asyncio.TimeoutError:
      # Handle timeout if no response is received within the specified timeout duration
      await self.message.channel.send("Time's up! Please try again.")

  async def leave_it_to_authorities(self):
    """
        Decides to leave the confrontation with the Legendary Pokémon to the authorities.
        """
    message_text = (
        "**You decide to leave the confrontation with the Legendary Pokémon to the authorities.**\n\n"
        "You inform them of the situation, and they assure you that they'll handle it.\n\n"
        "With your part done, you continue your journey, knowing that Fula City is in safe hands."
    )

    # Create an embedded message with a color
    embed_message = Embed(description=message_text, color=0xFF0000)  # Red

    # Send the embedded message
    await self.message.channel.send(embed=embed_message)
    await self.send_image("end.jpeg")
    await self.message.channel.send("\n--- The End ---")
