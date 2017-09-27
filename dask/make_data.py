import json
from random import randint, choice
from dicttoxml import dicttoxml
from tqdm import tqdm
from dask import delayed
from dask.diagnostics import ProgressBar
from time import time

def make_data(i):
    data = dict()
    data['number'] = randint(1, 10)
    data['letter'] = choice(['A', 'B', 'C'])
    if data['letter'] == 'A':
        data['symbol'] = dict()
        data['symbol']['AAPL'] = randint(10, 20)
    if data['letter'] == 'B':
        data['transaction'] = dict()
        data['transaction']['amount'] = randint(10, 100)
    if data['letter'] == 'C':
        data['identifier'] = dict()
        data['identifier']['amount'] = randint(33, 44)
    return data


def write_json(data, i):
    with open(f'data/{i}.json', 'w+') as f:
        json.dump(data, f)
    return None


def write_xml(data, i):
    with open(f'data/{i}.xml', 'w+') as f:
        f.write(str(dicttoxml(data)))
    return None


def main_serial():
    for i in tqdm(range(10000)):
        data = make_data(i)
        write_json(data, i)
        write_xml(data, i)


def main_parallel():
    # data = [delayed(make_data)(i) for i in range(10000)]
    with ProgressBar():
        things = []
        for i in range(10000):
            data = delayed(make_data)(i)
            j = delayed(write_json)(data, i)
            x = delayed(write_xml)(data, i)
            things.append(j)
            things.append(x)
        counts = delayed(len)(things)
        counts.compute()


if __name__ == '__main__':
    start = time()
    main_serial()
    end = time()
    print(f'Serial time: {end - start}')

    start = time()
    main_parallel()
    end = time()
    print(f'Parallel time: {end - start}')
