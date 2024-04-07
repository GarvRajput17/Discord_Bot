import requests
import random

POKEAPI_URL = "https://pokeapi.co/api/v2"

ABILITIES = ["Attack", "Defense", "Special Attack", "Special Defense"]

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
            print(
                f"Error fetching Pokémon data for ID {pokemon_id}: {response.status_code}"
            )
            return None

    async def start_battle(self, channel):
        for player_id, player in self.players.items():
            player.pokemon = await self.load_pokemon()
            if player.pokemon:
                player.stats = [stat['base_stat'] for stat in player.pokemon['stats']]
                player.types = [type_entry['type']['name'] for type_entry in player.pokemon['types']]
                await channel.send(
                    f"```\n{player.user.name}'s Pokemon: {player.pokemon['name']}\n```"
                )
                await channel.send(f"```\nTypes: {', '.join(player.types)}\n```")
                await channel.send(
                    f"```\nStats: {', '.join(str(stat) for stat in player.stats)}\n```"
                )
            else:
                await channel.send(
                    f"```\nFailed to load a Pokémon for {player.user.name}\n```"
                )

        await channel.send("```\n🔥🌟🔥 Calculating results... 🔥🌟🔥\n```")

        pts = {player_id: 0 for player_id in self.players.keys()}

        # Display each player's Pokémon's stats before proceeding to each round
        for stat_index, stat_name in enumerate(ABILITIES):
            for player_id, player in self.players.items():
                await channel.send(f"```\n{player.user.name}'s Pokemon {stat_name}: {player.stats[stat_index]}\n```")

        # Remaining battle logic...
        for i, stat_name in enumerate(ABILITIES):
            stat_values = [player.stats[i] for player in self.players.values()]
            max_stat = max(stat_values)
            winning_players = [
                player_id
                for player_id, stat_value in zip(self.players.keys(), stat_values)
                if stat_value == max_stat
            ]

            if len(winning_players) == 1:
                pts[winning_players[0]] += 1
                await channel.send(
                    f"```\n🎉 {self.players[winning_players[0]].user.name} won the {stat_name} round! 🎉\n```"
                )
            else:
                await channel.send(
                    f"```\n🤝 Round ended in a tie for {stat_name}! 🤝\n```"
                )

        # Display round results
        if list(pts.values())[0] > list(pts.values())[1]:
            winner = self.players[list(pts.keys())[0]].user.name
            await channel.send(
                f"```\n🏆 Congratulations {winner}, You have won the Round! 🏆\n```"
            )
        elif list(pts.values())[0] < list(pts.values())[1]:
            winner = self.players[list(pts.keys())[1]].user.name
            await channel.send(
                f"```\n🏆 Congratulations {winner}, You have won the Round! 🏆\n```"
            )
        else:
            await channel.send("```\n🤝 Round ended in a tie! 🤝\n```")

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
