#!/usr/bin/env python3
import sys, os, json
# Check to make sure we are running the correct version of Python
assert sys.version_info >= (3,7), "This script requires at least Python 3.7"

# The game and item description files (in the same folder as this script)
game_file = 'game1.json'
item_file = 'items.json'
inventory = []
items = []


# Load the contents of the files into the game and items dictionaries. You can largely ignore this
# Sorry it's messy, I'm trying to account for any potential craziness with the file location
def load_files():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, game_file)) as json_file: game = json.load(json_file)
    with open(os.path.join(__location__, game_file)) as json_file: items = json.load(json_file)
    return game, items

def check_inventory(items):
    for i in inventory: 
        if i == items:
            return True
    return False


def render(game,items,current):
    c = game[current]
    print("You are at the " + c["name"])
    print(c["desc"])

    for i in inventory:
        if i in items:
            if current in items[i]["exits"]:
                print(items[i]["exits"][current])
                inventory.remove(i)


    print("/snAvailable exits:")
    if "exits" in c:
        for e in c["exits"]:
            print(e["exit"].lower())


def get_input():
    response = input("What do you want to do? ")
    response = response.upper().strip()
    return response

def update(game,items,current,response):
    if response == "INVENTORY":
        print("/nYou are carrying:")
        if len(inventory) == 0:
            print("Nothing")
            return current
        else:
            for i in inventory:
                print(i.lower())
        return current
    c = game[current]
    for e in c["exits"]:
        if response == e["exit"]:
            return e["target"]
    
    c = game[current]
    for e in c["exits"]:
        if response == e["exit"]:
            return e["target"]

    for items in c["items"]:
        if response == "GET " + items["items"] and not check_inventory(items["items"]):
            print()
            print(items["take"])
            inventory.append(items["items"])
            return current
    for i in inventory:
        if i in items:
            for action in items[i]["actions"]:
                if response == action + " " + i:
                    print(items[i]["actions"][action])
                    return current
    if response[0:3] == "GET":
        print("You can't take that!")
    elif response in ["NORTH","SOUTH","EAST","WEST","NW","NE","SW","SE","UP","DOWN"]:
        print("You can't go that way!")
    else:
        print("I don't understand what you're trying to do.")       
    

# The main function for the game
def main():
    current = 'START'  # The starting location
    end_game = ['END']  # Any of the end-game locations

    (game, items) = load_files()

    name = input("What is your name: ")
    name = name.strip()
    if name == "":
        name = "Starkiller"
    print("/nThe republic and the Jedi order has fallen and the empire is taking over. You are one of the last of the Jedi left and the Empire are after you. You crash land in an unfamiliar planet. You need to find a ship and get out.")

    while True:
        render(game,items,current)

        for e in end_game:
            if current == e:
                print("You win!")
                break #break out of the while loop

        response = get_input()

        if response == "QUIT" or response == "Q":
            break #break out of the while loop

        current = update(game,items,current,response)

    print("Thanks for playing!")

# run the main function
if __name__ == '__main__':
	main()