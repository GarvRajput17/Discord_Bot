import asyncio


class PokemonPowerOfUs:

  def __init__(self, message,bot):
    self.character = None
    self.message = message
    self.bot = bot

  async def power_of_us_intro(self):
    await self.message.channel.send("Welcome to Pokémon: The Power of Us game!"
                                    )
    await asyncio.sleep(1)
    await self.message.channel.send(
        "You find yourself in the bustling seaside town of Fula City during the annual Wind Festival."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "This festival celebrates the legendary Pokémon Lugia, said to bring the wind that powers the city."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "As you explore the city, you encounter various characters and hear whispers of excitement in the air."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "It seems there's something extraordinary about to happen. Are you ready to embark on an adventure?"
    )
    await asyncio.sleep(2)
    await self.message.channel.send("Let's get started!\n")
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
        await self.message.channel.send("2. Risa")
        await self.message.channel.send("3. Toren")
        await self.message.channel.send("4. Callahan")
        await self.message.channel.send("5. Harriet")
        await self.message.channel.send("6. Margo")

        def check(m):
            return m.author == self.message.author and m.channel == self.message.channel and m.content.isdigit()

        try:
            response = await self.bot.wait_for('message', check=check, timeout=30.0)
            choice = int(response.content)
            self.user_input = choice
            if choice == 1:
                self.character = "Ash Ketchum"
                await self.ash_intro()
            elif choice == 2:
                self.character = "Risa"
                await self.risa_intro()
            elif choice == 3:
                self.character = "Toren"
                await self.toren_intro()
            # Add additional conditions for other characters here
            else:
                await self.message.channel.send(
                  "Invalid choice. Please select a number between 1 and 6.")
                await self.choose_character()
        except asyncio.TimeoutError:
            await self.message.channel.send("\nTime's up! Please try again.")


  async def ash_intro(self):
    await self.message.channel.send("\nYou've chosen to play as Ash Ketchum.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "As Ash, you're excited to explore Fula City and participate in the Wind Festival."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You decide to head towards the center of the city where the festivities are in full swing."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Along the way, you encounter various Pokémon trainers and enthusiasts, all buzzing with excitement."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Suddenly, you hear a commotion nearby. You rush to the scene and find a Pokémon in distress."
    )
    await asyncio.sleep(2)
    await self.message.channel.send("What will you do?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Approach the Pokémon cautiously.")
    await self.message.channel.send(
        "2. Call out to the Pokémon and try to calm it down.")
    def check(m):
        
        return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    await self.message.channel.send(
        "\nYou cautiously approach the distressed Pokémon.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "It seems scared and defensive, but you try to convey your friendly intentions."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Slowly, the Pokémon begins to calm down and allows you to get closer."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "As you reach out to help the Pokémon, you notice something glimmering nearby."
    )
    await asyncio.sleep(2)
    await self.message.channel.send("What will you do?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Investigate the glimmering object.")
    await self.message.channel.send("2. Focus on comforting the Pokémon.")

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    await self.message.channel.send(
        "\nYou call out to the distressed Pokémon in a soothing voice.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "Your gentle approach seems to have an effect as the Pokémon starts to calm down."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Suddenly, you notice something glimmering nearby.")
    await asyncio.sleep(2)
    await self.message.channel.send("What will you do?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Investigate the glimmering object.")
    await self.message.channel.send("2. Keep focusing on calming the Pokémon.")

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    await self.message.channel.send(
        "\nYou approach the glimmering object and discover a valuable item.")
    await asyncio.sleep(1)
    await self.message.channel.send("It could be useful on your journey.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "As you pick up the item, you hear a voice calling out for help from further ahead."
    )
    await asyncio.sleep(2)
    await self.message.channel.send("Will you investigate?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Proceed cautiously towards the voice.")
    await self.message.channel.send(
        "2. Stay where you are and observe the surroundings.")

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    await self.message.channel.send(
        "\nYou focus on comforting the distressed Pokémon.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "Your gentle approach seems to work as the Pokémon starts to relax.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Suddenly, you notice something glimmering nearby.")
    await asyncio.sleep(2)
    await self.message.channel.send("What will you do?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Investigate the glimmering object.")
    await self.message.channel.send("2. Keep comforting the Pokémon.")

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

    try:
            # Wait for a message from the user that satisfies the check function
            response = await self.bot.wait_for('message', check=check, timeout=20.0)
            choice = response.content

            # Process the user's choice
            if choice == '1':
                await self.investigate_glimmering_object()
            elif choice == '2':
                await self.keep_focusing_on_comforting_pokemon()

    except asyncio.TimeoutError:
            # Handle timeout if no response is received within the specified timeout duration
            await self.message.channel.send("Time's up! Please try again.")


  async def keep_focusing_on_calming_pokemon(self):
    await self.message.channel.send(
        "\nYou continue to focus on calming the distressed Pokémon.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "Your soothing voice and gestures seem to be working.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Suddenly, you notice something glimmering nearby.")
    await asyncio.sleep(2)
    await self.message.channel.send("What will you do?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Investigate the glimmering object.")
    await self.message.channel.send("2. Keep your attention on the Pokémon.")

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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


  async def proceed_towards_voice(self):
    await self.message.channel.send(
        "\nYou cautiously proceed towards the direction of the voice.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "As you get closer, you see a group of Pokémon cornered by a group of wild Pokémon."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Without hesitation, you jump into action to help the trapped Pokémon."
    )
    await asyncio.sleep(2)
    await self.message.channel.send("What will you do?")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "1. Engage in battle to defeat the wild Pokémon.")
    await self.message.channel.send(
        "2. Try to distract the wild Pokémon to give the trapped Pokémon a chance to escape."
    )

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    await self.message.channel.send(
        "\nYou decide to stay where you are and observe the surroundings.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "From your vantage point, you notice a group of Pokémon cornered by a group of wild Pokémon."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You realize they're in trouble and need your help.")
    await asyncio.sleep(2)
    await self.message.channel.send("What will you do?")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "1. Rush in to engage in battle and help the trapped Pokémon.")
    await self.message.channel.send(
        "2. Try to come up with a plan to distract the wild Pokémon and aid the trapped Pokémon."
    )

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    await self.message.channel.send(
        "\nYou decide to engage in battle to defeat the wild Pokémon and help the trapped Pokémon."
    )
    await asyncio.sleep(1)
    await self.message.channel.send(
        "Your Pokémon leap into action, ready to fight alongside you.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "The battle is intense, but with your skill and determination, you manage to defeat the wild Pokémon."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "The trapped Pokémon are grateful for your help and express their thanks."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You feel a sense of accomplishment as you continue your journey through Fula City."
    )
    await asyncio.sleep(2)
    await self.original_story_continuation()

  async def distract_wild_pokemon(self):
    await self.message.channel.send(
        "\nYou come up with a plan to distract the wild Pokémon and aid the trapped Pokémon."
    )
    await asyncio.sleep(1)
    await self.message.channel.send(
        "You gather some nearby items and make noise to get the attention of the wild Pokémon."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Your plan works, and the wild Pokémon are momentarily distracted, allowing the trapped Pokémon to escape."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "The trapped Pokémon express their gratitude and flee to safety.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You feel satisfied with your quick thinking and resourcefulness as you continue exploring Fula City."
    )
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
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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


  async def participate_in_tournament(self):
    await self.message.channel.send(
        "\nYou decide to participate in the Pokémon battle tournament.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "Your Pokémon are ready, and you're eager to showcase your skills.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "The battles are intense, but you manage to win several rounds and make it to the final match."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "In the final match, you face off against a formidable opponent.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "It's a tough battle, but with determination and teamwork, you emerge victorious!"
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "The crowd cheers for your impressive performance, and you feel proud of your accomplishments."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "With the tournament over, you continue your exploration of Fula City, eager for more adventures."
    )
    await asyncio.sleep(2)
    await explore_more_of_fula_city()

  async def explore_more_of_fula_city(self):
    await self.message.channel.send(
        "\nYou decide to explore more of Fula City before participating in the tournament."
    )
    await asyncio.sleep(1)
    await self.message.channel.send(
        "There are so many interesting places to see and people to meet!")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "As you wander around, you stumble upon a mysterious-looking building."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "It seems abandoned, but there's something intriguing about it.")
    await asyncio.sleep(2)
    await self.message.channel.send("Will you investigate the building?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Yes, I'm curious to see what's inside."
                                    )
    await self.message.channel.send(
        "2. Maybe later, I'll continue exploring the city for now.")

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    await self.message.channel.send(
        "\nYou decide to investigate the abandoned building.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "As you enter, you're greeted by darkness and silence.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You cautiously explore the interior, discovering old equipment and remnants of past experiments."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Suddenly, you hear a strange noise coming from deeper within the building."
    )
    await asyncio.sleep(2)
    await self.message.channel.send("What will you do?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Investigate the source of the noise.")
    await self.message.channel.send(
        "2. Leave the building and come back later with backup.")

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    await self.message.channel.send(
        "\nYou decide to continue exploring the city.")
    await asyncio.sleep(1)
    await self.message.channel.send("There's still so much to see and do!")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "As you wander through the streets, you come across a bustling marketplace."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Merchants are selling all kinds of goods, including rare Pokémon items."
    )
    await asyncio.sleep(2)
    await self.message.channel.send("Will you browse the marketplace?")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "1. Yes, I'm curious to see what they have.")
    await self.message.channel.send(
        "2. Maybe later, I'll keep exploring for now.")

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

    try:
            # Wait for a message from the user that satisfies the check function
            response = await self.bot.wait_for('message', check=check, timeout=20.0)
            choice = response.content

            # Process the user's choice
            if choice == '1':
                await self.browse_marketplace()
            elif choice == '2':
                await self.keep_exploring_without_marketplace()

    except asyncio.TimeoutError:
            # Handle timeout if no response is received within the specified timeout duration
            await self.message.channel.send("Time's up! Please try again.")


  async def browse_marketplace(self):
    await self.message.channel.send("\nYou decide to browse the marketplace.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "There are so many interesting items for sale, including rare Pokémon items."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "As you examine the goods, you come across a vendor selling ancient artifacts."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "One particular artifact catches your eye—a mysterious stone with strange markings."
    )
    await asyncio.sleep(2)
    await self.message.channel.send("Will you purchase the artifact?")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "1. Yes, it could be valuable or hold some secrets.")
    await self.message.channel.send("2. No, it seems too risky.")

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    await self.message.channel.send(
        "\nYou decide to purchase the mysterious artifact.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "The vendor accepts your offer, and you acquire the artifact.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "As you hold it in your hands, you feel a strange energy emanating from it."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You're not sure what its purpose is, but you're excited to find out!")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "With the artifact in your possession, you continue your exploration of Fula City."
    )
    await asyncio.sleep(2)
    # Continue with the rest of the storyline

  async def decide_not_to_purchase_artifact(self):
    await self.message.channel.send(
        "\nYou decide not to purchase the mysterious artifact.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "It seems too risky to acquire something with unknown powers.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You thank the vendor but politely decline the offer.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "With caution in mind, you continue your exploration of Fula City, wary of any potential dangers."
    )
    await asyncio.sleep(2)
    # Continue with the rest of the storyline

  async def investigate_source_of_noise(self):
    await self.message.channel.send(
        "\nYou decide to investigate the source of the noise.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "As you venture deeper into the building, the noise grows louder.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You finally reach the source—a hidden laboratory with strange equipment."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Inside, you find a group of researchers conducting experiments on Pokémon."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "They seem surprised by your presence but welcome you nonetheless.")
    await asyncio.sleep(2)
    await self.message.channel.send("What will you do?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Offer to help with their research.")
    await self.message.channel.send(
        "2. Express concern about the experiments and suggest safer alternatives."
    )

    def check(m):
            # Check if the message author is the same as the user who triggered the command
            # Check if the message is sent in the same channel as the prompt message
            # Check if the message content is either '1' or '2'
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    """
        Leaves the abandoned building and plans to return later with backup.
        """
    await self.message.channel.send(
        "\nYou decide to leave the building and come back later with backup.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "It's better to approach the situation with caution and not take any unnecessary risks."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You make a mental note to return to the abandoned building when you're better prepared."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "For now, you'll continue your exploration of Fula City, keeping an eye out for any other mysteries."
    )
    await asyncio.sleep(2)
    await self.original_story_continuation()

  async def original_story_continuation(self):
    """
        Continues the original storyline after leaving the abandoned building.
        """
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

        # Define a check function to validate the user's respons

    def check(m):
          # Check if the message author is the same as the user who triggered the command
          # Check if the message is sent in the same channel as the prompt message
          # Check if the message content is either '1' or '2'
          return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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




  async def participate_in_tournament(self):
    """
        Participates in the Pokémon battle tournament.
        """
    await self.message.channel.send(
        "\nYou decide to participate in the Pokémon battle tournament.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "Your Pokémon are ready, and you're eager to showcase your skills.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "The battles are intense, but you manage to win several rounds and make it to the final match."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "In the final match, you face off against a formidable opponent.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "It's a tough battle, but with determination and teamwork, you emerge victorious!"
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "The crowd cheers for your impressive performance, and you feel proud of your accomplishments."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "With the tournament over, you continue your exploration of Fula City, eager for more adventures."
    )
    await asyncio.sleep(2)
    await self.explore_more_of_fula_city()

  async def explore_more_of_fula_city(self):
    """
        Explores more of Fula City.
        """
    await self.message.channel.send(
        "\nYou decide to explore more of Fula City before participating in the tournament."
    )
    await asyncio.sleep(1)
    await self.message.channel.send(
        "There are so many interesting places to see and people to meet!")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "As you wander around, you stumble upon a mysterious-looking building."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "It seems abandoned, but there's something intriguing about it.")
    await asyncio.sleep(2)
    await self.message.channel.send("Will you investigate the building?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Yes, I'm curious to see what's inside."
                                    )
    await self.message.channel.send(
        "2. Maybe later, I'll continue exploring the city for now.")

        # Define a check function to validate the user's response
    def check(m):
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

    try:
            # Wait for the user's response with a timeout of 20 seconds
            response = await self.bot.wait_for('message', check=check, timeout=20.0)
            choice = response.content

            # Process the user's choice
            if response == '1':
                await self.investigate_abandoned_building()
            elif response == '2':
                await self.continue_exploring_city()

    except asyncio.TimeoutError:
            # Handle timeout if no response is received within the specified timeout duration
            await self.message.channel.send("Time's up! Please try again.")


  async def investigate_abandoned_building(self):
    """
        Investigates the abandoned building.
        """
    await self.message.channel.send(
        "\nYou decide to investigate the abandoned building.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "As you enter, you're greeted by darkness and silence.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You cautiously explore the interior, discovering old equipment and remnants of past experiments."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Suddenly, you hear a strange noise coming from deeper within the building."
    )
    await asyncio.sleep(2)
    await self.message.channel.send("What will you do?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Investigate the source of the noise.")
    await self.message.channel.send(
        "2. Leave the building and come back later with backup.")
    await self.message.channel.send(
        "3. Ignore the noise and continue exploring.")

        # Define a check function to validate the user's response
    def check(m):
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2', '3']

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
    await self.message.channel.send(
        "\nYou decide to investigate the source of the noise.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "As you venture deeper into the building, the noise grows louder.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You finally reach the source—a hidden laboratory with strange equipment."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Inside, you find a group of researchers conducting experiments on Pokémon."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "They seem surprised by your presence but welcome you nonetheless.")
    await asyncio.sleep(2)
    await self.message.channel.send("What will you do?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Offer to help with their research.")
    await self.message.channel.send(
        "2. Express concern about the experiments and suggest safer alternatives."
    )
    await self.message.channel.send(
        "3. Leave the laboratory and inform the authorities.")

        # Define a check function to validate the user's response
    def check(m):
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2', '3']

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
    await self.message.channel.send(
        "\nYou offer to help with their research, intrigued by the experiments."
    )
    await asyncio.sleep(1)
    await self.message.channel.send(
        "The researchers gladly accept your offer and invite you to assist them."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Together, you work on various experiments, learning new things about Pokémon."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Your contributions are valuable, and the researchers appreciate your assistance."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You feel proud to be a part of such important work.")
    await asyncio.sleep(2)
    await self.original_story_continuation()

  async def express_concern_and_suggest_alternatives(self):
    """
        Expresses concern about the experiments and suggests safer alternatives.
        """
    await self.message.channel.send(
        "\nYou express concern about the experiments and suggest safer alternatives."
    )
    await asyncio.sleep(1)
    await self.message.channel.send(
        "The researchers listen to your suggestions and agree to consider them."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "They appreciate your input and assure you that they'll prioritize the safety and well-being of Pokémon."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You feel relieved that your concerns were heard and respected.")
    await asyncio.sleep(2)
    await self.original_story_continuation()

  async def leave_lab_and_inform_authorities(self):
    """
        Leaves the laboratory and decides to inform the authorities about the experiments.
        """
    await self.message.channel.send(
        "\nYou decide to leave the laboratory and inform the authorities about the experiments."
    )
    await asyncio.sleep(1)
    await self.message.channel.send(
        "It's important to ensure the safety and well-being of Pokémon.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You make your way to the authorities and report what you witnessed.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "They assure you that they'll investigate the matter further.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "With your duty fulfilled, you continue your exploration of Fula City."
    )
    await asyncio.sleep(2)
    await self.original_story_continuation()

  async def leave_building_and_come_back_with_backup(self):
    """
        Leaves the abandoned building and plans to return later with backup.
        """
    await self.message.channel.send(
        "\nYou decide to leave the building and come back later with backup.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "It's better to approach the situation with caution and not take any unnecessary risks."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You make a mental note to return to the abandoned building when you're better prepared."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "For now, you'll continue your exploration of Fula City, keeping an eye out for any other mysteries."
    )
    await asyncio.sleep(2)
    await self.original_story_continuation()

  async def ignore_noise_and_continue_exploring(self):
    """
        Ignores the strange noise in the abandoned building and continues exploring.
        """
    await self.message.channel.send(
        "\nYou decide to ignore the noise and continue exploring.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "Perhaps it's best not to get involved in something that might be dangerous."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You focus on other parts of Fula City, searching for more clues and adventures."
    )
    await asyncio.sleep(2)
    await self.original_story_continuation()

  async def original_story_continuation(self):
    """
        Continues the original storyline after leaving the abandoned building or laboratory.
        """
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

        # Define a check function to validate the user's response
    def check(m):
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    """
        Participates in the Pokémon battle tournament.
        """
    await self.message.channel.send(
        "\nYou decide to participate in the Pokémon battle tournament.")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "Your Pokémon are ready, and you're eager to showcase your skills.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "The battles are intense, but you manage to win several rounds and make it to the final match."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "In the final match, you face off against a formidable opponent.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "It's a tough battle, but with determination and teamwork, you emerge victorious!"
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "The crowd cheers for your impressive performance, and you feel proud of your accomplishments."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "With the tournament over, you continue your exploration of Fula City, eager for more adventures."
    )
    await asyncio.sleep(2)
    await self.final_encounter()

  async def explore_more_of_fula_city(self):
    """
        Explores more of Fula City before participating in the tournament.
        """
    await self.message.channel.send(
        "\nYou decide to explore more of Fula City before participating in the tournament."
    )
    await asyncio.sleep(1)
    await self.message.channel.send(
        "There are so many interesting places to see and people to meet!")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "As you wander around, you stumble upon a mysterious-looking building."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "It seems abandoned, but there's something intriguing about it.")
    await asyncio.sleep(2)
    await self.message.channel.send("Will you investigate the building?")
    await asyncio.sleep(1)
    await self.message.channel.send("1. Yes, I'm curious to see what's inside."
                                    )
    await self.message.channel.send(
        "2. Maybe later, I'll continue exploring the city for now.")

        # Define a check function to validate the user's response
    def check(m):
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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


  async def continue_exploring_city(self):
    """
        Continues exploring Fula City after deciding not to investigate the abandoned building immediately.
        """
    await self.message.channel.send(
        "\nYou decide to continue exploring Fula City.")
    await self.final_encounter()

  async def final_encounter(self):
    """
        Concludes the storyline with a final encounter or event.
        """
    await self.message.channel.send(
        "\nWith your victory in the tournament, you've become a local hero in Fula City."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "As you bask in the glory, you receive news of a disturbance at the outskirts of the city."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Rumors of a powerful Legendary Pokémon causing trouble spread like wildfire."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "Will you investigate and confront the Legendary Pokémon?")
    await asyncio.sleep(1)
    await self.message.channel.send(
        "1. Yes, I'll face the Legendary Pokémon and protect Fula City!")
    await self.message.channel.send("2. No, I'll leave it to the authorities.")

        # Define a check function to validate the user's response
    def check(m):
            return m.author == self.message.author and m.channel == self.message.channel and m.content in ['1', '2']

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
    await self.message.channel.send(
        "\nYou bravely decide to confront the Legendary Pokémon.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "With your trusted Pokémon by your side, you head towards the outskirts of Fula City."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "The Legendary Pokémon appears before you, its power overwhelming.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "It's a fierce battle, but you refuse to back down.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "With determination and strategy, you manage to weaken the Legendary Pokémon."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "As it retreats, Fula City is safe once again, thanks to your heroism."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You're hailed as a true Pokémon Champion, admired by all.")
    await asyncio.sleep(2)
    await self.message.channel.send(
        "With your adventure in Fula City coming to a close, you bid farewell to new friends and head towards your next destination."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "But the memories of your journey in Fula City will always remain with you."
    )
    await asyncio.sleep(2)
    await self.message.channel.send("\n--- The End ---")

  async def leave_it_to_authorities(self):
    """
        Decides to leave the confrontation with the Legendary Pokémon to the authorities.
        """
    await self.message.channel.send(
        "\nYou decide to leave the confrontation with the Legendary Pokémon to the authorities."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "You inform them of the situation, and they assure you that they'll handle it."
    )
    await asyncio.sleep(2)
    await self.message.channel.send(
        "With your part done, you continue your journey, knowing that Fula City is in safe hands."
    )
    await asyncio.sleep(2)
    await self.message.channel.send("\n--- The End ---")
