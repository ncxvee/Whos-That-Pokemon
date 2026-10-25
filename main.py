import random
import requests

pokemon_list = [
    "bulbasaur",
    "charmander",
    "ditto",
    "eevee",
    "jigglypuff",
    "pikachu",
    "snorlax"
]

def get_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            print("Pokemon not found!")
            return None

        response.raise_for_status()
        data = response.json()

        abilities = [
            item["ability"]["name"].replace("-", " ").title()
            for item in data["abilities"]
        ]

        return {
            "name": data["name"].casefold(),
            "height": data["height"],
            "weight": data["weight"],
            "abilities": abilities
        }

    except requests.exceptions.RequestException as error:
        print("Network or API error:", error)
        return None

    except (ValueError, KeyError, TypeError) as error:
        print("Error reading Pokemon data:", error)
        return None

def play_game():
    while True:
        print("\n================================")
        print("       WHO'S THAT POKEMON?")
        print("================================")
        print("Guess the Pokemon!")
        print("You have 3 attempts.")

        print("\nChoose from these Pokemon:")
        for number, name in enumerate(pokemon_list, start=1):
            print(f"{number}. {name.title()}")

        chosen_name = random.choice(pokemon_list)
        pokemon = get_pokemon_data(chosen_name)

        if pokemon is None:
            print("Unable to start the game. Please try again.")
            return

        print("\nHere are your clues:")
        print(f"Height: {pokemon['height']} decimeters")
        print(f"Weight: {pokemon['weight']} hectograms")
        print("Abilities: " + ", ".join(pokemon["abilities"]))

        attempts_used = 0
        max_attempts = 3

        while attempts_used < max_attempts:
            guess = input(
                f"\nAttempt {attempts_used + 1}/{max_attempts} "
                "- Guess the Pokemon: "
            ).strip().casefold()

            if not guess:
                print(
                    "Please enter a Pokemon name. "
                )
                continue

            if guess not in pokemon_list:
                print(
                    "Pokemon not on the list! Please check your spelling. "
                )
                continue

            attempts_used += 1

            if guess == pokemon["name"]:
                print("\nCorrect! You guessed the Pokemon!")
                break

            print(
                f"Incorrect! You have "
                f"{max_attempts - attempts_used} attempt(s) left."
            )

        else:
            print(
                f"\nOut of attempts! The Pokemon was "
                f"{pokemon['name'].title()}."
            )

        while True:
            play_again = input(
                "\nWould you like to play again? (yes/no): "
            ).strip().casefold()

            if play_again in ("yes", "y"):
                break

            if play_again in ("no", "n"):
                print("\nThanks for playing!")
                return

            print("Please enter yes or no.")

if __name__ == "__main__":
    play_game()
