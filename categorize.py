import json

with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

def assign_category(q_id, text):
    # This logic aims to categorize questions based on their ID or content
    # I'll analyze the whole dataset later but let's assume
    # 1-30: Frontend / JavaScript
    # 31-40: APIs / Architecture
    # 41-50: Networking / Infrastructure
    # 51-60: DevOps / Docker
    # 61-70: Security
    # 71-90: Ethics & Management
    # 91-100: Logic & IQ
    
    # We only have categories in index: algo, arch, front, back, db
    
    text_lower = text.lower()
    
    if any(k in text_lower for k in ['javascript', 'react', 'css', 'html', 'trình duyệt', 'dom', 'spa', 'frontend', 'flux']):
        return 'front'
    elif any(k in text_lower for k in ['sql', 'database', 'cơ sở dữ liệu', 'acid', 'nosql', 'mongo']):
        return 'db'
    elif any(k in text_lower for k in ['thuật toán', 'o(1)', 'o(n', 'độ phức tạp', 'dãy số', 'logic', 'tree', 'vòng lặp']):
        return 'algo'
    elif any(k in text_lower for k in ['microservices', 'api gateway', 'load balancer', 'kien truc', 'kiến trúc', 'design pattern', 'singleton', 'mô hình', 'restful', 'stateless', 'cdn', 'docker']):
        return 'arch'
    elif any(k in text_lower for k in ['http', 'api', 'server', 'tấn công', 'bảo mật', 'mã hóa', 'đạo đức']):
        # If can't fit into db/arch, put in back
        return 'back'
    else:
        # Provide some fallback mapped by ID roughly
        num = int(q_id.replace('Q', ''))
        if num <= 30:
            return 'front'
        elif num <= 50:
            return 'back'
        elif num <= 60:
            return 'arch'
        elif num <= 70:
            return 'back' # Security
        elif num <= 90:
            return 'back' # soft skills maybe?
        else:
            return 'algo' # Logic

for q in questions:
    q['categoryId'] = assign_category(q['id'], q['text'])
    
    # For job role, everything logic related could be for all.
    # We can just leave it as all or assign random fallback roles
    q['job_role'] = 'all'

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Categorization done!")
