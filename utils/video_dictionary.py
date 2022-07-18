import json
from os import path

JSON_PATH = 'assets/json/background_options.json'


def console():
    print("You load a script file to edit a dictionary of videos.\n"
          "-\nURL: link of the youtube video,\n"
          "FILENAME: name of the video,\n"
          "CREATOR: owner of the video,\n"
          "POSITION: position of image clips in the background\n-")
    command = input("Want you like to add, update or remove video?\n")
    while not is_valid_command(command):
        command = input("Invalid input! Try again.\n")
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


def json_rewriter(json_file):
    with open(JSON_PATH, 'w') as f:
        json.dump(json_file, f,
                indent=4,
                separators=(',', ': '))


def add():
    json_file = json_loader()
    uri = input("Input an URI of your video:\n")
    filename = input("Input a filename (without extension):\n")
    creator = input("Input a name of creator:\n")
    position = input("Input a position (e.g. '10, 10'):\n").split()

    json_file[filename] = {
        "uri": uri,
        "filename": filename + ".mp4",
        "creator": creator,
        "position": position
    }

    json_rewriter(json_file)
    print(f'Successfully added the \'{filename}\'')


def update():
    json_file = json_loader()
    filename = input("Input a filename that you want to update (without extension):\n")

    while not is_existing_filename(filename):
        filename = input("Invalid input! Try again.\n")
    else:
        options = input("Input options that you want to change (uri, filename, creator or position):\n").split()
        while not is_valid_options(options):
            options = input("Invalid input! Try again.\n").split()
        else:
            for option in options:
                match option:
                    case "uri":
                        new_uri = input("Input new uri:\n")
                        json_file[filename]["uri"] = new_uri
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

    json_rewriter(json_file)
    print(f'Successfully updated the \'{filename}\'.')


def remove():
    json_file = json_loader()
    filename = input("Input a filename that you want to remove (without extension):\n")
    del json_file[filename]

    json_rewriter(json_file)
    print(f'Successfully removed the \'{filename}\'.')


def is_valid_command(command):
    return command in ["add", "update", "remove"]


def is_valid_uri(uri):
    return True


def is_existing_filename(filename):
    return filename in json_loader()

def is_valid_filename(filename):
    return True

def is_valid_options(options):
    for option in options:
        if option not in ["uri", "filename", "creator", "position"]:
            print(f"\'{option}\' is invalid option!")
            return False
    return True

def is_valid_position(position):
    return True

console()