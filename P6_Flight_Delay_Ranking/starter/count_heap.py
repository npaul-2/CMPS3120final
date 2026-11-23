"""Count heapsort moves and writes on the three 10,000-row files."""

from pathlib import Path

import problem


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATASETS = (
    "flights_n010000_schedule.csv",
    "flights_n010000_nearly_sorted.csv",
    "flights_n010000_reversed.csv",
)


def heap_counts(inst):
    items = [
        (-delay, position, flight_id)
        for position, (flight_id, delay) in enumerate(zip(inst["ids"], inst["delay"]))
    ]
    n = len(items)
    swaps = 0

    def sift_down(root, heap_size):
        nonlocal swaps
        while 2 * root + 1 < heap_size:
            child = 2 * root + 1
            if child + 1 < heap_size and items[child] < items[child + 1]:
                child += 1
            if items[root] >= items[child]:
                break
            items[root], items[child] = items[child], items[root]
            swaps += 1
            root = child

    for start in range(n // 2 - 1, -1, -1):
        sift_down(start, n)

    for end in range(n - 1, 0, -1):
        items[end], items[0] = items[0], items[end]
        swaps += 1
        sift_down(0, end)

    ids = [flight_id for _, _, flight_id in items]
    valid, _, message = problem.validate(inst, ids)
    if not valid:
        raise RuntimeError(f"heapsort returned an invalid order: {message}")

    heap_initial_writes = n
    heap_swap_writes = 2 * swaps
    output_writes = n
    return {
        "swaps": swaps,
        "traditional_swap_moves": 3 * swaps,
        "heap_writes": heap_initial_writes + heap_swap_writes,
        "output_writes": output_writes,
        "total_writes": heap_initial_writes + heap_swap_writes + output_writes,
    }


def main():
    print("Heapsort move/write counts")
    print("A swap is 3 traditional moves or 2 heap-array writes.")
    print("Total writes include n heap placements and n returned-ID writes.")
    print(
        f"{'dataset':38s} {'n':>7s} {'swaps':>12s} {'swap moves':>14s} "
        f"{'heap writes':>14s} {'output writes':>15s} {'total writes':>14s}"
    )

    for filename in DATASETS:
        inst = problem.load_instance(DATA_DIR / filename)
        counts = heap_counts(inst)
        print(
            f"{filename:38s} {inst['n']:7d} {counts['swaps']:12,d} "
            f"{counts['traditional_swap_moves']:14,d} {counts['heap_writes']:14,d} "
            f"{counts['output_writes']:15,d} {counts['total_writes']:14,d}"
        )


if __name__ == "__main__":
    main()
