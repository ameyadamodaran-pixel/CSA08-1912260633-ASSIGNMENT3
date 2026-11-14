import copy, sys, time

def main():
    rows, cols = 3, 4
    bad = [[0] * cols] * rows
    bad[0][1] = 7
    good = [[0 for _ in range(cols)] for _ in range(rows)]
    good[0][1] = 7
    print("bad :", bad); print("good:", good)
    print("row identity:", bad[0] is bad[1], good[0] is good[1])
    stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
    print("tuple key lookup:", stops[(13.0418, 80.2341)])
    try: stops[[13.0418, 80.2341]] = "Invalid key"
    except TypeError as e: print("list key error:", type(e).__name__, str(e))
    original = [[1, 2], [3, 4]]
    alias = original; shallow = copy.copy(original); sliced = original[:]; deep = copy.deepcopy(original)
    original[0][0] = 99
    print("alias is original:", alias is original)
    print("shallow sees nested change:", shallow[0][0], "deep copy retains:", deep[0][0])
    def change_first(items): items[0] = "changed"
    values=["before"]; change_first(values); print("mutated caller list:", values)
    tuple_with_list = ([1, 2], "fixed outer tuple")
    tuple_with_list[0].append(3); print("mutable item inside tuple:", tuple_with_list)
    values_list=list(range(1_000_000)); values_tuple=tuple(values_list)
    print("container shallow sizes for 1,000,000 refs:", sys.getsizeof(values_list), sys.getsizeof(values_tuple), "bytes")
    t=time.perf_counter(); temp=tuple(range(100_000)); tuple_create=time.perf_counter()-t
    t=time.perf_counter(); temp_list=list(range(100_000)); list_create=time.perf_counter()-t
    t=time.perf_counter(); _=temp[50_000]; tuple_index=time.perf_counter()-t
    t=time.perf_counter(); _=temp_list[50_000]; list_index=time.perf_counter()-t
    print(f"100k create seconds tuple={tuple_create:.6f}, list={list_create:.6f}")
    print(f"single index seconds tuple={tuple_index:.9f}, list={list_index:.9f}")
if __name__=="__main__": main()
