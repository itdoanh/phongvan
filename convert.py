import json

def parse_txt():
    with open('cauhoi.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the starting point where questions begin
    # They seem to start after "Đáp Án\n1\n"
    import re
    # Match the pattern of question number, question text, 4 options, and the answer
    # A question block:
    # <number>
    # <question_text> (can span multiple lines, until A))
    # A) <option>
    # B) <option>
    # C) <option>
    # D) <option>
    # <Answer letter>
    
    # We can split on number followed by newline if it's 1 to 100
    questions = []
    
    blocks = re.split(r'\n(\d+)\n', '\n' + content)

    for i in range(1, len(blocks)-1, 2):
        q_num_str = blocks[i]
        q_num = int(q_num_str)
        text_block = blocks[i+1].strip()
        
        # Now text_block contains question text, A)... B)... C)... D)... Answer
        # Let's try to extract A), B), C), D) and answer
        pattern = r"(.*?)\nA\)\s*(.*?)\nB\)\s*(.*?)\nC\)\s*(.*?)\nD\)\s*(.*?)\n([A-D])(?:\n|$)"
        match = re.search(pattern, text_block, re.DOTALL)
        if match:
            q_text = match.group(1).strip()
            opt_a = match.group(2).strip()
            opt_b = match.group(3).strip()
            opt_c = match.group(4).strip()
            opt_d = match.group(5).strip()
            ans = match.group(6).strip()
            
            correct_idx = ord(ans) - ord('A')
            
            questions.append({
                "id": f"Q{q_num:03d}",
                "job_role": "all",
                "location": "all",
                "categoryId": "general",
                "text": q_text,
                "options": [opt_a, opt_b, opt_c, opt_d],
                "correct": correct_idx,
                "explanation": ""
            })
    
    with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

parse_txt()
