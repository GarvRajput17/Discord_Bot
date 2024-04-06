import requests
import random

POKEAPI_URL = "https://pokeapi.co/api/v2"

ABILITIES = ["attack", "defense", "special-attack", "special-defense"]

class Player:
    def __init__(self, user):
        self.user = user
        self.pokemon = None
        self.stats = None
        self.types = None

class Game:
    def __init__(self):
        self.players = {}
        self.round = 0

    def add_player(self, player):
        self.players[player.user.id] = player

    def get_player(self, user):
        return self.players.get(user.id)

    async def load_pokemon(self):
        try:
            pokemon_id = random.randint(1, 800)
            pokemon_data = await self.get_pokemon_data(pokemon_id)
            return pokemon_data
        except Exception as e:
            print(f"Error fetching Pokémon data for ID {pokemon_id}: {e}")
            return None

    async def get_pokemon_data(self, pokemon_id):
        url = f"{POKEAPI_URL}/pokemon/{pokemon_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching Pokémon data for ID {pokemon_id}: {response.status_code}")
            return None

    async def start_battle(self, channel):
        for player_id, player in self.players.items():
            player.pokemon = await self.load_pokemon()
            if player.pokemon:
                player.stats = await self.get_pokemon_stats(player.pokemon)
                player.types = await self.get_pokemon_types(player.pokemon)
                await channel.send(f"{player.user.name}'s Pokemon: {player.pokemon['name']}")
                await channel.send(f"Types: {player.types}")
                await channel.send(f"Stats: {player.stats}")
            else:
                await channel.send(f"Failed to load a Pokémon for {player.user.name}")

        await channel.send("Calculating results...")

        stats_sum = {player_id: sum(player.stats) for player_id, player in self.players.items()}

        if list(self.players.keys())[0] > list(self.players.keys())[1]:
            winner = self.players[list(self.players.keys())[0]].user.name
            await channel.send(f"Congratulations {winner}, You have won the Round!")
        elif list(self.players.keys())[0] < list(self.players.keys())[1]:
            winner = self.players[list(self.players.keys())[1]].user.name
            await channel.send(f"Congratulations {winner}, You have won the Round!")
        else:
            await channel.send("Round ended in a tie!")

    async def get_pokemon_stats(self, pokemon_info):
        stats = pokemon_info.get('stats', [])
        relevant_stats = ['attack', 'defense', 'special-attack', 'special-defense']
        stats_dict = {stat['stat']['name']: stat['base_stat'] for stat in stats}
        return [stats_dict[stat] for stat in relevant_stats]

    async def get_pokemon_types(self, pokemon_info):
        types = pokemon_info.get('types', [])
        return [type_entry['type']['name'] for type_entry in types]

game = Game()

async def join(message):
    player = Player(message.author)
    game.add_player(player)
    await message.channel.send(f"{message.author.name} has joined the game.")

async def start_game(message):
    if len(game.players) < 2:
        await message.channel.send("Need at least 2 players to start the game.")
        return
    await game.start_battle(message.channel)
