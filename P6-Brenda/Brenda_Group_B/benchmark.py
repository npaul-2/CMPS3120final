"""Run from any directory: python benchmark.py. Writes measured evidence to results/."""
import csv
import gc
import hashlib
import json
import os
import platform
import random
import statistics
import sys
import time
import tracemalloc
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'starter'))
import problem
from group_b_solutions import solve_merge, solve_counting


def instance(delays):
    return {'n': len(delays), 'ids': ['F'+str(i) for i in range(len(delays))], 'delay': delays}


def reference(inst):
    # Reference check only.
    return [inst['ids'][i] for i in sorted(range(inst['n']), key=lambda i: -inst['delay'][i])]


def measure(name, inst, **bounds):
    expected = reference(inst)
    output = []
    for method, solver in [('merge', solve_merge), ('counting', solve_counting)]:
        kwargs = bounds if method == 'counting' else {}
        assert solver(inst, **kwargs) == expected  # Warm up.
        times = []
        for _ in range(5):
            gc.collect()
            start = time.perf_counter()
            sol = solver(inst, **kwargs)
            elapsed = time.perf_counter()-start
            assert sol == expected
            times.append(elapsed)
            del sol
        gc.collect()
        tracemalloc.start()
        sol = solver(inst, **kwargs)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        assert sol == expected
        del sol
        stats = {}
        assert solver(inst, stats=stats, **kwargs) == expected
        output.append(dict(dataset=name, n=inst['n'], method=method,
                           R=bounds.get('max_delay',900)-bounds.get('min_delay',-60)+1,
                           median_seconds=statistics.median(times), raw_seconds=times,
                           peak_extra_bytes=peak, stability='PASS', **stats))
    return output


