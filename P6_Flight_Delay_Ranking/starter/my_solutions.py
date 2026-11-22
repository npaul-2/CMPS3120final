"""
my_solutions.py - starter file for Project P6: Flight Delay Ranking (sorting at scale)

Implement the TWO techniques assigned to you (the keys are listed in TECHNIQUES below). Delete or ignore the others.
Every function receives the loaded instance (a dict; its fields are described at the top of problem.py)
and must return: a list of flight ids, worst delay first (equal delays keep file order).

Test your work from this folder:
    python run_checks.py my_solutions.py --only <key>[,<key>]      e.g.  --only insertion,merge
Rules: write the algorithms under study yourself (see the project brief for which library helpers are allowed).
"""

def solve_insertion(inst):
    """Decrease-and-conquer (insertion sort).

    Return: a list of flight ids, worst delay first (equal delays keep file order).
    """
    #raise NotImplementedError("write the insertion technique here")

    ordered = []
    for flight_id, delay in zip(inst["ids"], inst["delay"]):
        i = len(ordered) - 1
        while i >= 0 and ordered[i][1] < delay:
            i -= 1
        ordered.insert(i + 1, (flight_id, delay))
    return [flight_id for flight_id, _ in ordered]


def solve_merge(inst):
    """Divide-and-conquer (mergesort).

    Return: a list of flight ids, worst delay first (equal delays keep file order).
    """
    raise NotImplementedError("write the merge technique here")


def solve_heap(inst):
    """Transform-and-conquer (heapsort).

    Return: a list of flight ids, worst delay first (equal delays keep file order).
    """
    raise NotImplementedError("write the heap technique here")


def solve_counting(inst):
    """Space-time trade-off (counting sort).

    Return: a list of flight ids, worst delay first (equal delays keep file order).
    """
    raise NotImplementedError("write the counting technique here")


TECHNIQUES = {
    "insertion": solve_insertion,
    "merge": solve_merge,
    "heap": solve_heap,
    "counting": solve_counting,
}
