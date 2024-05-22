import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import json
import requests


class PokemonGame:

    def __init__(self, bot):
        self.bot = bot
        self.pokemon_data = read_pokemon_data('pokemon_Data.txt')
        self.sp_attack_used = [False, False]  # [player1, player2]
        self.sp_defense_used = [False, False]  # [player1, player2]

    async def challenge(self, ctx, opponent_id):
        challenger_id = ctx.author.id
        embed = discord.Embed(
            title="Battle Challenge",
            description=f"<@{challenger_id}> has challenged <@{opponent_id}> to a battle!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

        await ctx.send(f"<@{opponent_id}>, type `!ready` under 30 seconds to accept the challenge.")

        def check_ready(message):
            return message.author.id == opponent_id and message.content.lower() == '!ready'

        try:
            ready_message = await self.bot.wait_for('message', check=check_ready, timeout=30)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="Battle Challenge",
                description=f"<@{opponent_id}> did not accept the challenge in time.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return False

        embed = discord.Embed(
            title="Battle Challenge",
            description=f"<@{opponent_id}> has accepted the challenge!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        return True

    async def choose_pokemon(self, ctx, user_id):
        user_inventory = self.bot.user_inventory.get(str(user_id), {})
        pokemon_options = user_inventory.keys()

        embed = discord.Embed(
            title="Choose Your Pokémon",
            description="Select your Pokémon from the options below:",
            color=discord.Color.blue()
        )

        class PokemonSelectView(View):
            def __init__(self):
                super().__init__()
                for pokemon_name in pokemon_options:
                    button = Button(label=pokemon_name, style=discord.ButtonStyle.primary)
                    button.callback = self.pokemon_callback
                    self.add_item(button)
                self.selected_pokemon = None

            async def pokemon_callback(self, interaction: discord.Interaction):
                self.selected_pokemon = interaction.component.label
                self.stop()

        view = PokemonSelectView()
        msg = await ctx.send(embed=embed, view=view)

        await view.wait()
        if view.selected_pokemon:
            return view.selected_pokemon
        else:
            embed = discord.Embed(
                title="Choose Your Pokémon",
                description=f"<@{user_id}> took too long to respond.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return None

    async def attack(self, ctx, player):
        embed = discord.Embed(
            title="Attack Chosen",
            description=f"<@{player}> chose to attack!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        return 'attack'

    async def defense(self, ctx, player):
        embed = discord.Embed(
            title="Defense Chosen",
            description=f"<@{player}> chose to defend!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        return 'defense'

    async def sp_attack(self, ctx, player):
        player_index = 0 if ctx.author.id == player else 1
        if not self.sp_attack_used[player_index]:
            embed = discord.Embed(
                title="Special Attack Chosen",
                description=f"<@{player}> chose to use special attack!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            self.sp_attack_used[player_index] = True
            return 'sp_attack'
        else:
            embed = discord.Embed(
                title="Special Attack Unavailable",
                description="You have already used special attack once in this battle!",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return None

    async def sp_defense(self, ctx, player):
        player_index = 0 if ctx.author.id == player else 1
        if not self.sp_defense_used[player_index]:
            embed = discord.Embed(
                title="Special Defense Chosen",
                description=f"<@{player}> chose to use special defense!",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
            self.sp_defense_used[player_index] = True
            return 'sp_defense'
        else:
            embed = discord.Embed(
                title="Special Defense Unavailable",
                description="You have already used special defense once in this battle!",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return None

    async def surrender(self, ctx, player_id):
        embed = discord.Embed(
            title="Player Surrendered",
            description=f"<@{player_id}> has surrendered!",
            color=discord.Color.dark_red()
        )
        await ctx.send(embed=embed)
        other_player_id = ctx.author.id if player_id != ctx.author.id else ctx.opponent.id
        await update_user_data(player_id, 'loss')
        await update_user_data(other_player_id, 'win')
        embed = discord.Embed(
            title="Battle Result",
            description=f"<@{other_player_id}> wins by surrender!",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)
        return True

    async def run_battle(self, ctx, player1_id, player2_id):
        player1_hp = 500
        player2_hp = 500

        player1_pokemon = await self.choose_pokemon(ctx, player1_id)
        player2_pokemon = await self.choose_pokemon(ctx, player2_id)

        if not player1_pokemon or not player2_pokemon:
            embed = discord.Embed(
                title="Battle Initialization Failed",
                description="Could not choose Pokémon. Exiting battle.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        player1_image_url = await self.load_pokemon_image(player1_pokemon)
        player2_image_url = await self.load_pokemon_image(player2_pokemon)

        embed = discord.Embed(
            title="Pokémon Selection",
            description="Pokémon selected for the battle:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Player 1", value=player1_pokemon)
        embed.add_field(name="Player 2", value=player2_pokemon)
        await ctx.send(embed=embed)

        if player1_image_url:
            await ctx.send(player1_image_url)
        if player2_image_url:
            await ctx.send(player2_image_url)

        player_turn = 1

        while player1_hp > 0 and player2_hp > 0:
            current_player_id = player1_id if player_turn == 1 else player2_id
            current_player_pokemon = player1_pokemon if player_turn == 1 else player2_pokemon
            opponent_player_id = player2_id if player_turn == 1 else player1_id
            opponent_player_hp = player2_hp if player_turn == 1 else player1_hp

            action = await self.choose_action(ctx, current_player_id)
            if action == 'attack':
                damage = self.pokemon_data[current_player_pokemon]['attack']
                opponent_player_hp -= damage
                if player_turn == 1:
                    player2_hp = opponent_player_hp
                else:
                    player1_hp = opponent_player_hp

            elif action == 'defense':
                defense = self.pokemon_data[current_player_pokemon]['defense']
                opponent_player_hp -= defense // 2  # Simple defense logic

            elif action == 'sp_attack':
                sp_attack = self.pokemon_data[current_player_pokemon]['sp_attack']
                opponent_player_hp -= sp_attack
                if player_turn == 1:
                    player2_hp = opponent_player_hp
                else:
                    player1_hp = opponent_player_hp

            elif action == 'sp_defense':
                sp_defense = self.pokemon_data[current_player_pokemon]['sp_defense']
                opponent_player_hp -= sp_defense // 2  # Simple special defense logic

            elif action == 'surrender':
                await self.surrender(ctx, current_player_id)
                return

            embed = discord.Embed(
                title="Battle Update",
                description=f"{current_player_pokemon} attacked! Remaining HP: Player 1 - {player1_hp}, Player 2 - {player2_hp}",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

            if player1_hp <= 0 or player2_hp <= 0:
                winner_id = player1_id if player2_hp <= 0 else player2_id
                loser_id = player2_id if winner_id == player1_id else player1_id
                await update_user_data(winner_id, 'win')
                await update_user_data(loser_id, 'loss')

                embed = discord.Embed(
                    title="Battle Result",
                    description=f"<@{winner_id}> wins the battle!",
                    color=discord.Color.gold()
                )
                await ctx.send(embed=embed)
                return

            player_turn = 2 if player_turn == 1 else 1

    async def choose_action(self, ctx, player_id):
        embed = discord.Embed(
            title="Choose Your Action",
            description="Select your action from the options below:",
            color=discord.Color.blue()
        )

        class ActionSelectView(View):
            def __init__(self):
                super().__init__()
                actions = ["Attack", "Defense", "Special Attack", "Special Defense", "Surrender"]
                for action in actions:
                    button = Button(label=action, style=discord.ButtonStyle.primary if action != "Surrender" else discord.ButtonStyle.danger)
                    button.callback = self.action_callback
                    self.add_item(button)
                self.selected_action = None

            async def action_callback(self, interaction: discord.Interaction):
                self.selected_action = interaction.component.label.lower().replace(" ", "_")
                self.stop()

        view = ActionSelectView()
        msg = await ctx.send(embed=embed, view=view)

        await view.wait()
        if view.selected_action:
            return view.selected_action
        else:
            embed = discord.Embed(
                title="Action Selection",
                description=f"<@{player_id}> took too long to respond.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return None

    async def load_pokemon_image(self, pokemon_name):
        url = f"https://api.pokemontcg.io/v2/cards?q=name:{pokemon_name}&pageSize=1"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                image_url = data['data'][0]['images']['small']
                return image_url
            else:
                return None
        else:
            return None


async def update_user_data(user_id, result):
    with open('user_data.json', 'r') as file:
        user_data = json.load(file)

    if result == 'win':
        user_data[str(user_id)]['matches_won'] += 1
        user_data[str(user_id)]['user_currency'] += 100
    elif result == 'loss':
        user_data[str(user_id)]['matches_lost'] += 1
        user_data[str(user_id)]['user_currency'] -= 50

    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)


def read_pokemon_data(file_path):
    pokemon_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            fields = line.strip().split('\t')
            number = fields[0]
            name = fields[1]
            type1 = fields[2]
            type2 = fields[3]
            hp = int(fields[4])
            attack = int(fields[5])
            defense = int(fields[6])
            sp_attack = int(fields[7])
            sp_defense = int(fields[8])
            speed = int(fields[9])
            pokemon_data[name] = {
                'number': number,
                'type1': type1,
                'type2': type2,
                'hp': hp,
                'attack': attack,
                'defense': defense,
                'sp_attack': sp_attack,
                'sp_defense': sp_defense,
                'speed': speed
            }
    return pokemon_data

# Example usage with discord.py bot initialization
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="$", intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.command()
async def battle(ctx, opponent: discord.Member):
    game = PokemonGame(client)
    if await game.challenge(ctx, opponent.id):
        await game.run_battle(ctx, ctx.author.id, opponent.id)

client.run('YOUR_BOT_TOKEN')