def main():
    dest = ROOT/'results'
    dest.mkdir(exist_ok=True)
    test_results = []
    cases = {'empty': [], 'one_flight': [5], 'all_ties': [12]*5,
             'negative_and_boundaries': [-60, 900, -1, 0, 900, -60],
             'already_sorted': [30, 12, 12, 0, -5], 'reversed': [-5, 0, 12, 12, 30]}
    for name, values in cases.items():
        inst = instance(values)
        assert solve_merge(inst) == solve_counting(inst) == reference(inst)
        test_results.append(name+': PASS')
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        inst = instance([rng.randint(-60, 900) for _ in range(1000)])
        assert solve_merge(inst) == solve_counting(inst) == reference(inst)
        test_results.append('random_seed_'+str(seed)+': PASS')
    rows = []
    manifest = json.loads((ROOT/'data/manifest.json').read_text())
    for dataset in manifest['datasets']:
        inst = problem.load_instance(ROOT/'data'/dataset['file'])
        expected = reference(inst)
        digest = hashlib.md5('\n'.join(expected).encode()).hexdigest()
        assert digest == dataset['reference']['md5_of_ids_joined_by_newline']
        rows += measure(dataset['file'], inst)
        test_results.append(dataset['file']+': BOTH PASS; manifest hash matches')
        print(dataset['file'], 'done', flush=True)
    inst = problem.load_instance(ROOT/'data/flights_n010000_schedule.csv')
    variants = [('clipped_0_100', [max(0,min(100,x)) for x in inst['delay']], 0,100),
                ('scaled_100', [x*100 for x in inst['delay']], -6000,90000),
                ('scaled_1000', [x*1000 for x in inst['delay']], -60000,900000)]
    for name, delays, lo, hi in variants:
        changed = dict(inst, delay=delays)
        rows += measure(name, changed, min_delay=lo, max_delay=hi)
        print(name, 'done', flush=True)
    cpu = platform.processor()
    p = Path('/proc/cpuinfo')
    if p.exists():
        cpu = next((s.split(':',1)[1].strip() for s in p.read_text().splitlines()
                    if s.startswith('model name')), cpu)
    environment = dict(python=sys.version, os=platform.platform(), cpu=cpu,
                       logical_cpus=os.cpu_count(), timing_runs=5,
                       memory='tracemalloc peak in a separate call; input excluded, returned output included',
                       timing='time.perf_counter; CSV load, validation, GC and memory tracing excluded')
    (dest/'results.json').write_text(json.dumps(dict(environment=environment, rows=rows, tests=test_results),indent=2))
    with (dest/'results.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (dest/'correctness.txt').write_text('\n'.join(test_results)+'\n')
    print(json.dumps(environment,indent=2))
    for row in rows:
        print(row['dataset'],row['method'],f"{row['median_seconds']:.6f}s",row['comparisons'],row['record_writes'],row['counter_writes'],f"{row['peak_extra_bytes']/1048576:.4f} MiB")
    try:
        make_plots(rows, dest)
    except ImportError:
        print('Install matplotlib to create plots; measurement files were saved.')


def make_plots(rows, dest):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import math
    plt.rcParams.update({'figure.dpi':160,'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    colors={'merge':'#3462AE','counting':'#D47721'}
    normal=[r for r in rows if r['dataset'].endswith('_schedule.csv')]
    fig,ax=plt.subplots(figsize=(7,4.5),layout='constrained')
    for method in colors:
        chosen=[r for r in normal if r['method']==method]
        ax.loglog([r['n'] for r in chosen],[r['median_seconds'] for r in chosen],'-o',label=method,color=colors[method])
    ax.set(xlabel='Number of flights n',ylabel='Median runtime (seconds)',title='Runtime versus input size')
    ax.legend();ax.grid(alpha=.2);fig.savefig(dest/'runtime_vs_n.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,4.5),layout='constrained')
    labels=['schedule','nearly_sorted','reversed']
    for j,method in enumerate(colors):
        vals=[next(r['median_seconds'] for r in rows if r['dataset']==f'flights_n010000_{order}.csv' and r['method']==method) for order in labels]
        ax.bar([i+(j-.5)*.35 for i in range(3)],vals,width=.35,label=method,color=colors[method])
    ax.set_xticks(range(3),['Schedule','Nearly sorted','Reversed'])
    ax.set(ylabel='Median runtime (seconds)',title='Input order comparison at n = 10,000');ax.legend()
    fig.savefig(dest/'runtime_vs_order.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,4.5),layout='constrained')
    for method in colors:
        chosen=[next(r for r in rows if r['dataset']==name and r['method']==method) for name in ['clipped_0_100','flights_n010000_schedule.csv','scaled_100','scaled_1000']]
        ax.semilogx([r['R'] for r in chosen],[r['median_seconds'] for r in chosen],'-o',label=method,color=colors[method])
    ax.set(xlabel='Allowed delay range width R',ylabel='Median runtime (seconds)',title='Range comparison at n = 10,000');ax.legend();ax.grid(alpha=.2)
    fig.savefig(dest/'runtime_vs_range.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,4.5),layout='constrained')
    for method in colors:
        chosen=[r for r in normal if r['method']==method]
        ax.plot([r['n'] for r in chosen],[r['comparisons'] for r in chosen],'-o',label=method,color=colors[method])
    ns=[r['n'] for r in normal if r['method']=='merge']
    ax.plot(ns,[n*math.log2(n) for n in ns],'--',color='#555555',label='n log2(n)')
    ax.plot(ns,[n*n for n in ns],':',color='#777777',label='n squared')
    ax.set_xscale('log');ax.set_yscale('symlog',linthresh=1)
    ax.set_ylim(0, 2*max(ns)**2)
    ax.set(xlabel='Number of flights n',ylabel='Delay-key comparisons',title='Comparison counts and theoretical growth')
    ax.legend();ax.grid(alpha=.2);fig.savefig(dest/'comparisons_vs_n.png');plt.close(fig)


if __name__ == '__main__':
    main()
