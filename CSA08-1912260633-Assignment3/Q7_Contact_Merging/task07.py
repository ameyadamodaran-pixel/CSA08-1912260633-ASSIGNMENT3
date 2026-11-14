import json, re, random, time
from pathlib import Path
DATA=Path(__file__).with_name("contacts.json")
def normalize_phone(value):
    digits=re.sub(r"\D", "", value or "")
    if digits.startswith("91") and len(digits)==12: digits=digits[2:]
    return digits

def normalize_name(value): return " ".join((value or "").lower().replace("."," ").split())
def merge_contacts(contacts):
    # Number is the primary identity key. Contacts without a phone are kept by normalized email.
    groups={}; email_only={}
    for contact in contacts:
        phone=normalize_phone(contact.get("phone","")); email=(contact.get("email") or "").strip().lower()
        key=phone if phone else ("email:"+email if email else "name:"+normalize_name(contact.get("name","")))
        target=groups if phone else email_only
        entry=target.setdefault(key,{"names":set(),"phones":set(),"emails":set()})
        name=(contact.get("name") or "").strip()
        if name: entry["names"].add(name)
        if phone: entry["phones"].add(phone)
        if email: entry["emails"].add(email)
    merged=[]
    for key,entry in {**groups,**email_only}.items():
        merged.append({"identity_key":key,"names":sorted(entry["names"]),"phones":sorted(entry["phones"]),"emails":sorted(entry["emails"])})
    return sorted(merged,key=lambda x:x["identity_key"])
def main():
    contacts=json.loads(DATA.read_text(encoding="utf-8")); result=merge_contacts(contacts)
    print("Merged contact groups:")
    for item in result: print(item)
    print("input contacts:",len(contacts),"merged groups:",len(result))
    # duplicate and missing-field checks
    tests=[{"name":"A","phone":"+91 98400 12345"},{"name":"A2","phone":"9840012345"},{"name":"No phone","email":"x@y.com"}]
    print("test groups:",merge_contacts(tests))
    print("Benchmark contacts, seconds")
    rng=random.Random(7)
    for n in (1_000,100_000):
        sample=[{"name":f"Person {i}","phone":f"+91 {9000000000+(i//2):010d}","email":f"p{i}@example.com"} for i in range(n)]
        t=time.perf_counter(); out=merge_contacts(sample); elapsed=time.perf_counter()-t
        print(f"{n}: {elapsed:.6f}; groups={len(out)}")
if __name__=="__main__": main()
