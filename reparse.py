import json
import re

with open('cauhoi.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

blocks = [] # text blocks
current_text = []

# identify the questions
questions_lookup = {}
questions = []

i = 0
while i < len(lines):
    # a question starts with a number followed by text, A), B), C), D) and single letter
    if lines[i].isdigit():
        q_num = int(lines[i])
        if 1 <= q_num <= 100:
            # save any accumulated text
            if current_text:
                blocks.append({'type': 'text', 'content': '\n'.join(current_text)})
                current_text = []
                
            q_text = lines[i+1]
            i += 2
            options = []
            while i < len(lines) and (lines[i].startswith('A)') or lines[i].startswith('B)') or lines[i].startswith('C)') or lines[i].startswith('D)')):
                options.append(lines[i][3:].strip())
                i += 1
            
            ans = ""
            if i < len(lines) and lines[i] in ['A', 'B', 'C', 'D']:
                ans = lines[i]
                i += 1
            
            correct_idx = ord(ans) - ord('A') if ans else 0

            # The block type is 'question'
            q_obj = {
                "id": f"Q{q_num:03d}",
                "q_num": q_num,
                "job_role": "all",
                "location": "all",
                "categoryId": "c" + str((q_num-1)//15 + 1 if q_num <= 90 else 7),
                "text": q_text,
                "options": options,
                "correct": correct_idx,
                "explanation": ""
            }
            questions.append(q_obj)
            blocks.append({'type': 'question', 'question': q_obj})
            continue
    
    # Check if lines[i] is just headers like "Số Thứ Tự", "Câu Hỏi Đánh Giá Năng Lực", etc
    ignore_lines = ["Số Thứ Tự", "Câu Hỏi Đánh Giá Năng Lực", "Các Lựa Chọn Khả Thi", "Đáp Án", "Câu Hỏi Đánh Giá Năng Lực (Tình huống Mô phỏng)", "Các Lựa Chọn Phản Ứng Khả Thi", "Câu Hỏi Đánh Giá Năng Lực (Tư duy Trừu tượng & Logic)"]
    if lines[i] not in ignore_lines:
        current_text.append(lines[i])
    i += 1

if current_text:
    blocks.append({'type': 'text', 'content': '\n'.join(current_text)})

# Now attach the nearest text blocks to the questions' explanation
# Group questions by their 1-15, 16-30... segments
sections = [
    (1, 15, "cat1"),
    (16, 30, "cat2"),
    (31, 45, "cat3"),
    (46, 60, "cat4"),
    (61, 75, "cat5"),
    (76, 90, "cat6"),
    (91, 100, "cat7")
]

# We can just construct the explanation by looking at the text blocks that appear BEFORE the first question in the section, and AFTER the last question in the section (but before the NEXT section's text).
for idx, b in enumerate(blocks):
    if b['type'] == 'text':
        print(f"TEXT BLOCK: {b['content'][:50]}...")
    else:
        print(f"Q BLOCK: {b['question']['q_num']}")

# Let's find text blocks that belong to each section.
section_texts = {s[2]: [] for s in sections}

current_section = "cat1"
for b in blocks:
    if b['type'] == 'text':
        # Don't add if it's empty
        if not b['content'].strip(): continue
        section_texts[current_section].append(b['content'])
    elif b['type'] == 'question':
        # update current section based on question
        current_section = b['question']['categoryId']

# Since text blocks AFTER a section's questions but BEFORE the next section's headers
# actually belong to the PREVIOUS section because the next section's header is also in the same text block, we might have merged them.
# Let's refine text assignment:
# A text block between Q15 and Q16 contains BOTH the outro of Q1-Q15 AND the intro to Q16-Q30.
