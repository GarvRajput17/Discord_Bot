import os
import discord
import requests
import time
import asyncio
import random
import json

class Pokedex:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"

    async def get_pokemon_by_id(self, index):
        try:
            url = f"{self.base_url}/pokemon/{index}"
            response = requests.get(url)
            data = response.json()
            return data
        except Exception as e:
            print(f"Error fetching data for Pokémon with ID {index}: {e}")
            return None


class pika:
    def __init__(self):
        self.state = {
            'activeQuiz': False,
            'pokemon': {}
        }
        self.pokedex = Pokedex() 

    async def reset_state(self):
        self.state = {
            'activeQuiz': False,
            'pokemon': {}
        }

    async def pick_random_pokemon(self):
        index = random.randint(1, 100)
        pokemon_data = await self.pick_pokemon(index)
        return pokemon_data

    async def pick_pokemon(self, index):
        try:
            self.state['activeQuiz'] = True
            pokemon_info = await self.pokedex.get_pokemon_by_id(index)  # Use the pokedex instance
            pokemon = {
                'form': pokemon_info['forms'][0]['name'],
                'sprite': pokemon_info['sprites']['front_default']
            }
            self.state['pokemon'] = pokemon
            return pokemon
        except Exception as e:
            print("[o_O pickPokemon] Something went wrong while picking a random Pokémon!")
            print(e)
            await self.reset_state()
            return None

    async def check_pokemon(self, name):
        if self.state['pokemon']['form'].lower() == name.lower():
            await self.reset_state()
            return True
        return False

wtp = pika()


async def start_quiz(message):
    if not wtp.state['activeQuiz']:
        try:
            pokemon_data = await wtp.pick_random_pokemon()
            if pokemon_data:
                embed = discord.Embed(title="WHO'S THAT POKÉMON?", color=discord.Color.blue())
                embed.set_image(url=pokemon_data['sprite'])
                await message.channel.send(embed=embed)
                await message.channel.send("Type your guess using `$guess <pokemon_name>`")
                # Set a timeout for guessing
                await asyncio.sleep(20)
                if wtp.state['activeQuiz']:
                    await wtp.reset_state()
                    await message.channel.send(f"The correct answer was {pokemon_data['form'].capitalize()}.")
        except Exception as e:
            await message.channel.send("Couldn't start the quiz. Try again later.")
            print(e)

async def guess_pokemon(message):
    if wtp.state['activeQuiz']:
        guess = message.content.split(' ', 1)[1].lower()
        if await wtp.check_pokemon(guess):
            embed = discord.Embed(description="**YOU GOT IT RIGHT!**", color=discord.Color.green())
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(description="**WRONG GUESS!**", color=discord.Color.red())
            await message.channel.send(embed=embed)
    else:
        await message.channel.send("No active quiz. Start one using `$startquiz`.")

