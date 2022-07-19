import json
import requests
from os import path


# TODO: use 'rich' library
# TODO: parser for a name of creator
# TODO: output list of existence elements in the JSON file

JSON_PATH = 'json/background_options.json'
YT_LINK = "https://youtu.be/"


def console():
    print("You run a script that edit a dictionary of videos.\n"
          "-\nURL: link of the youtube video,\n"
          "FILENAME: name of the video,\n"
          "CREATOR: owner of the video,\n"
          "POSITION: position of image clips in the background.\n-")
    command = input("Want you like to add, update or remove a video?\n")

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

    video_code = input("Input a code of your video (\'https://youtu.be/<video_code>\'):\n")
    while not is_valid_uri(video_code):
        video_code = input(f"\'{video_code}\' is invalid! Try again.\n")
    else:
        uri = YT_LINK + video_code
        owner = get_video_owner(uri)

    filename = input("Input a name (without extension):\n")
    while not is_valid_filename(filename):
        name = input(f"\'{filename}\' is invalid! Try again.\n")

    position = input("Input a position (split by space, e. g. '10 10'):\n").split()
    while not is_valid_position(position):
        position = input(f"\'{position}\' is invalid! Try again.\n").split()

    json_file[filename] = {
        "uri": uri,
        "filename": filename + ".mp4",
        "owner": owner,
        "position": position
    }

    json_rewriter(json_file)
    print(f'Successfully added the \'{filename}\' to the JSON file.')


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
                        new_video_code = input("Input new code of your video (\'https://youtu.be/<video_code>\'):\n")
                        json_file[filename]["uri"] = YT_LINK + new_video_code
                        json_file[filename]["owner"] = get_video_owner(YT_LINK + new_video_code)
                    case "filename":
                        new_filename = input("Input new name:\n")
                        while not is_valid_filename(new_filename):
                            new_filename = input("Input new filename:\n")
                        else:
                            json_file[new_filename] = json_file.pop(filename)
                            json_file[new_filename]["filename"] = new_filename
                    case "position":
                        new_position = input("Input new position:\n")
                        json_file[filename]["position"] = new_position

    json_rewriter(json_file)
    print(f'Successfully updated the \'{filename}\' in the JSON file.')


def remove():
    json_file = json_loader()
    filename = input("Input a filename that you want to remove (without extension):\n")
    del json_file[filename]

    json_rewriter(json_file)
    print(f'Successfully removed the \'{filename}\'.')


def is_valid_command(command):
    return command in ["add", "update", "remove"]


# this doesn't work the way I would like
def is_valid_uri(video_code):
    response = requests.get(YT_LINK + video_code)
    if response.status_code == 200:
        return True
    else:
        print(f"\'{video_code}\' is invalid!")
        return False


def is_existing_filename(filename):
    return filename in json_loader()


def is_valid_filename(filename):
    return True


def get_video_owner(uri):
    response = requests.get("https://noembed.com/embed?url=" + uri)
    obj = response.json()
    return obj["author_name"]


def is_valid_options(options):
    for option in options:
        if option not in ["uri", "filename", "owner", "position"]:
            print(f"\'{option}\' is invalid option!")
            return False
    return True


def is_valid_position(position):
    return True


console()