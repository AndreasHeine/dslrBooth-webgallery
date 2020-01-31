'''
Author: Andreas Heine
Version: 0.2.1 "beta"
Datum: 22.01.2020

To Do:
-Check if dslrBooth is running
'''

##############################
#dslrBooth:
##############################

import os, sys, platform, json, time

if os.name != "nt":
    raise OSError("Windows 10 is required!")
if platform.system() != "Windows":
    raise OSError("Windows 10 is required!")
if platform.release() != "10":
    raise OSError("Windows 10 is required!")

app_path = os.path.dirname(os.path.abspath(__file__))
dslrBooth_folder = os.path.join(app_path, "static", "dslrBooth")
config_file = os.path.join(app_path, "config.json")
try:
    with open(file=config_file) as file:
        config = json.load(fp=file)
        username = config["winuser"]
        reverse_all_lists = config["reversed"]
except Exception as e:
    print(e)
    pass

dslrBooth_config_file = r"C:\\Users\\" + username + r"\\AppData\\Roaming\\dslrBooth\\app_settings.json"
try:
    with open(file=dslrBooth_config_file) as file:
        dslrBooth_config = json.load(fp=file)
        projectname = dslrBooth_config["AlbumName"]
    image_folder = os.path.join(dslrBooth_folder, projectname, "Prints")
    thumb_folder = os.path.join(image_folder, "thumb")
except Exception as e:
    image_folder = ""
    thumb_folder = ""
    projectname = ""
    print(e)
    pass

def find_images(path, reverse_flag):
    filelist = os.listdir(path=path)
    foundimages = []
    if filelist:
        for filename in filelist:
            if ".jpg" in filename:
                foundimages.append(filename)
            elif ".JPG" in filename:
                foundimages.append(filename)
            else:
                pass
    if reverse_flag:
        return reversed(foundimages)
    else:
        return foundimages


##############################
# Falsk Web-App:
##############################

try:
    from flask import Flask, escape, request, render_template
except ImportError:
    print("Flask is not installed -> 'python -m pip install flask'")

if __name__ == "__main__":
    ip = "0.0.0.0"
    port = 80
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def index():
        if thumb_folder == "":
            context = {
                "title": "Gallery is empty",
                "imagelist": []
                }
        else:
            imglist = list(zip(find_images(path=image_folder, reverse_flag=reverse_all_lists), find_images(path=thumb_folder, reverse_flag=reverse_all_lists)))
            context = {
                "title": projectname,
                "imagelist": imglist
                }

        return render_template(template_name_or_list='index.html', title='index', context=context)

    app.run(host=ip, port=port, debug=False)