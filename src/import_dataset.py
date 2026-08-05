import pandas as pd
from database import get_connection
# --------------------------------

normal = pd.read_csv('../data/dataset1.csv')
translated = pd.read_csv('../data/dataset2.csv')



# -------- KELİME YÜKLEME ------------
def vocabulary_insert(normal):
    connection = None
    cursor = None

    insert_count = 0
    skip_count = 0

    try:
        connection = get_connection()
        if connection is None:
            print("Bağlantı Başarısız.")
            return

        print("Bağlantı Başarılı.")
        cursor = connection.cursor()

        for index, row in normal.iterrows():

            word = row['word'].strip().lower()
            meaning_tr = row['meaning_tr']                       
            example_sentence = row['example_sentence']            
            definition_en = row['definition_en']

            print("Aranan Kelime:", word)

            cursor.execute("""
                SELECT word
                FROM Vocabulary
                WHERE word = ?    
            """, 
            (word,)
            )
            result = cursor.fetchone()
            print("Bulunan:", result)

            if result:
                    
                f"{word} zaten mevcut"
                skip_count += 1
                
            else:

                cursor.execute(
                    """
                    INSERT INTO Vocabulary
                    (
                        Word,
                        Meaning,                                       
                        ExampleSentence,                    
                        DefinitionEN                                         
                    )            
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        word,
                        meaning_tr, 
                        example_sentence,                      
                        definition_en                                                              
                    )
                )                
                    
                print(f"{word} Eklendi")
                insert_count += 1

            connection.commit()
            print("---------------------------------")
            print("Tüm Kelimeler Başarıyla Kaydedildi.")
            print(f"Eklenen Kelime Sayısı: {insert_count}")
            print(f"Atlanan Kelime Sayısı: {skip_count}")

    except Exception as Hata:
        print(f"Database Hatası: {Hata}")
    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ----- KELİME GÜNCELLEME -------------
def update_translation(translated):
    connection = None
    cursor = None
    update_count = 0

    try:
        connection = get_connection()
        cursor = connection.cursor()

        for index, row in translated.iterrows():

            word = row['word'].strip().lower()
            example_translation = row['example_translation']
            
            cursor.execute(
                """
                UPDATE Vocabulary
                SET ExampleTranslation = ?
                WHERE LOWER(Word) = ?
                """,
                (
                    example_translation , 
                    word
                                    
                )
            )

            print(f"{word} Çevirisi Güncellendi.")
            update_count += 1

            connection.commit()
            print("------------------------")
            print("KElime Çeviri Güncellemesi Tamamlandı.")
            print(f"Güncellenen Kelime Sayısı: {update_count}")
            print(translated.head(10))
            print(translated.columns)
            print(len(translated))

    except Exception as Hata:
        print(f"Çeviri Hatası: {Hata}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

