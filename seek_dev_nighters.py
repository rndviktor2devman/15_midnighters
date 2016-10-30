import requests
from datetime import datetime, time
from pytz import timezone


def load_attempts():
    base_url = "https://devman.org/api/challenges/solution_attempts/"
    users_list = []
    pages = 1
    devman_json = requests.get(base_url, params={'page': pages}).json()
    pages_count = devman_json['number_of_pages']
    users_list.extend(get_user_info(devman_json))
    for page in range(pages + 1, pages_count + 1):
        number = {'page': page}
        page_json = requests.get(base_url, params=number).json()
        users_list.extend(get_user_info(page_json))
    return users_list


def get_midnighters(users):
    night_owls = set()
    for user in users:
        if user['timestamp'] is not None:
            server_zone = timezone("Europe/Moscow")
            server_time = datetime.fromtimestamp(user['timestamp'])
            server_time_localized = server_zone.localize(server_time)
            user_zone = timezone(user['timezone'])
            user_time = server_time_localized.astimezone(user_zone)
            if time(0, 0, 0) < user_time.time() < time(4, 0, 0):
                night_owls.add(user['username'])

    return night_owls


def get_user_info(data):
    users_info = []
    users = data['records']
    for user in users:
        users_info.append({
            'username': user['username'],
            'timestamp': user['timestamp'],
            'timezone': user['timezone']
        })

    return users_info


if __name__ == '__main__':
    users = load_attempts()
    night_owls = get_midnighters(users)
    print("People, who contribute to devman.org between 0:00AM and 4:00AM:")
    for user in night_owls:
        print(user)

