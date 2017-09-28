from dask import delayed
from dask.diagnostics import ProgressBar
import json
from time import time
import click


def load(filename):
    with open(filename, 'r+') as f:
        return json.load(f)


def sum_by_letter(list_of_dicts, letter):
    """
    :param list_of_dicts: A list of dictionaries.
    :param letter: A value of the letter keyed by 'letter'.
    """
    total = 0
    for d in list_of_dicts:
        if d['letter'] == letter:
            total += d['number']
    return total


def mean(arr):
    return sum(arr) / len(arr)


def run_parallel(n):
    """Program code to run."""
    with ProgressBar():
        filenames = [f'data/{i}.json' for i in range(n)]
        data = [delayed(load)(f) for f in filenames]
        sumA = delayed(sum_by_letter)(data, 'A')
        sumB = delayed(sum_by_letter)(data, 'B')
        sumC = delayed(sum_by_letter)(data, 'C')
        mean_score = mean([sumA, sumB, sumC])
        mean_score = mean_score.compute()

    print(mean_score)


def run_serial(n):
    """Program code to run."""
    data = []
    for i in range(n):
        filename = f'data/{i}.json'
        datum = load(filename)
        data.append(datum)
    sumA = sum_by_letter(data, 'A')
    sumB = sum_by_letter(data, 'B')
    sumC = sum_by_letter(data, 'C')
    mean_score = mean([sumA, sumB, sumC])
    print(mean_score)


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
