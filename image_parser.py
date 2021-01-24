import cv2
import pytesseract
import re
from difflib import get_close_matches

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def parse_image(img):
    def read_config(config="config.yml"):
        """
        :param file: str
            Name of file to read
        :return: ObjectView
            Parsed config file
        """

    img_data = pytesseract.image_to_string(img)

    img_lines = img_data.splitlines()

    # turn to lower case and remove empty lines
    img_lines = [line.lower() for line in img_lines if line.strip()]

    def find_date():
        date_pattern = r"(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])/\d\d"
        for line in img_lines:
            # print(line)
            match = re.match(date_pattern, line)
            if match:
                return match.group(0)
        return None

    date_str = find_date()

    MARKETS = ["walmart", "costco"]

    # find market_str
    market_str = None
    accuracy = 0.6

    def find_market():
        for market in MARKETS:
            for line in img_lines:
                words = line.split()
                # Get the single best match in line
                matches = get_close_matches(market, words, n=1, cutoff=accuracy)
                if matches:
                    return market
        return None

    market_str = find_market()

    SUM_KEYS = ["total", "sum"]

    # accuracy = 0.6

    sum_pattern = "\d+(\.\s?|,\s?|[^a-zA-Z\d])\d{2}"

    def find_sum():
        for sum_key in SUM_KEYS:
            for line in img_lines:
                words = line.split()
                matches = get_close_matches(sum_key, words, n=1, cutoff=accuracy)
                if matches:
                    # Replace all commas with a dot to make finding and parsing the sum easier
                    line = line.replace(",", ".")
                    # Parse the sum
                    sum_float = re.search(sum_pattern, line)
                    if sum_float:
                        return sum_float.group(0)
        return None

    sum_str = find_sum()

    return (date_str, market_str, sum_str)


# img = cv2.imread('data/walmart2.jpg')
# (date, market, sum) = img_to_json(img)

# print("Date: {}".format(date))
# print("Market: {}".format(market))
# print("Sum: {}".format(sum))

