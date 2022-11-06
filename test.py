import os.path
from time import sleep
from datetime import datetime
import speedtest
from tqdm import tqdm
import pickle
import sys

SLEEP = int(sys.argv[1])  # Seconds between tests
RUNS = int(sys.argv[2])  # How many times to run the test (-1 for infinite)


def load_history() -> list:
    """Load the results from the pickle file or return an empty list."""

    return pickle.load(open('results.pkl', 'rb')) if os.path.isfile('results.pkl') else []


def bit_to_MB(bit: float) -> float:
    """Convert bits to megabytes."""

    return bit / 8 / 1024 / 1024


def test(bar: tqdm) -> dict:
    """Run a speedtest and return the results."""

    bar.set_description(f"{datetime.now()} | Running speedtest")
    bar.set_description('Creating speedtest object')
    client = speedtest.Speedtest()

    bar.set_description('Searching for the best server')
    client.get_servers()
    client.get_best_server()

    bar.set_description('Testing download speed')
    client.download()

    bar.set_description('Testing upload speed')
    client.upload()

    bar.set_description('Test complete')

    results_dict = client.results.dict()

    download = bit_to_MB(results_dict['download'])
    upload = bit_to_MB(results_dict['upload'])

    return {'download': download, 'upload': upload, 'ping': results_dict['ping']}


def run_tests(runs: int, sleep_seconds: int) -> list:
    """Run the speedtest runs times. If runs is -1, do infinite speedtests."""

    results = load_history()

    with tqdm(total=runs) as bar:
        bar.set_description(f"{datetime.now()} | Starting speedtests")
        while runs != 0:
            try:
                result = test(bar)
            except:
                bar.set_description(f"{datetime.now()} | Error running speedtest")
                sleep(5)
                continue
            result['time'] = datetime.now()

            results.append(result)
            pickle.dump(results, open('results.pkl', 'wb'))

            bar.update()
            runs -= 1

            bar.set_description(f"{datetime.now()} | Sleeping for {SLEEP} seconds")
            sleep(sleep_seconds)
        bar.set_description(f"{datetime.now()} | Done")

    return results


bar = tqdm(total=RUNS)

results = run_tests(RUNS, SLEEP)

import plot
