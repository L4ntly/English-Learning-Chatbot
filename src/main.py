from database import get_words_without_enrichment, insert_quiz_question
from llm import generate_quiz_question
import time


# ------------------------------
def main():
    print("🚀 Sistem Başlatılıyor.")
    get_words = get_words_without_enrichment()
    toplam_quiz = len(get_words)

    if toplam_quiz == 0:
        print("✅ Harika! Soru üretilecek yeni kelime bulunamadı. Veritabanın tamamen güncel.")
        return

    
    print(f"\n--- {toplam_quiz} KELİME İÇİN QUİZ ÜRETİMİ BAŞLIYOR ---")

    for islenen_sayi, word in enumerate(get_words, start=1):
        kalan_quiz = toplam_quiz - islenen_sayi
        print("-----------------------")
        print(f"[{islenen_sayi}/{toplam_quiz}] 🚀 '{word}' için soru üretiliyor... (Kalan: {kalan_quiz})")

        # LLM'den soruyu alır
        gonder = generate_quiz_question(word)

        if gonder is None:
            print(f"⚠️ Model cevap veremedi veya JSON ayıklanamadı. '{word} atlanıyor...")
            continue    

        gerekli_anahtarlar = [
            'question_text', 
            'option_a', 
            'option_b', 
            'option_c', 
            'option_d', 
            'correct_answer', 
            'explanation'
        ]

        eksik_var_mi = False

        for anahtar in gerekli_anahtarlar:
            if anahtar not in gonder:
                print(f"⚠️ Model '{anahtar} üretmedi. {word} atlanıyor...")
                eksik_var_mi = True
                break
        if eksik_var_mi:
            continue

        question_text = gonder['question_text']
        option_a = gonder['option_a']
        option_b = gonder['option_b']
        option_c = gonder['option_c']
        option_d = gonder['option_d']
        correct_answer = gonder['correct_answer']
        explanation = gonder['explanation']

        quiz_words = insert_quiz_question(
                word,
                question_text,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer,
                explanation                    
        )
        if quiz_words:
            print("📝 --- Üretilen Soru ---")
            print(f"Soru: {question_text}")
            print(f"A) {option_a}")
            print(f"B) {option_b}")
            print(f"C) {option_c}")
            print(f"D) {option_d}")
            print(f"Doğru Cevap: {correct_answer}")
            print(f"Açıklama: {explanation}")
            print(f"✅ {word} Veritabanına Başarıyla Eklendi!\n")

        else:
            print(f"🚨 DİKKAT: {word} için soru üretildi AMA veritabanına KAYDEDİLEMEDİ!")

        time.sleep(1)

                
# --------------------------------
if __name__ == "__main__":
   main()



