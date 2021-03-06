import json
import time
from pathlib import Path

import steamspypi


def get_cooldown():
    cooldown = 70  # 1 minute plus a cushion

    return cooldown


def get_some_sleep():
    cooldown = get_cooldown()
    print("Sleeping for {} seconds on {}".format(cooldown, time.asctime()))

    time.sleep(cooldown)

    return


def download_a_single_page(page_no=0):
    print("Downloading page={} on {}".format(page_no, time.asctime()))

    data_request = dict()
    data_request['request'] = 'tag'
    data_request['tag'] = 'visual+novel'
    data = steamspypi.download(data_request)

    return data



def get_file_name(page_no):
    # Get current day as yyyymmdd format
    date_format = "%Y%m%d"
    current_date = time.strftime(date_format)

    file_name = "{}_steamspy_page_tag_Vn{}.json".format(current_date, page_no)

    return file_name


def download_all_pages(num_pages):
    # Download

    for page_no in range(num_pages):
        file_name = get_file_name(page_no)

        if not Path(file_name).is_file():
            page_data = download_a_single_page(page_no=page_no)

            with open(file_name, "w", encoding="utf8") as f:
                json.dump(page_data, f)

            if page_no != (num_pages - 1):
                get_some_sleep()

    # Aggregate

    data = dict()

    for page_no in range(num_pages):
        file_name = get_file_name(page_no)

        with open(file_name, "r", encoding="utf8") as f:
            page_data = json.load(f)

            data.update(page_data)

    return data


if __name__ == "__main__":
    # TODO: one would have to figure out the number of pages, it should be close to 40 as of August 2020.
    data = download_all_pages(num_pages=54)