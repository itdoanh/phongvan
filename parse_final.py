import json
import re

with open('cauhoi.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

blocks = []
current_text = []
questions = []

i = 0
while i < len(lines):
    if lines[i].isdigit() and 1 <= int(lines[i]) <= 100:
        q_num = int(lines[i])
        
        if current_text:
            blocks.append({'type': 'text', 'content': '\n\n'.join(current_text)})
            current_text = []
            
        q_text = lines[i+1]
        i += 2
        options = []
        while i < len(lines) and (lines[i].startswith('A)') or lines[i].startswith('B)') or lines[i].startswith('C)') or lines[i].startswith('D)') or (len(lines[i]) >= 3 and lines[i][0].isalpha() and lines[i][1:3] == ') ')):
            options.append(lines[i][3:].strip())
            i += 1
            
        ans = ""
        if i < len(lines) and lines[i] in ['A', 'B', 'C', 'D']:
            ans = lines[i]
            i += 1
            
        correct_idx = ord(ans) - ord('A') if len(ans) == 1 else 0

        c_id = "c" + str((q_num-1)//15 + 1 if q_num <= 90 else 7)
        
        q_obj = {
            "id": f"Q{q_num:03d}",
            "job_role": "all",
            "location": "all",
            "categoryId": c_id,
            "text": q_text,
            "options": options,
            "correct": correct_idx,
            "explanation": ""
        }
        questions.append(q_obj)
        blocks.append({'type': 'question', 'question': q_obj})
        continue
    
    ignore_lines = ["Số Thứ Tự", "Câu Hỏi Đánh Giá Năng Lực", "Các Lựa Chọn Khả Thi", "Đáp Án", 
                    "Câu Hỏi Đánh Giá Năng Lực (Tình huống Mô phỏng)", "Các Lựa Chọn Phản Ứng Khả Thi", 
                    "Câu Hỏi Đánh Giá Năng Lực (Tư duy Trừu tượng & Logic)"]
    if lines[i] not in ignore_lines:
        current_text.append(lines[i])
    i += 1

if current_text:
    blocks.append({'type': 'text', 'content': '\n\n'.join(current_text)})

# We have 7 categories: c1 to c7.
# Let's collect all text into the explanations.
# The text block right before Q1 goes to c1.
# The text block between Q15 and Q16 goes partially to c1, partially to c2. Or we can just append it to the nearest category.
# Let's just create a dictionary of texts per category.
category_explanations = {f"c{i}": [] for i in range(1, 8)}

current_cat = "c1"

for i in range(len(blocks)):
    b = blocks[i]
    if b['type'] == 'text':
        # the text before any question applies to the first category it encounters
        # if it's after the first question, it applies to the CURRENT category
        # wait, if it's the block between Q15 and Q16, it's after Q15 (c1).
        # We can split it. Or just assign it to the question's explanation field directly!
        pass

# Actually, the simplest way is to put the text directly into the questions' explanation array.
# For any question Q, its explanation = the text block before it + the text block after it (until the next question).
# But text blocks are shared. So maybe just give each category a "global explanation" and inject it into the first question of that category?
# No, let's just dump the text blocks into a "category knowledge base" string and put it in ALL questions of that category.

for cat in range(1, 8):
    cat_id = f"c{cat}"
    # find all text blocks that are adjacent to questions of this category
    cat_texts = []
    
    for i, b in enumerate(blocks):
        if b['type'] == 'text':
            # is it adjacent to a question in cat_id?
            adjacent_cats = set()
            if i > 0 and blocks[i-1]['type'] == 'question':
                adjacent_cats.add(blocks[i-1]['question']['categoryId'])
            if i < len(blocks)-1 and blocks[i+1]['type'] == 'question':
                adjacent_cats.add(blocks[i+1]['question']['categoryId'])
            
            if cat_id in adjacent_cats:
                cat_texts.append(b['content'])

    final_exp = "\n\n".join(cat_texts)
    
    for q in questions:
        if q['categoryId'] == cat_id:
            q['explanation'] = final_exp

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Done parsing")
