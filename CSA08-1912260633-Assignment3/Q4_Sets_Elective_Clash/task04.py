import random, time

def analyse(elective_a,elective_b,all_students):
    a,b=set(elective_a),set(elective_b)
    clash=a & b
    exactly_one=a ^ b
    neither=all_students-(a|b)
    return sorted(clash),sorted(exactly_one),sorted(neither)

def main():
    a={"192311001","192311004","192311007","192311009"}
    b={"192311002","192311004","192311009","192311010"}
    all_students={f"192311{i:03d}" for i in range(1,11)}
    clash,one,neither=analyse(a,b,all_students)
    print("clash:",clash); print("exactly one:",one); print("neither:",neither)
    print("method results:", sorted(a.intersection(b)), sorted(a.symmetric_difference(b)), sorted(all_students.difference(a.union(b))))
    print("duplicate removed:", len([*a,*a])>len(a))
    print("empty electives:", analyse(set(),set(),all_students))
    print("identical electives:", analyse(a,a,all_students))
    print("Benchmark membership: n, list seconds, set seconds")
    rng=random.Random(42)
    for n in (10_000,100_000,1_000_000):
        values=list(range(n)); s=set(values); probes=[rng.randrange(n) for _ in range(1000)]
        t=time.perf_counter(); _=[x in values for x in probes]; tl=time.perf_counter()-t
        t=time.perf_counter(); _=[x in s for x in probes]; ts=time.perf_counter()-t
        print(f"{n}: {tl:.6f}, {ts:.6f}")
    # A small common-student comparison
    x=list(range(500)); y=list(range(250,750))
    t=time.perf_counter(); common=[v for v in x for w in y if v==w]; nested=time.perf_counter()-t
    t=time.perf_counter(); common2=sorted(set(x)&set(y)); set_time=time.perf_counter()-t
    print(f"common students: nested={nested:.6f}s, set intersection={set_time:.6f}s, same={set(common)==set(common2)}")
if __name__=="__main__": main()
