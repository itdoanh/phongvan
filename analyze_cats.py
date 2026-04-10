import json

with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

for q in questions[:100:10]: # Print every 10th question to get a sense of contents
    print(f"{q['id']} - {q['text'][:50]}...")
