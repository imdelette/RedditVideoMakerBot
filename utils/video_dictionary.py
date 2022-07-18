import json
from os import path

JSON_PATH = 'assets/json/background_options.json'
COMMANDS = ["add", "update", "remove"]


def console():
    print("You load a function to edit a dictionary of videos.\n"
          "Want you like to add, update or remove video?")
    command = input()
    while command not in COMMANDS:
        command = input("Invalid command!\n")
    else:
        match command:
            case "add":
                add()
            case "update":
                update()
            case "remove":
                remove()


def json_loader():
    obj = {}
    if path.isfile(JSON_PATH) is False:
        raise Exception("File not found")
    with open(JSON_PATH) as fp:
        obj = json.load(fp)
    return obj


def add():
    json_file = json_loader()
    url = input("Input an url of your video:\n")
    filename = input("Input a filename (without extension):\n")
    creator = input("Input a name of creator:\n")
    position = input("Input a position (x, y):\n").split()

    json_file[filename] = {
        "url": url,
        "filename": filename + ".mp4",
        "creator": creator,
        "position": position
    }

    with open(JSON_PATH, 'w') as f:
        json.dump(json_file, f,
                  indent=4,
                  separators=(',', ': '))

    print('Successfully appended to the JSON file')


console()