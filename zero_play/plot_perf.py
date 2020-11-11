from collections import defaultdict
from csv import DictReader
from pathlib import Path

from matplotlib import pyplot as plt


def main():
    times = defaultdict(list)  # {(iters, procs): [time]}
    data_path = Path(__file__).parent.parent / "docs" / "journal" / "2020"
    with (data_path / "multiprocessing_times.csv").open() as result_file:
        for row in DictReader(result_file):
            iters = int(row['iters'])
            procs = int(row['procs'])
            time = float(row['time'])
            times[(iters, procs)].append(time)
    proc_times = defaultdict(list)  # { procs: [time] }
    proc_iters = defaultdict(list)  # { procs: [iters] }
    for (iters, procs), times_list in times.items():
        time = sum(times_list) / len(times_list)
        proc_times[procs].append(time)
        proc_iters[procs].append(iters)

    for procs, times_list in proc_times.items():
        iters_list = proc_iters[procs]
        label = f'{procs} CPU'
        if procs > 1:
            label += 's'
        plt.plot(iters_list, times_list, label=label)

    plt.legend()
    plt.xlabel('Search iterations')
    plt.ylabel('Average think time (s)')
    plt.title('Performance Improvement by Multiprocessing')
    plt.tight_layout()
    plt.show()


main()
