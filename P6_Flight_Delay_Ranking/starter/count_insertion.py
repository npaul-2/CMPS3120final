"""Count insertion-sort delay comparisons and shifts on the three 10,000-row files."""

from pathlib import Path

import problem


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATASETS = (
    "flights_n010000_schedule.csv",
    "flights_n010000_nearly_sorted.csv",
    "flights_n010000_reversed.csv",
)


def insertion_counts(inst):
    ordered = []
    comparisons = 0
    shifts = 0

    for flight_id, delay in zip(inst["ids"], inst["delay"]):
        i = len(ordered) - 1
        while i >= 0:
            comparisons += 1
            if ordered[i][1] < delay:
                i -= 1
            else:
                break

        position = i + 1
        shifts += len(ordered) - position
        ordered.insert(position, (flight_id, delay))

    ids = [flight_id for flight_id, _ in ordered]
    return ids, comparisons, shifts


def main():
    print("Insertion sort operation counts")
    print("Shifts count existing records moved, insertions are not included.")
    print(f"{'dataset':38s} {'n':>7s} {'comparisons':>15s} {'shifts':>15s}")

    for filename in DATASETS:
        inst = problem.load_instance(DATA_DIR / filename)
        ids, comparisons, shifts = insertion_counts(inst)

        valid, _, message = problem.validate(inst, ids)
        if not valid:
            raise RuntimeError(f"{filename}: insertion sort returned an invalid order: {message}")

        print(f"{filename:38s} {inst['n']:7d} {comparisons:15,d} {shifts:15,d}")

    n = 10_000
    print("\nTheoretical comparison references for n = 10,000:")
    print(f"  Best case, n - 1:                 {n - 1:,}")
    print(f"  Average case, approximately n^2/4: {n * n // 4:,}")
    #print(f"  Worst case, n(n - 1)/2:           {n * (n - 1) // 2:,}")


if __name__ == "__main__":
    main()
