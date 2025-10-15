import csv
import random

rows = 16     # จำนวนแถว
cols = 60      # จำนวนคอลัมน์

with open('random_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([f'Q{i+1}' for i in range(cols)])  # สร้างหัวคอลัมน์ เช่น Q1, Q2, ..., Q60

    for _ in range(rows):
        row = [random.randint(-3, 3) for _ in range(cols)]  # สุ่มตัวเลขในแต่ละคอลัมน์
        writer.writerow(row)

print("✅ สร้างไฟล์ random_data.csv เรียบร้อยแล้ว! (14 แถว x 60 คอลัมน์)")
