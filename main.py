import requests
import os
from git import Repo

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
                print(file_data)
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

def update_directory_with_github_url(local_path, github_url):
    # Files and folders to exclude from deletion
    exclude_folders = ['.upm', '.pythonlibs']
    exclude_files = ['.replit', 'pyproject.toml', 'poetry.lock']

    # Delete everything except files and folders in the exclusion list
    for root, dirs, files in os.walk(local_path, topdown=False):
        for file in files:
            if file not in exclude_files:
                os.remove(os.path.join(root, file))
        for dir in dirs:
            if dir not in exclude_folders:
                os.rmdir(os.path.join(root, dir))

    # Clone the GitHub repository into the local directory
    Repo.clone_from(github_url, local_path)

    print("Update completed successfully!")

url_to_check = "https://raw.githubusercontent.com/syrabrox/Test-Updater/main/version.txt"
file_path_to_check = "version.txt"
checker = needToUpdate(url_to_check, file_path_to_check)
downloadUrl = "https://github.com/syrabrox/Test-Updater.git"
if checker:
  # update!
  print(checker)
  update(os.getcwd(), downloadUrl)
else:
  print(checker)
