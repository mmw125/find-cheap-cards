import json
import urllib.request
import os.path

database_folder = os.path.join(__path__, "../database")

def _get_or_download_file(filename: str):
    if os.path.exists(filename):
        return
    url = "http://mtgjson.com/api/v5/" + filename
    print("downloading " + filename + " from " + url)
    urllib.request.urlretrieve(url, filename)
    print("done downloading")


class Database:
    def __init__(self):
        self.all_printings = None

    def init(self):
        for file in ["AllPrintings.json"]:
            _get_or_download_file(file)
            print("loading " + file)
            with open(file) as f:
                self.all_printings = json.load(f)
                print("done loading " + file)

if __name__ == "__main__":
    Database().init()
