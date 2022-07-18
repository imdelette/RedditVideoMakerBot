import json
from os import path

JSON_PATH = 'assets/json/background_options.json'
COMMANDS = ["add", "update", "remove"]


def console():
    print("You load a script file to edit a dictionary of videos.\n"
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
    position = input("Input a position (e.g. '10, 10'):\n").split(", ")

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


def update():
    json_file = json_loader()
    filename = input("Input a filename that you want to remove (without extension):\n")
    options = input("Input options that you want to change (url, filename, creator, position):\n").split(", ")

    for option in options:
        match option:
            case "url":
                new_url = input("Input new url:\n")
                json_file[filename]["url"] = new_url
            case "filename":
                new_filename = input("Input new filename:\n")
                json_file[new_filename] = json_file.pop(filename)
                json_file[new_filename]["filename"] = new_filename
            case "creator":
                new_creator = input("Input new creator:\n")
                json_file[filename]["creator"] = new_creator
            case "position":
                new_position = input("Input new position:\n")
                json_file[filename]["position"] = new_position

    with open(JSON_PATH, 'w') as f:
        json.dump(json_file, f,
                  indent=4,
                  separators=(',', ': '))
    print('Successfully updated the object of JSON file')


def remove():
    json_file = json_loader()
    filename = input("Input a filename that you want to remove (without extension):\n")
    del json_file[filename]

    with open(JSON_PATH, 'w') as f:
        json.dump(json_file, f,
                  indent=4,
                  separators=(',', ': '))
    print('Successfully removed the object from the JSON file')


console()