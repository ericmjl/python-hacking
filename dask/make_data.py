import json
from random import randint, choice
from dicttoxml import dicttoxml
from tqdm import tqdm
from dask import delayed
from dask.diagnostics import ProgressBar
from time import time
import click
import os


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


def run_serial(n):
    n = int(n)
    for i in tqdm(range(n)):
        data = make_data(i)
        write_json(data, i)
        write_xml(data, i)


def run_parallel(n):
    # data = [delayed(make_data)(i) for i in range(10000)]
    n = int(n)
    with ProgressBar():
        things = []
        for i in range(n):
            data = delayed(make_data)(i)
            j = delayed(write_json)(data, i)
            x = delayed(write_xml)(data, i)
            things.append(j)
            things.append(x)
        counts = delayed(len)(things)
        counts.compute()


@click.command()
@click.option('--parallel/--serial', default=True)
@click.option('--n', default=1000)
def main(parallel=True, n=1000):
    start = time()
    if parallel:
        run_parallel(n)
        end = time()
        print(f'Parallel time: {end - start}')
    else:
        run_serial(n)
        end = time()
        print(f'Serial time: {end - start}')


if __name__ == '__main__':
    main()
