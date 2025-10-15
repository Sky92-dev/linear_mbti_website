from flask import Flask, request, render_template_string, redirect, url_for, send_file, flash, render_template,session
import csv
import os
from datetime import datetime
from io import StringIO
import math
import json

filename = "mbti_base_profiles.csv"

app = Flask(__name__)
app.secret_key = "replace-with-a-random-secret"  # needed for flash messages
app.secret_key = os.urandom(24)
MBTI_AVG = {
        "ENFJ": [], "ENFP": [], "ENTJ": [], "ENTP": [],
        "ESFJ": [], "ESFP": [], "ESTJ": [], "ESTP": [],
        "INFJ": [], "INFP": [], "INTJ": [], "INTP": [],
        "ISFJ": [], "ISFP": [], "ISTJ": [], "ISTP": []
    }

    # อ่านไฟล์
with open(filename, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        mbti = row['MBTI'].strip().upper()
        # แปลงค่าทุกค่าเป็น float
        data = [float(v) for k, v in row.items() if k != 'MBTI']
        if mbti in MBTI_AVG:
            MBTI_AVG[mbti] = data 
            
question = [
    "คุณมักจะสร้างเพื่อนใหม่อยู่เป็นประจำ",
    "แนวคิดที่ซับซ้อนและแปลกใหม่ทำให้คุณตื่นเต้นมากกว่าแนวคิดที่เรียบง่ายตรงไปตรงมา",
    "คุณมักจะเชื่อในสิ่งที่กระทบความรู้สึกมากกว่าข้อเท็จจริง",
    "พื้นที่ใช้ชีวิตและการทำงานของคุณมักสะอาดและเป็นระเบียบ",
    "คุณมักสงบนิ่งได้แม้อยู่ในสถานการณ์กดดัน",
    "คุณรู้สึกประหม่าเมื่อต้องสร้างเครือข่ายหรือนำเสนอตัวเองกับคนแปลกหน้า",
    "คุณมักจะวางแผนและจัดการงานได้ดี มักทำเสร็จก่อนกำหนด",
    "เรื่องราวและอารมณ์ของผู้คนส่งผลต่อคุณมากกว่าข้อมูลหรือตัวเลข",
    "คุณชอบใช้เครื่องมือจัดระเบียบ เช่น ตารางเวลา หรือรายการสิ่งที่ต้องทำ",
    "แม้แต่ความผิดพลาดเล็กน้อยก็อาจทำให้คุณสงสัยในความสามารถของตนเองได้",
    "คุณรู้สึกสบายใจที่จะเข้าไปคุยกับคนที่คุณสนใจโดยไม่ลังเล",
    "คุณไม่ค่อยสนใจการสนทนาเกี่ยวกับการตีความผลงานสร้างสรรค์ในแบบต่าง ๆ",
    "คุณให้ความสำคัญกับข้อเท็จจริงมากกว่าความรู้สึกของคนอื่นเมื่อต้องตัดสินใจ",
    "คุณมักปล่อยให้วันของคุณดำเนินไปโดยไม่มีแผนที่แน่นอน",
    "คุณแทบไม่กังวลเลยว่าคนอื่นจะมองคุณอย่างไรเมื่อพบกันครั้งแรก",
    "คุณชอบทำกิจกรรมที่ต้องทำงานเป็นทีม",
    "คุณชอบทดลองแนวทางใหม่ ๆ ที่ยังไม่เคยมีใครลองมาก่อน",
    "คุณให้ความสำคัญกับความอ่อนไหวต่อความรู้สึกมากกว่าความตรงไปตรงมา",
    "คุณมักมองหาประสบการณ์หรือความรู้ใหม่ ๆ เพื่อเรียนรู้เพิ่มเติมอยู่เสมอ",
    "คุณมักกังวลว่าสิ่งต่าง ๆ อาจจะไม่เป็นไปตามที่หวัง",
    "คุณชอบทำกิจกรรมคนเดียวมากกว่าการอยู่ในกลุ่ม",
    "คุณไม่สามารถจินตนาการว่าตัวเองจะเขียนนิยายเป็นอาชีพได้",
    "คุณให้ความสำคัญกับประสิทธิภาพของการตัดสินใจ แม้จะต้องละเลยอารมณ์ของผู้อื่นก็ตาม",
    "คุณชอบทำงานบ้านหรือหน้าที่ให้เสร็จก่อนค่อยพักผ่อน",
    "เวลามีข้อขัดแย้ง คุณมักให้ความสำคัญกับการพิสูจน์ว่าคุณถูกมากกว่าการรักษาน้ำใจคนอื่น",
    "คุณมักรอให้คนอื่นแนะนำตัวก่อนในงานสังคม",
    "อารมณ์ของคุณสามารถเปลี่ยนแปลงได้อย่างรวดเร็ว",
    "คุณไม่ค่อยถูกโน้มน้าวด้วยเหตุผลทางอารมณ์",
    "คุณมักจะทำสิ่งต่าง ๆ ในวินาทีสุดท้าย",
    "คุณชอบถกเถียงเกี่ยวกับประเด็นทางจริยธรรม",
    "คุณมักจะชอบอยู่กับคนอื่นมากกว่าการอยู่คนเดียว",
    "คุณมักจะรู้สึกเบื่อเมื่อการสนทนาเริ่มซับซ้อนหรือเป็นเชิงทฤษฎีมากเกินไป",
    "เมื่อข้อเท็จจริงกับความรู้สึกขัดแย้งกัน คุณมักจะทำตามหัวใจของตัวเอง",
    "คุณรู้สึกว่าการรักษาตารางเวลาการเรียนหรือการทำงานให้คงที่เป็นเรื่องยาก",
    "คุณแทบไม่ลังเลหรือตั้งคำถามกับการตัดสินใจของตัวเอง",
    "เพื่อน ๆ มักจะมองว่าคุณเป็นคนร่าเริงและเปิดเผย",
    "คุณรู้สึกดึงดูดกับงานสร้างสรรค์ เช่น การเขียน",
    "คุณมักจะตัดสินใจโดยอิงจากข้อเท็จจริงมากกว่าความรู้สึก",
    "คุณชอบมีรายการสิ่งที่ต้องทำในแต่ละวัน",
    "คุณแทบไม่รู้สึกไม่มั่นใจในตัวเอง",
    "คุณมักหลีกเลี่ยงการโทรศัพท์",
    "คุณชอบสำรวจแนวคิดหรือมุมมองใหม่ ๆ ที่ไม่คุ้นเคย",
    "คุณสามารถเข้ากับคนที่เพิ่งรู้จักได้อย่างง่ายดาย",
    "หากแผนของคุณถูกรบกวน สิ่งสำคัญที่สุดของคุณคือพยายามกลับเข้าสู่แผนให้เร็วที่สุด",
    "คุณยังคงรู้สึกไม่สบายใจเกี่ยวกับความผิดพลาดที่เกิดขึ้นในอดีต",
    "คุณไม่ค่อยสนใจการพูดคุยเกี่ยวกับทฤษฎีหรือภาพอนาคตของโลก",
    "อารมณ์ของคุณมักควบคุมคุณมากกว่าที่คุณควบคุมอารมณ์ของตัวเอง",
    "เมื่อคุณตัดสินใจ คุณมักจะคิดถึงความรู้สึกของคนที่ได้รับผลกระทบมากกว่าสิ่งที่มีเหตุผลที่สุด",
    "สไตล์การทำงานของคุณมักเป็นช่วง ๆ ตามแรงบันดาลใจ มากกว่าการทำงานอย่างสม่ำเสมอ",
    "เมื่อมีคนมองว่าคุณเป็นคนดี คุณมักสงสัยว่าเขาจะรู้สึกผิดหวังในตัวคุณเมื่อไร",
    "คุณอยากได้งานที่ให้คุณทำงานคนเดียวเป็นส่วนใหญ่",
    "คุณคิดว่าการครุ่นคิดเรื่องปรัชญาเป็นเรื่องไร้ประโยชน์",
    "คุณรู้สึกดึงดูดกับสถานที่ที่มีความคึกคักและเต็มไปด้วยผู้คนมากกว่าสถานที่ที่เงียบสงบ",
    "ถ้าการตัดสินใจนั้น ‘รู้สึกถูกต้อง’ คุณมักจะทำเลยโดยไม่ต้องหาหลักฐานเพิ่มเติม",
    "คุณมักจะรู้สึกว่าถูกครอบงำด้วยสิ่งต่าง ๆ ได้ง่าย",
    "คุณทำสิ่งต่าง ๆ อย่างเป็นขั้นตอน โดยไม่ข้ามลำดับใด ๆ",
    "คุณชอบงานที่ต้องใช้ความคิดสร้างสรรค์มากกว่างานที่ต้องทำตามขั้นตอนที่ชัดเจน",
    "คุณมักจะพึ่งพาความรู้สึกภายในมากกว่าเหตุผลเชิงตรรกะเมื่อต้องตัดสินใจ",
    "คุณมักจะมีปัญหากับการทำงานให้ทันตามกำหนดเวลา",
    "คุณมั่นใจว่าสุดท้ายแล้วทุกอย่างจะออกมาดี"
]

# Configuration
NUM_QUESTIONS = 60
CHOICES = list(range(-3, 4))  # -3, -2, -1, 0, 1, 2, 3
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "responses.csv")


# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
#HTML for ENFJ page


# HTML template (single-file app uses render_template_string for simplicity)
TEMPLATE = '''
<!doctype html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>🧭 แบบทดสอบบุคลิกภาพ</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: "Noto Sans Thai", sans-serif;
      background: linear-gradient(135deg, #f4f7f6, #faf5ff);
      color: #333;
      padding: 30px;
      max-width: 900px;
      margin: auto;
      animation: fadeIn 0.8s ease;
    }

    @keyframes fadeIn {
      from {opacity: 0; transform: translateY(10px);}
      to {opacity: 1; transform: translateY(0);}
    }

    h1 {
      text-align: center;
      background: linear-gradient(135deg, #6b4fa0, #3ba776);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-size: 2.4rem;
      margin-bottom: 40px;
      font-weight: 800;
    }

    /* Progress Bar */
    .progress-container {
      background: #e7ebea;
      border-radius: 30px;
      height: 12px;
      width: 100%;
      margin-bottom: 25px;
      overflow: hidden;
    }

    .progress-bar {
      height: 100%;
      background: linear-gradient(90deg, #6b4fa0, #3ba776);
      width: 0%;
      transition: width 0.4s ease;
    }

    .question-block {
      background: #fff;
      border-radius: 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      padding: 25px 30px;
      margin-bottom: 25px;
      transition: all 0.3s ease;
    }

    .question-block:hover {
      transform: translateY(-4px);
      box-shadow: 0 6px 14px rgba(0,0,0,0.1);
    }

    .question p {
      font-weight: 600;
      font-size: 1.2rem;
      margin-bottom: 15px;
    }

    .scale {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
    }

    .choices {
      display: flex;
      justify-content: center;
      gap: 25px;
      flex: 1;
      padding: 0 15px;
    }

    input[type="radio"] {
      appearance: none;
      width: 22px;
      height: 22px;
      border: 2px solid #ccc;
      border-radius: 50%;
      cursor: pointer;
      transition: all 0.25s ease;
      position: relative;
    }

    input[type="radio"]:hover {
      border-color: #6b4fa0;
      transform: scale(1.2);
    }

    input[type="radio"]:checked {
      border-color: #3ba776;
      background: radial-gradient(circle at center, #3ba776 50%, transparent 50%);
      transform: scale(1.3);
    }

    .left-label, .right-label {
      font-weight: 600;
      min-width: 90px;
      text-align: center;
      font-size: 0.95rem;
    }

    .left-label { color: #7c4d9f; }
    .right-label { color: #2ca45c; }

    /* Input & Button */
    .submit-block {
      text-align: center;
      margin-top: 45px;
    }

    input[type="text"] {
      padding: 12px 16px;
      font-size: 1rem;
      border-radius: 10px;
      border: 1px solid #ccc;
      width: 260px;
      transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }

    input[type="text"]:focus {
      border-color: #3ba776;
      box-shadow: 0 0 6px rgba(59,167,118,0.4);
      outline: none;
    }

    button {
      background: linear-gradient(135deg, #3ba776, #2c8e63);
      color: white;
      border: none;
      padding: 12px 28px;
      font-size: 1rem;
      border-radius: 12px;
      cursor: pointer;
      margin-left: 12px;
      box-shadow: 0 3px 8px rgba(59,167,118,0.3);
      transition: all 0.3s ease;
    }

    button:hover {
      background: linear-gradient(135deg, #2c8e63, #3ba776);
      box-shadow: 0 5px 12px rgba(59,167,118,0.4);
      transform: translateY(-2px);
    }

    /* Result */
    .result {
      background: #ffffffcc;
      border-radius: 16px;
      box-shadow: 0 3px 10px rgba(0,0,0,0.07);
      padding: 25px 30px;
      margin-top: 50px;
      line-height: 1.6;
      animation: fadeIn 0.8s ease;
    }

    .result h2 {
      text-align: center;
      color: #3ba776;
      margin-bottom: 15px;
    }

    .emoji {
      font-size: 2rem;
      text-align: center;
      margin-bottom: 10px;
    }

  </style>
</head>
<body>
  <h1>🧭 แบบทดสอบบุคลิกภาพ</h1>

  <div class="progress-container">
    <div class="progress-bar" id="progress-bar"></div>
  </div>

  <form method="post" action="{{ url_for('submit') }}" id="quizForm">
    {% for i in range(1, num_questions + 1) %}
      <div class="question-block">
        <div class="question">
          <p>ข้อ {{ i }}. {{ questions[i-1] }}</p>
        </div>

        <div class="scale">
          <span class="left-label">ไม่เห็นด้วย</span>
          <div class="choices">
            {% for c in choices %}
              <label>
                <input type="radio" name="q{{ i }}" value="{{ c }}" {% if c == 0 %}checked{% endif %}>
              </label>
            {% endfor %}
          </div>
          <span class="right-label">เห็นด้วย</span>
        </div>
      </div>
    {% endfor %}

    <div class="submit-block">
      <input type="text" name="participant" placeholder="ชื่อผู้ตอบ" required>
      <button type="submit">ส่งแบบสอบถาม</button>
    </div>
  </form>

  {% if result %}
    <div class="result">
      <div class="emoji">🌿</div>
      <h2>ผลลัพธ์</h2>
      <p><strong>รวมคะแนน:</strong> {{ total }}</p>
      <p><strong>คะแนนเฉลี่ย:</strong> {{ average }}</p>
      <p><strong>คำตอบแยกข้อ:</strong></p>
      <ol>
        {% for ans in answers %}
          <li>{{ ans }}</li>
        {% endfor %}
      </ol>
    </div>
  {% endif %}

  <script>
    // อัปเดต progress bar
    const form = document.getElementById('quizForm');
    const radios = form.querySelectorAll('input[type="radio"]');
    const progressBar = document.getElementById('progress-bar');
    const totalQuestions = {{ num_questions }};
    const answered = new Set();

    radios.forEach(radio => {
      radio.addEventListener('change', () => {
        answered.add(radio.name);
        let progress = (answered.size / totalQuestions) * 100;
        progressBar.style.width = progress + "%";
      });
    });
  </script>
</body>
</html>

'''

