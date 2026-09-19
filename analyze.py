import json
import sys

import numpy as np


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <path_to_json_file>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        data: dict = json.load(f)

    # print(f"keys of data: {list(data)}")
    # for k, v in data.items():
    #     if type(v) == list:
    #         print("{}: [a list]".format(k))
    #     else:
    #         print("{}: {}".format(k, v))

    print("--- Pre-computed ---")
    print("p50_ttft_ms: {:.2f} ms".format(data["median_ttft_ms"]))
    print("p99_ttft_ms: {:.2f} ms".format(data["p99_ttft_ms"]))
    print("p50_tpot_ms: {:.2f} ms".format(data["median_tpot_ms"]))
    print("p99_tpot_ms: {:.2f} ms".format(data["p99_tpot_ms"]))
    print("p50_itl_ms: {:.2f} ms".format(data["median_itl_ms"]))
    print("p99_itl_ms: {:.2f} ms".format(data["p99_itl_ms"]))


    print("\n--- From raw data ---")
    ttft: np.ndarray = np.asarray(data["ttfts"])
    ttft_p50, ttft_p99 = np.percentile(ttft, [50, 99])
    print("p50_ttft_ms: {:.2f} ms".format(1000 * ttft_p50))
    print("p99_ttft_ms: {:.2f} ms".format(1000 * ttft_p99))

    # tpot: np.ndarray = np.asarray(data["tpots"])
    # tpot_p50, tpot_p99 = np.nanpercentile(tpot, [50, 99])
    # print("p50_tpot_ms: {:.2f} ms".format(1000 * tpot_p50))
    # print("p99_tpot_ms: {:.2f} ms".format(1000 * tpot_p99))

    itl: np.ndarray = np.concatenate(data["itls"])
    itl_p50, itl_p99 = np.nanpercentile(itl, [50, 99])
    print("p50_itl_ms: {:.2f} ms".format(1000 * itl_p50))
    print("p99_itl_ms: {:.2f} ms".format(1000 * itl_p99))

if __name__ == "__main__":
    main()

