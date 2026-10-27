import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <path_to_result_folder>")
        sys.exit(1)

    tags = ["tp1", "tp2", "tp4", "probe"]
    folder = Path(sys.argv[1])
    files: dict = {}
    
    for tag in tags:
        files.update({tag: list(folder.rglob("*{}*.json".format(tag)))})
        if not tag in files:
            print("File '*-{}-*' not found in {}\n".format(tag, folder))
            continue

    fig_ttft, ax_ttft = plt.subplots()
    fig_tpot, ax_tpot = plt.subplots()
    fig_itl, ax_itl = plt.subplots()
    
    for tag, file in files.items():
        print("----- {} -----".format(tag))

        with open(file[0]) as f: # Only care about first file
            data: dict = json.load(f)
            
        analyze(data, tag, ax_ttft, ax_tpot, ax_itl)
        print()
        
    ax_ttft.set_title("TTFT distribution")
    fig_ttft.savefig("./imgs/ttft.png", dpi=300)
    
    ax_tpot.set_title("TPOT distribution")
    fig_tpot.savefig("./imgs/tpot.png", dpi=300)

    ax_itl.set_title("ITL distribution")
    fig_itl.savefig("./imgs/itl.png", dpi=300)


def analyze(data, tag, ax_ttft, ax_tpot, ax_itl):
    ttft: np.ndarray = np.asarray(data["ttfts"])
    tpot: np.ndarray = np.array([np.mean(arr[1:]) for arr in data["itls"]])
    itl: np.ndarray = np.concatenate(data["itls"])

    print_info(data, ttft, tpot, itl)
    plot(ttft, "ttft", tag, ax_ttft)
    plot(tpot, "tpot", tag, ax_tpot)
    plot(itl, "itl", tag, ax_itl)
    
    
def print_info(data, ttft, tpot, itl):
    # print(f"keys of data: {list(data)}")
    # for k, v in data.items():
    #     if type(v) == list:
    #         print("{}: [a huge list]".format(k))
    #     else:
    #         print("{}: {}".format(k, v))
    
    print("Pre-computed:")
    print("p50_ttft_ms: {:.2f} ms".format(data["median_ttft_ms"]))
    print("p99_ttft_ms: {:.2f} ms".format(data["p99_ttft_ms"]))
    print("p50_tpot_ms: {:.2f} ms".format(data["median_tpot_ms"]))
    print("p99_tpot_ms: {:.2f} ms".format(data["p99_tpot_ms"]))
    print("p50_itl_ms: {:.2f} ms".format(data["median_itl_ms"]))
    print("p99_itl_ms: {:.2f} ms".format(data["p99_itl_ms"]))
    
    print("From raw data:")
    
    ttft_p50, ttft_p99 = np.nanpercentile(ttft, [50, 99])
    print("p50_ttft_ms: {:.2f} ms".format(1000 * ttft_p50))
    print("p99_ttft_ms: {:.2f} ms".format(1000 * ttft_p99))
    
    tpot_p50, tpot_p99 = np.nanpercentile(tpot, [50, 99])
    print("p50_tpot_ms: {:.2f} ms".format(1000 * tpot_p50))
    print("p99_tpot_ms: {:.2f} ms".format(1000 * tpot_p99))
    
    itl_p50, itl_p99 = np.nanpercentile(itl, [50, 99])
    print("p50_itl_ms: {:.2f} ms".format(1000 * itl_p50))
    print("p99_itl_ms: {:.2f} ms".format(1000 * itl_p99))


def plot(y, label, tag, ax):
    x = range(len(y))

    ax.plot(x, 1000 * np.sort(y), label=tag)

    ax.set_xlabel("prompt index")
    ax.set_ylabel("{} (ms)".format(label))
    ax.legend()
    
    seperate_plot(y, label, tag)


def seperate_plot(y, label, tag):
    x = range(len(y))
    
    fig, ax = plt.subplots()
    ax.plot(x, 1000 * y, label="unsorted")
    ax.plot(x, 1000 * np.sort(y), label="sorted")

    ax.set_xlabel("prompt index")
    ax.set_ylabel("{} (ms)".format(label))
    ax.legend()

    ax.set_title("{} distribution".format(label))
    fig.savefig("./imgs/{}_{}.png".format(tag, label), dpi=300)
    
    
if __name__ == "__main__":
    main()

