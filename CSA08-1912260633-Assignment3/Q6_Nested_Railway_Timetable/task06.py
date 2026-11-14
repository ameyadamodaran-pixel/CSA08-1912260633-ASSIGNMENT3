import json, time, sys
from pathlib import Path
DATA=Path(__file__).with_name("timetable.json")
def load():
    raw=json.loads(DATA.read_text(encoding="utf-8"))
    return {no:{"name":v["name"],"stops":[tuple(x) for x in v["stops"]],"days":set(v["days"])} for no,v in raw.items()}
def station_query(table, station, day):
    found=[]
    for no,info in table.items():
        if day in info["days"] or "Daily" in info["days"]:
            for st,arr,dep in info["stops"]:
                if st==station: found.append((no,info["name"],arr,dep))
    return sorted(found,key=lambda x:x[3])
def build_index(table):
    index={}
    for no,info in table.items():
        for st,arr,dep in info["stops"]: index.setdefault(st,[]).append((no,info,arr,dep))
    return index
def indexed_query(index,station,day):
    found=[(no,info["name"],arr,dep) for no,info,arr,dep in index.get(station,[]) if day in info["days"] or "Daily" in info["days"]]
    return sorted(found,key=lambda x:x[3])
def main():
    table=load(); print("Trains:",len(table))
    for no,info in table.items():
        print(no,info["name"],"|",[(s,a,d) for s,a,d in sorted(info["stops"],key=lambda x:x[2])],"|",sorted(info["days"]))
    # third station's departure time in a train's stop list
    print("third station departure, train 12601:",table["12601"]["stops"][2][2])
    index=build_index(table)
    print("Katpadi on Mon:",station_query(table,"Katpadi","Mon"))
    print("indexed matches equal:",station_query(table,"Katpadi","Mon")==indexed_query(index,"Katpadi","Mon"))
    print("unknown station:",indexed_query(index,"Atlantis","Mon"))
    print("not-running day:",indexed_query(index,"Tambaram","Mon"))
    print("Benchmark query count, scan_s, indexed_s")
    # deterministic scaled synthetic timetable; benchmark the query pattern
    for n in (100,1000,10000):
        synthetic={f"T{i}":{"name":f"Train {i}","stops":[(f"S{j%100}","08:00","08:10") for j in range(8)],"days":{"Mon"}} for i in range(n)}
        ix=build_index(synthetic)
        t=time.perf_counter()
        for _ in range(100): station_query(synthetic,"S42","Mon")
        scan=time.perf_counter()-t
        t=time.perf_counter()
        for _ in range(100): indexed_query(ix,"S42","Mon")
        fast=time.perf_counter()-t
        print(f"{n}: {scan:.6f}, {fast:.6f}; index entries={sum(map(len,ix.values()))}")
    index_bytes=sys.getsizeof(index)+sum(sys.getsizeof(bucket)+sum(sys.getsizeof(entry) for entry in bucket) for bucket in index.values())
    print("index memory estimate:",index_bytes,"bytes (dictionary, station buckets and index-entry tuples; shared train records excluded)")
if __name__=="__main__": main()
