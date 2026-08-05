import pyodbc


# --------- SQL Bağlantısı ----------
server = 'localhost'
database = 'EnglishLearningDB'

conn_str = (
        "DRIVER=ODBC Driver 18 for SQL SERVER;"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
)
# --------------------------------
def get_connection():
    try:
        return pyodbc.connect(conn_str)
    except Exception as Hata:
        print(f"Veritabanı Bağlantı Hatası Aldınız: {Hata}")
        return None
    
# ------------------------------------
# Soru Üretimi İçin Kelime Getir
# ------------------------------------
def get_words_without_enrichment():
    """Henüz sorusu üretilmemiş (Questions tablosunda olmayan) kelimeleri getirir."""
    conn = get_connection()

    if conn is None:
        return []
        
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"""
            SELECT 
                Word
            FROM Vocabulary
            WHERE Word NOT IN (SELECT Word FROM Questions)
            ORDER BY NEWID()
            """ 
        )
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    except Exception as Hata:
        print(f"Kelime Getirilemedi -> Hata: {Hata}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn: 
            conn.close()
            
# ------------------------------------
# LLM'den Gelen Soruyu SQL'e yaz
# ------------------------------------
def insert_quiz_question(
        word,
        question_text,
        option_a,
        option_b,
        option_c,
        option_d,
        correct_answer,
        explanation
):
    conn = None
    cursor = None

    try:
        conn = get_connection()
            
        if conn is None:
            return False

        cursor = conn.cursor()
            
        cursor.execute("""
            INSERT INTO Questions
            (
                Word,
                QuestionText,
                OptionA,
                OptionB,
                OptionC,
                OptionD,
                CorrectAnswer,
                Explanation                                             
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                word,
                question_text,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer,
                explanation
            )
        )
        print(f"✅ {word} için soru eklendi. ")
        conn.commit()
        return True

    except Exception as Hata:
        print(f"🚨 {word} için soru eklenemedi. {Hata}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()







        