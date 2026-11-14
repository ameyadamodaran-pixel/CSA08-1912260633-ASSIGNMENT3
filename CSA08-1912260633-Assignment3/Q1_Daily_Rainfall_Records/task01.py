import csv, random, time
from pathlib import Path

DATA = Path(__file__).with_name("rainfall.csv")

def load_readings(path=DATA):
    with open(path, newline="", encoding="utf-8") as f:
        return [float(row["rainfall_mm"]) for row in csv.DictReader(f)]

def weekly_totals(readings):
    return [round(sum(readings[i:i+7]), 2) for i in range(0, len(readings), 7)]

def moving_average_naive(values, window=7):
    if window <= 0: raise ValueError("window must be positive")
    if len(values) < window: return []
    return [sum(values[i:i+window])/window for i in range(len(values)-window+1)]

def moving_average_running(values, window=7):
    if window <= 0: raise ValueError("window must be positive")
    if len(values) < window: return []
    current = sum(values[:window]); result = [current/window]
    for i in range(window, len(values)):
        current += values[i] - values[i-window]
        result.append(current/window)
    return result

def benchmark():
    print("Benchmark (n, naive seconds, running-sum seconds)")
    rng = random.Random(42)
    for n in (365, 36_500, 365_000):
        data = [rng.random()*50 for _ in range(n)]
        t=time.perf_counter(); a=moving_average_naive(data); naive=time.perf_counter()-t
        t=time.perf_counter(); b=moving_average_running(data); fast=time.perf_counter()-t
        assert len(a)==len(b) and all(abs(x-y)<1e-9 for x,y in zip(a,b))
        print(f"{n}, {naive:.6f}, {fast:.6f}")

def main():
    r=load_readings(); weeks=weekly_totals(r); avg=moving_average_running(r)
    wet=max(range(len(weeks)), key=weeks.__getitem__); dry=min(range(len(weeks)), key=weeks.__getitem__)
    peak=max(r); low=min(r)
    print(f"Readings: {len(r)}; weekly totals: {len(weeks)}")
    print(f"Wettest week: {wet+1}, total={weeks[wet]:.1f} mm")
    print(f"Driest week: {dry+1}, total={weeks[dry]:.1f} mm")
    print(f"Maximum daily rainfall: {peak:.1f} mm on day {r.index(peak)+1}")
    print(f"Minimum daily rainfall: {low:.1f} mm on day {r.index(low)+1}")
    print(f"7-day moving averages: {len(avg)}; first={avg[0]:.2f} mm")
    dry_days=[i+1 for i,x in enumerate(r) if x==0]
    print(f"Dry days (0 mm): {len(dry_days)}; first 15={dry_days[:15]}")
    print("Slices: readings[7:14] = days 8-14; readings[-7:] = final 7 days; readings[::7] = every 7th reading")
    print("Edge tests:", moving_average_running([]), moving_average_running([1,2,3,4,5,6]))
    benchmark()
if __name__=="__main__": main()
