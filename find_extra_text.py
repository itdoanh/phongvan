import re

with open('cauhoi.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

i = 0
in_q = False
while i < len(lines):
    if lines[i].isdigit():
        q_num = int(lines[i])
        i += 1
        q_text = lines[i]
        i += 1
        
        while i < len(lines) and (lines[i].startswith('A)') or lines[i].startswith('B)') or lines[i].startswith('C)') or lines[i].startswith('D)') or (lines[i][0].isalpha() and lines[i][1:3] == ') ')):
            i += 1
            
        if i < len(lines) and lines[i] in ['A', 'B', 'C', 'D']:
            i += 1
            
        # Any text between answer letter and next digit?
        extra = []
        while i < len(lines) and not lines[i].isdigit():
            extra.append(lines[i])
            i += 1
            
        if len(extra) > 0:
            print(f"Extra text after Q{q_num}:")
            for t in extra:
                print("  ", t)
    else:
        # Before question 1
        i += 1
