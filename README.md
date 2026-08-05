# English Learning LLM Project 
A comprehensive, AI-powered personal English learning assistant and chatbot. My goal in creating this project is to expose myself to the English language and achieve my desired IELTS/TOEFL scores. It utilizes a native Large Language Model (Llama 3.2 via Ollama) to create dynamic vocabulary tests and provides an interactive web interface using Streamlit; all supported by a robust SQL Server database. I initially tested it by loading 1000 advanced words. Also you can ask proverbs, idioms, phrases, slangs, etc.

## Phase 1 - Import Core Vocabulary

**Objective** 
- Import the core vocabulary dataset into the SQL Server database to establish the foundation of the learning application.


**Dataset**
- dataset1.csv


**Columns**
- 'word'
- 'meaning_tr'
- 'definition_en'
- 'example_sentence'


**Tasks** 
- Read CSV data utilizing Pandas
- Validate required columns and data integrity.
- Check for duplicate words before insertion.
- Insert validated data into the 'Vocabulary' SQL table.


**Status**
- ✅ Done


## Phase 2 - Import Example Translations

**Objective** 
- Enrich the existing vocabulary with Turkish example sentence translations


**Dataset**
- 'dataset2.csv'


**Columns** 
- 'word'
- 'example_translation'


**Tasks** +
- Read the secondary dataset.
- Match new translations to existing records by the 'word' colum.
- Update the 'example_translation' column in the database.


**Status** 
- ✅ Done

---


## Phase 3 - Automatic Quiz Generation

**Objective**
- Generate interactive, context-aware fill-in-the-blank vocabulary quizzes automatically using a local Ollama API.(without api key)


**Generate** 
- Unique sentence questions (with target words replaced by blanks).
- Four MCQ options (one correct, three real-word distractors).
- Correct answer identification.
- Brief, impressive explanation of the word's core nuance.


**Database** 
- Parse LLM JSON responses and store them into the 'Questions' table.


**Status**
- ✅ Done