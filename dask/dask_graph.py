from dask import delayed
from dask.diagnostics import ProgressBar
import json
from time import time


def load(filename):
    with open(filename, 'r+') as f:
        return json.load(f);


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


def main_parallel():
    """Program code to run."""
    with ProgressBar():
        filenames = [f'data/{i}.json' for i in range(10000)]
        data = [delayed(load)(f) for f in filenames]
        sumA = delayed(sum_by_letter)(data, 'A')
        sumB = delayed(sum_by_letter)(data, 'B')
        sumC = delayed(sum_by_letter)(data, 'C')
        mean_score = mean([sumA, sumB, sumC])
        mean_score = mean_score.compute()

    print(mean_score)


def main_serial():
    """Program code to run."""
    filenames = [f'data/{i}.json' for i in range(10000)]
    data = [load(f) for f in filenames]
    sumA = sum_by_letter(data, 'A')
    sumB = sum_by_letter(data, 'B')
    sumC = sum_by_letter(data, 'C')
    mean_score = mean([sumA, sumB, sumC])
    print(mean_score)


if __name__ == '__main__':
    start = time()
    main_parallel()
    end = time()
    print(f'Parallel time: {end - start}')

    start = time()
    main_serial()
    end = time()
    print(f'Serial time: {end - start}')
