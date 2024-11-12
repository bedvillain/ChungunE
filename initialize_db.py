import sqlite3
import json

# 데이터베이스 초기화 함수
def initialize_db():
    # JSON 파일 로드
    with open('data/school_info.json', 'r', encoding='utf-8') as f:
        school_data = json.load(f)
    
    conn = sqlite3.connect('data/school_info.db')
    cursor = conn.cursor()

    # schools 테이블 생성
    cursor.execute('''CREATE TABLE IF NOT EXISTS schools (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        address TEXT,
                        principal TEXT,
                        vice_principal TEXT,
                        kind TEXT
                      )''')

    # events 테이블 생성
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY,
                        school_id INTEGER,
                        date DATE,
                        event TEXT,
                        FOREIGN KEY (school_id) REFERENCES schools(id)
                      )''')

    # grade_2 테이블 생성 (2학년 학급 정보)
    cursor.execute('''CREATE TABLE IF NOT EXISTS grade_2 (
                        id INTEGER PRIMARY KEY,
                        class TEXT,
                        teacher TEXT,
                        T_subject TEXT,
                        T_description TEXT
                      )''')

    # JSON 데이터 삽입 (schools 테이블)
    school_info = school_data["schools"]
    cursor.execute('''INSERT OR IGNORE INTO schools (id, name, address, principal, vice_principal, kind)
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                   (1, school_info["name"], school_info["address"], school_info["principal"], school_info["vice_principal"], school_info["kind"]))

    # JSON 데이터 삽입 (events 테이블)
    for event in school_data["events"]:
        cursor.execute('''INSERT INTO events (school_id, date, event) VALUES (?, ?, ?)''', 
                       (1, event["date"], event["event"]))

    # JSON 데이터 삽입 (grade_2 테이블)
    for class_info in school_data["2_grade"]:
        cursor.execute('''INSERT INTO grade_2 (class, teacher, T_subject, T_description) VALUES (?, ?, ?, ?)''', 
                       (class_info["class"], class_info["teacher"], class_info["T_subject"], class_info["T_description"]))

    conn.commit()
    conn.close()

# 데이터베이스 초기화 실행
initialize_db()
