from collections import Counter, defaultdict
from pathlib import Path
import re, random, time
DATA=Path(__file__).with_name("complaints.txt")
STOP={"not", "high", "the", "a", "is", "and", "to"}

def tokenize(text): return re.findall(r"[a-z]+", text.lower())
def frequencies(texts, stop):
    counts={}
    for text in texts:
        for word in tokenize(text):
            if word not in stop: counts[word]=counts.get(word,0)+1
    return counts

def top(counts,k): return sorted(counts.items(), key=lambda item:(-item[1],item[0]))[:k]

def main():
    calls=DATA.read_text(encoding="utf-8").splitlines()
    print("top words:", top(frequencies(calls,STOP),3))
    records=[("Thanjavur", "seeds delayed"), ("Madurai", "irrigation issue"), ("Thanjavur", "fertiliser supply"), ("Salem", "crop disease")]
    by_district=defaultdict(list); by_crop=defaultdict(list)
    for district, complaint in records: by_district[district].append(complaint)
    for crop, complaint in [("rice","seed delay"),("cotton","pest issue"),("rice","fertiliser")]: by_crop[crop].append(complaint)
    print("complaints by district:", dict(by_district)); print("complaints by crop:", dict(by_crop))
    print("empty text:", frequencies([""],STOP), "case/punctuation:", frequencies(["SEEDS, seeds! Seeds."],STOP))
    print("expected tie order:", top({"received":2,"price":2,"seeds":3},3))
    rng=random.Random(42); vocab=["seed","price","water","crop","delay","fertiliser","loan","pest"]
    print("Benchmark words: n, dict_s, list_count_s, Counter_s")
    for n in (1_000,10_000,100_000):
        words=[rng.choice(vocab) for _ in range(n)]
        t=time.perf_counter(); d={}
        for x in words: d[x]=d.get(x,0)+1
        td=time.perf_counter()-t
        t=time.perf_counter(); lc={x:words.count(x) for x in set(words)}; tl=time.perf_counter()-t
        t=time.perf_counter(); c=Counter(words); tc=time.perf_counter()-t
        assert d==lc==dict(c)
        print(f"{n}: {td:.6f}, {tl:.6f}, {tc:.6f}")
    print("Dictionary views: keys() gives keys, values() gives values, items() gives key-value pairs.")
if __name__=="__main__": main()
