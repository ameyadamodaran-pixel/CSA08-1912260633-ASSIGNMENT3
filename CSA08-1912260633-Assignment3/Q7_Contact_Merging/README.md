# Q7 – Design a Contact-Merging Program from First Principles
Run: `python task07.py`.
Input: `contacts.json` contains duplicates, alternate phone formats and missing phone values.
Result: normalizes phone numbers, groups by normalized phone (email/name fallback when no phone exists), merges names/numbers/emails, tests duplicates and missing fields, and measures 1,000/100,000 contacts.
Limitation: phone-number identity is a practical rule, not proof of identity; shared family numbers and number recycling require manual review. Name-only matches are not merged automatically.
