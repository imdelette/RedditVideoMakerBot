import json
import requests
from os import path

# TODO: use 'rich' library
# TODO: output list of existence elements in the JSON file
# TODO: remake a position setting


JSON_PATH = 'json/background_options.json'
YT_LINK = "https://youtu.be/"


def console():
    print("You run a script that edit a dictionary of videos.\n"
          "-\nURL: link of the youtube video,\n"
          "FILENAME: name of the video,\n"
          "CREATOR: owner of the video,\n"
          "POSITION: position of image clips in the background.\n-")
    command = input("Want you like to add, update or remove a video? (write \'no\', if you don't want)\n")

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
            case "no":
                return


def json_loader():
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


def json_parser():
    json_file = json_loader()
    background_options = {}
    for obj in json_file:
        if json_file[obj]["position"][1].isnumeric():
            x = json_file[obj]["position"][0]
            y = int(json_file[obj]["position"][1])
            pos = lambda t: (x, y + t)
        else:
            pos = (json_file[obj]["position"][0], json_file[obj]["position"][1])

        background_options[obj] = (
            json_file[obj]["uri"],
            json_file[obj]["filename"],
            json_file[obj]["owner"],
            pos,
        )
    return background_options


def add():
    json_file = json_loader()

    video_code = input("Input a code of your video (\'https://youtu.be/<video_code>\'):\n")
    while not is_valid_uri(video_code):
        video_code = input(f"\'{video_code}\' is invalid! Try again.\n")
    else:
        uri = YT_LINK + video_code
        owner = get_video_owner(uri)

    filename = input("Input a name (without extension):\n")
    while is_existing_filename(filename):
        filename = input(f"\'{filename}\' already exists! Try again.\n")

    x_position = input("Input an X position (or \'center\', \'top\', \'bottom\'):\n")
    while not is_valid_position(x_position):
        x_position = input(f"\'{x_position}\' is invalid! Try again.\n")
    json_file[filename] = {
        "uri": uri,
        "filename": filename + ".mp4",
        "owner": owner,
        "position": ["center", x_position]
    }
    json_rewriter(json_file)

    print(f'Successfully added the \'{filename}\' to the JSON file.')


def update():
    json_file = json_loader()
    filename = input("Input a filename that you want to update (without extension):\n")

    while not is_existing_filename(filename):
        filename = input(f"\'{filename}\' doesn't exist! Try again.\n")
    else:
        options = input("Input an option/options that you want to change (uri, filename, creator or position):\n").split()
        while not is_valid_options(options):
            options = input("Invalid input! Try again.\n").split()
        else:
            for option in options:
                match option:
                    case "uri":
                        new_video_code = input("Input new code of your video (\'https://youtu.be/<video_code>\'):\n")
                        json_file[filename]["uri"] = YT_LINK + new_video_code
                        json_file[filename]["owner"] = get_video_owner(YT_LINK + new_video_code)
                    case "filename":
                        new_filename = input("Input new name:\n")
                        while is_existing_filename(new_filename):
                            new_filename = input(f"\'{filename}\' already exists! Try again:\n")
                        else:
                            json_file[new_filename] = json_file.pop(filename)
                            json_file[new_filename]["filename"] = new_filename
                    case "position":
                        new_x_position = input("Input new position:\n")
                        json_file[filename]["position"][1] = new_x_position
    json_rewriter(json_file)
    print(f'Successfully updated the \'{filename}\' in the JSON file.')


def remove():
    json_file = json_loader()
    filename = input("Input a filename that you want to remove (without extension):\n")
    del json_file[filename]
    json_rewriter(json_file)
    print(f'Successfully removed the \'{filename}\'.')


def get_video_owner(uri):
    response = requests.get("https://noembed.com/embed?url=" + uri)
    obj = response.json()
    return obj["author_name"]


def is_valid_command(command):
    return command in ["add", "update", "remove", "no"]


def is_valid_uri(video_code):
    response = requests.get(YT_LINK + video_code)
    if response.status_code == 200 and is_valid_owner(YT_LINK + video_code):
        return True

    return False


def is_existing_filename(filename):
    return filename in json_loader()


def is_valid_owner(uri):
    try:
        get_video_owner(uri)
        return True
    except KeyError:
        print("Invalid author of video!")
        return False


def is_valid_position(position):
    if position.isnumeric() or position in ["center", "top", "bottom"]:
        return True
    return False


def is_valid_options(options):
    for option in options:
        if option not in ["uri", "filename", "owner", "position"]:
            print(f"\'{option}\' is invalid option!")
            return False
    return True


console()