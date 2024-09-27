import random

class Character:
    def __init__(self, name):
        self.name = name

class Weapon:
    def __init__(self, name):
        self.name = name

class Room:
    def __init__(self, name):
        self.name = name

class ClueGame:
    def __init__(self):
        self.characters = []
        self.weapons = []
        self.rooms = []
        self.knowledge_base = []
        self.potential_hints = []

    def setup_game(self):
        print("Please enter the characters (type 'done' when finished):")
        while True:
            char_name = input("Character name: ")
            if char_name.lower() == 'done':
                break
            self.characters.append(Character(char_name))

        print("Please enter the weapons (type 'done' when finished):")
        while True:
            weapon_name = input("Weapon name: ")
            if weapon_name.lower() == 'done':
                break
            self.weapons.append(Weapon(weapon_name))

        print("Please enter the rooms (type 'done' when finished):")
        while True:
            room_name = input("Room name: ")
            if room_name.lower() == 'done':
                break
            self.rooms.append(Room(room_name))

        self.build_knowledge_base()

    def build_knowledge_base(self):
        # Preguntar sobre personajes que no son el asesino
        for character in self.characters:
            response = input(f"Is {character.name} the murderer? (yes/no): ").strip().lower()
            if response == 'no':
                self.knowledge_base.append(lambda murderer, weapon, room, name=character.name: murderer.name != name)
                self.potential_hints.append(f"{character.name} is not the murderer.")

        # Preguntar sobre armas que no fueron utilizadas
        for weapon in self.weapons:
            response = input(f"Was the weapon {weapon.name} used? (yes/no): ").strip().lower()
            if response == 'no':
                self.knowledge_base.append(lambda murderer, weapon_obj, room, name=weapon.name: weapon_obj.name != name)
                self.potential_hints.append(f"{weapon.name} was not the weapon used.")

        # Preguntar sobre habitaciones donde no ocurrió el crimen
        for room in self.rooms:
            response = input(f"Did the crime occur in the {room.name}? (yes/no): ").strip().lower()
            if response == 'no':
                self.knowledge_base.append(lambda murderer, weapon, room_obj, name=room.name: room_obj.name != name)
                self.potential_hints.append(f"The crime did not occur in the {room.name}.")

    def is_kb_true(self, model):
        murderer, weapon, room = model
        return all(rule(murderer, weapon, room) for rule in self.knowledge_base)

    def check_recursive(self, remaining_characters, remaining_weapons, remaining_rooms, current_solution):
        if len(current_solution) == 3:
            if self.is_kb_true(current_solution):
                return [current_solution]
            return []

        solutions = []
        if len(current_solution) < 3:
            if len(current_solution) == 0:  # Agregar un personaje
                for char in remaining_characters:
                    solutions += self.check_recursive(remaining_characters - {char}, remaining_weapons, remaining_rooms, current_solution + (char,))
            elif len(current_solution) == 1:  # Agregar un arma
                for weapon in remaining_weapons:
                    solutions += self.check_recursive(remaining_characters, remaining_weapons - {weapon}, remaining_rooms, current_solution + (weapon,))
            elif len(current_solution) == 2:  # Agregar una habitación
                for room in remaining_rooms:
                    solutions += self.check_recursive(remaining_characters, remaining_weapons, remaining_rooms - {room}, current_solution + (room,))

        return solutions

    def check_all(self):
        remaining_characters = set(self.characters)
        remaining_weapons = set(self.weapons)
        remaining_rooms = set(self.rooms)
        return self.check_recursive(remaining_characters, remaining_weapons, remaining_rooms, ())

    def reveal_solutions(self, solutions):
        print("\nPossible solution based on the knowledge base:")
        for i, solution in enumerate(solutions):
            murderer, weapon, room = solution
            print(f"Solution {i+1}:")
            print(f"  Murderer: {murderer.name}")
            print(f"  Weapon: {weapon.name}")
            print(f"  Room: {room.name}")
        if not solutions:
            print("No valid solutions found.")

    def ask_for_hint(self):
        if self.potential_hints:
            # Escoger una pista aleatoriamente de las pistas posibles
            hint = random.choice(self.potential_hints)
            print(f"Hint: {hint}")
            # Eliminar la pista utilizada
            self.potential_hints.remove(hint)
        else:
            print("No hints available.")

    def play(self):
        print("Welcome to Clue! Try to guess the murderer, weapon, and room.")
        self.setup_game()
        
        while True:
            solutions = self.check_all()
            if solutions:
                self.reveal_solutions(solutions)
            else:
                print("No valid solutions found based on the knowledge base.")

            ask_hint = input("Would you like a hint? (yes/no): ").strip().lower()
            if ask_hint == 'yes':
                self.ask_for_hint()

            play_again = input("Do you want to play again? (yes/no): ").strip().lower()
            if play_again != 'yes':
                break

if __name__ == "__main__":
    game = ClueGame()
    game.play()
