import csv
import math

filename = "random_data.csv"

MBTI_AVG = {
    "ENFJ": [], "ENFP": [], "ENTJ": [], "ENTP": [],
    "ESFJ": [], "ESFP": [], "ESTJ": [], "ESTP": [],
    "INFJ": [], "INFP": [], "INTJ": [], "INTP": [],
    "ISFJ": [], "ISFP": [], "ISTJ": [], "ISTP": []
}

# อ่านไฟล์
with open(filename, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    print(reader)
    for row in reader:
        mbti = row['MTBI'].strip().upper()
        # แปลงค่าทุกค่าเป็น float
        data = [float(v) for k, v in row.items() if k != 'MTBI']
        if mbti in MBTI_AVG:
            MBTI_AVG[mbti] = data  # เก็บเป็น list เดียว (สมมติมีคนเดียว)
        

# ตัวอย่างคำตอบของ person2
person2 = [1, -2, 2, 0, 0, -3, 2, 2, -2, 0, 1, -2] * 5  # 60 ข้อ

# คำนวณ Cosine similarity
for mbti, data in MBTI_AVG.items():
    if data:  # ตรวจสอบว่ามีข้อมูล
        dot_product = sum(a*b for a, b in zip(data, person2))
        norm1 = math.sqrt(sum(a**2 for a in data))
        norm2 = math.sqrt(sum(b**2 for b in person2))
        cosine_similarity = dot_product / (norm1 * norm2)
        print(f"{mbti}: {cosine_similarity:.4f}")
