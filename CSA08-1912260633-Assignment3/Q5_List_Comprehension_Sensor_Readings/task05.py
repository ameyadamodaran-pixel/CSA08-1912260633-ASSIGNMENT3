import csv, time, sys
from pathlib import Path
DATA=Path(__file__).with_name("temperatures.csv")
def main():
    with DATA.open(newline="",encoding="utf-8") as f: raw=[float(r["celsius"]) for r in csv.DictReader(f)]
    valid=[]
    for c in raw:
        if -50 <= c <= 50: valid.append((c,c*9/5+32))
    comp=[(c,c*9/5+32) for c in raw if -50 <= c <= 50]
    mapped=list(map(lambda c:(c,c*9/5+32),filter(lambda c:-50<=c<=50,raw)))
    alarms=[(i+1,c) for i,c in enumerate(raw) if c<2 or c>8]
    print("valid Celsius/Fahrenheit:",[(round(c,1),round(f,1)) for c,f in comp])
    print("loop == comprehension == map/filter:",valid==comp==mapped)
    print("alarm minutes outside 2–8 C:",alarms)
    print("dictionary comprehension:",{i+1:round(c*9/5+32,1) for i,c in enumerate(raw) if -50<=c<=50})
    print("set comprehension of valid Celsius:",sorted({c for c in raw if -50<=c<=50}))
    print("generator/list memory for 100k:")
    data=list(range(100_000)); lst=[x*x for x in data]; gen=(x*x for x in data)
    print(sys.getsizeof(lst),sys.getsizeof(gen),"bytes (container sizes; generator excludes yielded values)")
    print("Benchmark n, loop_s, comprehension_s, map_filter_s")
    for n in (10_000,100_000,1_000_000):
        vals=[(i%101)-50 for i in range(n)]
        t=time.perf_counter(); out=[]
        for x in vals:
            if -50<=x<=50: out.append(x*9/5+32)
        a=time.perf_counter()-t
        t=time.perf_counter(); out2=[x*9/5+32 for x in vals if -50<=x<=50]; b=time.perf_counter()-t
        t=time.perf_counter(); out3=list(map(lambda x:x*9/5+32,filter(lambda x:-50<=x<=50,vals))); c=time.perf_counter()-t
        assert out==out2==out3
        print(f"{n}: {a:.6f}, {b:.6f}, {c:.6f}")
if __name__=="__main__": main()
