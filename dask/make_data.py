import json
from random import randint, choice


def main():
    for i in range(10000):
        data = dict()
        data['number'] = randint(1, 10)
        data['letter'] = choice(['A', 'B', 'C'])
        with open(f'data/{i}.json', 'w+') as f:
            json.dump(data, f)


if __name__ == '__main__':
    main()
