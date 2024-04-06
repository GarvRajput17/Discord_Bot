import requests
from PIL import Image, ImageOps


API_URL = "https://pokeapi.co/api/v2"

def fetch_pokemon_info(index):
    
    url = f"{API_URL}/pokemon/{index}"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except requests.RequestException:
        return None

def poki_info(pokedex_number, front_sprite=True):
    face_image = f'sprites/front/{pokedex_number}.png'
    behind_image = f'sprites/back/{pokedex_number}.png'
    sprite_path = face_image if front_sprite else behind_image
# Modify size
    try:
        img = Image.open(sprite_path).convert('RGBA')
        if img.size == (96, 96):
            img = img.resize((144, 144), Image.Resampling.LANCZOS)
        return img
    except (TypeError, OSError):
        return None

def battle_image(pokedex_number1, pokedex_number2):
    img1 = poki_info(pokedex_number1, front_sprite=False)
    img2 = poki_info(pokedex_number2, front_sprite=True)

    if not img1 or not img2:
        return None

    bf = Image.open('temp/battle_background.png')
    bf.paste(img1, (40, 85), img1)
    bf.paste(img2, (240, 5), img2)

    bf_path = 'temp/bf.png'
    bf.save(bf_path)
    return bf_path

