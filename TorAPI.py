import requests
import os
from urllib.parse import unquote
from zipfile import ZipFile, BadZipFile

class GeoIPDownloader:
    def __init__(self):
        self.config_folder = "config"
        self.last_number_file = os.path.join(self.config_folder, "last.txt")
        self.base_url = "https://gitlab.torproject.org/tpo/network-health/metrics/geoip-data/-/package_files/"
        self.max_attempts = 10
        self.extraction_dir = "extracted_files"
        os.makedirs(self.extraction_dir, exist_ok=True)

    def read_last_number(self):
        try:
            with open(self.last_number_file, 'r') as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return None

    def write_last_number(self, number):
        with open(self.last_number_file, 'w') as file:
            file.write(str(number) - 1)

    def download_and_extract(self, url, target_dir=None):
        response = requests.get(url)

        if response.status_code == 200:
            filename = unquote(url.split("/")[-1])
            target_dir = target_dir or self.extraction_dir

            with open(os.path.join(target_dir, filename), "wb") as file:
                file.write(response.content)

            try:
                with ZipFile(os.path.join(target_dir, filename), 'r') as zip_ref:
                    file_list = zip_ref.namelist()
                    valid_filenames = [file_name for file_name in file_list if file_name in {"geoip", "geoip6"}]

                    if valid_filenames:
                        zip_ref.extractall(target_dir, members=valid_filenames)
                        return valid_filenames
            except BadZipFile:
                pass

            os.remove(os.path.join(target_dir, filename))

        return None

    def filter_lines_containing_text(self, file_path, text):
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file.readlines() if text in line]
            with open(file_path, 'w') as file:
                file.write('\n'.join(lines))
        except FileNotFoundError:
            pass

    def run(self, filter_lines=False, filter_text=None):
        last_number = self.read_last_number()

        if last_number is not None:
            highest_valid_number = None

            for i in range(1, self.max_attempts + 1):
                current_url = f"{self.base_url}{last_number + i}/download.zip"
                valid_files = self.download_and_extract(current_url)

                if valid_files:
                    highest_valid_number = last_number + i

            if highest_valid_number is not None:
                final_url = f"{self.base_url}{highest_valid_number}/download.zip"
                self.download_and_extract(final_url, target_dir=self.extraction_dir)
                os.remove(os.path.join(self.extraction_dir, "download.zip"))

                if filter_lines:
                    for file_name in {"geoip", "geoip6"}:
                        file_path = os.path.join(self.extraction_dir, file_name)
                        self.filter_lines_containing_text(file_path, f",{filter_text}")

                self.write_last_number(highest_valid_number)
                print("Bot has completed the run!")
    
    def menu(self):
        print("GeoIP Dumper for Tor Expert Bundle by:  github.com/skhrlx")
        print("Filter Lines? yes or no (lowercase)")
        choice = input("Option selected:  ")
        
        if choice.lower() == "yes":
            country = input("Which country do you want to filter? (Ex: BR, US, CA, PT, CN):  ")
            self.run(filter_lines=True, filter_text=country)
        elif choice.lower() == "no":
            self.run(filter_lines=False, filter_text=None)


geoip_downloader = GeoIPDownloader()
geoip_downloader.menu()
#geoip_downloader.run(filter_lines=True, filter_text="BR")