@app.route('/cosine_summary', methods=['POST'])
def cosine_summary():
    data = request.form.get('cosine_dict', '{}')
    cosine_dict = json.loads(data)
    return render_template('cosine_summary.html', cosine_dict=cosine_dict)

@app.route('/', methods=['GET'])
def index():
    return render_template_string(
        TEMPLATE,
        num_questions=NUM_QUESTIONS,
        choices=CHOICES,
        result=None,
        questions=question   # ✅ เพิ่มบรรทัดนี้
    )

@app.route('/<mbti>')
def show_mbti_page(mbti):
    mbti = mbti.upper()  
    if mbti not in MBTI_AVG:  
        return "หน้าไม่พบ", 404
    user_name = session.get('user_name',{})
    cosine_dict = session.get('cosine_dict', {})
    
    # ส่งไป template
    return render_template(f'{mbti}.html', mbti=mbti, cosine_dict=cosine_dict,user_name=user_name)

@app.route('/submit', methods=['POST'])
def submit():
    # Collect answers
    answers = []
    for i in range(1, NUM_QUESTIONS + 1):
        key = f"q{i}"
        val = request.form.get(key, None)
        try:
            # If value missing, treat as 0
            v = int(val) if val is not None else 0
        except ValueError:
            v = 0
        # sanitize: ensure within allowed choices
        if v not in CHOICES:
            v = 0
        answers.append(v)

    participant = request.form.get('participant', '').strip()
    timestamp = datetime.utcnow().isoformat()

    

    # Save to CSV
    header = ["timestamp", "participant"] + [f"q{i}" for i in range(1, NUM_QUESTIONS + 1)] + ["total", "average"]
    
    cosine_dict = {
    "ENFJ": 0, "ENFP": 0, "ENTJ": 0, "ENTP": 0,
    "ESFJ": 0, "ESFP": 0, "ESTJ": 0, "ESTP": 0,
    "INFJ": 0, "INFP": 0, "INTJ": 0, "INTP": 0,
    "ISFJ": 0, "ISFP": 0, "ISTJ": 0, "ISTP": 0
    }


    # ตัวอย่างคำตอบของ person2

    # คำนวณ Cosine similarity
    for mbti, data in MBTI_AVG.items():
        if data:
            dot_product = sum(a*b for a, b in zip(data, answers))
            norm1 = math.sqrt(sum(a**2 for a in data))
            norm2 = math.sqrt(sum(b**2 for b in answers))
            cosine = dot_product / (norm1 * norm2)
            cosine_dict[mbti] = cosine  # เก็บลง dictionary

    # หา MBTI ที่ Cosine similarity สูงสุด
    best_mbti = max(cosine_dict, key=cosine_dict.get)
    best_score = cosine_dict[best_mbti]

        
    session['user_name'] = participant
    session['cosine_dict'] = cosine_dict  # เก็บไว้ใน session
    return redirect(url_for('show_mbti_page', mbti=best_mbti))
@app.route('/download', methods=['GET'])
def download_csv():
    if not os.path.exists(CSV_FILE):
        flash("ยังไม่มีผลลัพธ์ให้ดาวน์โหลด")
        return redirect(url_for('index'))
    return send_file(CSV_FILE, as_attachment=True, download_name='responses.csv')


if __name__ == '__main__':
    # Development server
    # For production, run with gunicorn: gunicorn -w 4 -b 0.0.0.0:8000 survey_app:app
    app.run(host='0.0.0.0', port=5000, debug=True)