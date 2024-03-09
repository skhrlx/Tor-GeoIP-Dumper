# TOR GeoIP Updater

This script automates the process of updating the GeoIP data for tor expert bundle. Follow the steps below to ensure you have the latest GeoIP data.

## Instructions:

1. **Update Last Number:**
   - Open the `config` folder.
   - Edit the `last.txt` file and replace the current number with the latest one from the following URL: [GeoIP Package Repository](https://gitlab.torproject.org/tpo/network-health/metrics/geoip-data/-/packages/).
   - Navigate to the latest package and copy the URL link of the file under the page "geoip-[RANDOM NUMBER].jar".
   - Extract the number from the link, e.g., [GeoIP Download Link](https://gitlab.torproject.org/tpo/network-health/metrics/geoip-data/-/package_files/3654/download) means your number is 3654 - 1, so put 3653 in `last.txt` (without spaces or additional characters).

2. **Run the Script:**
   - Execute `main.py` to automatically download and update the GeoIP data.
   - Optionally, you can specify a country by using its flag (e.g., United States = US, Brazil = BR).

3. **Check Output:**
   - The updated GeoIP data will be stored in the `extracted_files` directory.

Now your project is equipped with the latest GeoIP data. Happy coding! 😊
