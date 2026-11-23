# P6 Flight Delay Ranking Audit

Rank flight IDs by descending arrival delay. Equal delays keep their original CSV row order.

## Team and responsibilities

Group A: [add partner full name]. Insertion sort and heapsort. Existing code is in P6_Flight_Delay_Ranking/starter/my_solutions.py.

Group B: Brenda Murillo. Mergesort and counting sort. Code is in Brenda_Group_B/starter/group_b_solutions.py.

Keep this upload alongside the existing Group A project folder in the shared repository. Label the Group A folder with that student’s name and update its paths below if it is renamed.

## Run from the repository root

Use Python 3.10 or later. The algorithm and test code use the standard library. Graph generation in benchmark.py uses matplotlib.

Group B tests:

```bash
python3 Brenda_Group_B/test_group_b.py
```

Group B supplied checker:

```bash
python3 Brenda_Group_B/starter/run_checks.py Brenda_Group_B/starter/group_b_solutions.py --only merge,counting
```

Group B experiments:

```bash
python3 Brenda_Group_B/benchmark.py
```

This runs five timings per case, reports their median and writes fresh results and graphs to Brenda_Group_B/results. CSV loading and validation are outside the timed interval. Memory and operation counts use separate calls. Install matplotlib to regenerate graphs; the measurements also run without it.

Group A supplied checker using the existing folder:

```bash
python3 P6_Flight_Delay_Ranking/starter/run_checks.py P6_Flight_Delay_Ranking/starter/my_solutions.py --only insertion,heap
```

## Submitted documents

Project_Report.docx contains the report, pseudocode, hand examples, test results and graphs. Project_Slides.pptx contains the supplied presentation. One_Page_Recommendation.docx compares all four methods. Complete Cross_Check_Log_To_Complete.docx after each student tests the other student’s code, then rename it Cross_Check_Log.docx.

## Data and checks

Source: course-provided P6_Flight_Delay_Ranking.zip and P6 Project Brief. All seven supplied synthetic CSV files are included. No cleaning was applied to the original inputs. manifest.json contains the reference hashes.

The range experiment clips delays to 0 through 100 or multiplies them by 100 or 1000. It adjusts the counting bounds and recalculates the expected stable order for each transformed input.

Group B passed 14 supplied algorithm/dataset checks. Tests cover empty input, one flight, ties, negative and boundary delays, sorted and reversed inputs, and random seeds 1, 2 and 3. The benchmark verifies the supplied reference hashes.

## Assistance and measurement environment

ChatGPT assisted with Group B code, tests, benchmark execution, graphs, explanations and the shared recommendation. Group B report measurements used Linux x86_64, Python 3.12.14 and an AMD EPYC 9V74 processor. Timings vary by machine. Group A and Group B timings came from different environments and should not be used as a direct four-algorithm speed ranking. Group A should add any other assistance it received.

Before submission, enter the partner’s full name and complete the real partner cross-check entries. Both students should commit their own contributions. Ensure the instructor can access the repository.
