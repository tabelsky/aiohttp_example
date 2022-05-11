import requests
import time

URL = 'https://swapi.tech/api/people/'

MAX = 10

def get_person(person_id):
    return requests.get(f'{URL}{person_id}').json()


def main():
    for person_id in range(1, MAX+1):
        print(get_person(person_id))

start = time.time()
main()
print(time.time() - start)