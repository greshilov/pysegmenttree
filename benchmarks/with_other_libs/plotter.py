import collections
import itertools
import json
import statistics

import matplotlib.pyplot as plt
import numpy as np

from benchmarks.with_other_libs.main import (
    DATA_DIR,
    QUERY_COUNT,
    REFRENCE_SIZE,
    RESULT_FILE_NAME,
)


def plot():
    bench_data = json.load(open(RESULT_FILE_NAME))

    graph_titles = {
        "init": f"init",
        "query": f"query",
        "update": f"update",
    }

    for bench_name, results in bench_data.items():
        lib_labels = collections.defaultdict(list)
        bars_count = collections.defaultdict(int)

        for result in results:
            if result["result"]:
                res = statistics.mean(result["result"]) * 1000
                bars_count[result["type"]] += 1
            else:
                res = 0
            lib_labels[result["lib"]].append(res)

        labels = list(bars_count)
        bars = list(bars_count.values())
        x = list(range(len(labels)))

        width = 0.25
        fig, ax = plt.subplots()

        # Complex logic to support different amount of bars
        current_coords = [
            xi - width * (bc - 1) / 2 if bc > 1 else xi for xi, bc in zip(x, bars)
        ]
        for i, (typ, results) in enumerate(lib_labels.items()):
            x_coords = []
            for i, res in enumerate(results):
                x_coords.append(current_coords[i])
                if res > 0 and bars[i] > 1:
                    current_coords[i] += width

            rects = ax.bar(x_coords, results, width, label=typ)
            ax.bar_label(rects, fmt="%.2f", padding=3)

        ax.set_ylabel("Time, ms")
        ax.set_yscale("log")
        ax.set_title(graph_titles.get(bench_name))
        ax.set_xticks(x)
        ax.set_xticklabels(labels)

        # ax.legend(bbox_to_anchor=(1,0), loc="lower left")
        ax.legend()
        ax.margins(0.05, 0.6)

        fig.tight_layout()

        fig.savefig(DATA_DIR / "{}.png".format(bench_name))
        plt.close()


if __name__ == "__main__":
    plot()
