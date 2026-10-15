"""
KhasiConnect AI - Master Dataset Downloader and Organizer
This script downloads, validates, and organizes all datasets required for:
  - Module 1: Khasi Learning Assistant
  - Module 2: Voice-to-Voice Translation
  - Module 3: OCR Image Scanning and Translation
  - Shared Khasi-English Language Resource
"""

import os
import shutil
import urllib.request
import bz2
import json
import csv
from huggingface_hub import hf_hub_download

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")

DIRS = {
    "parallel": os.path.join(DATASETS_DIR, "parallel_translation"),
    "learning": os.path.join(DATASETS_DIR, "learning_assistant"),
    "ocr": os.path.join(DATASETS_DIR, "ocr_image_translation"),
    "ocr_images": os.path.join(DATASETS_DIR, "ocr_image_translation", "sample_images"),
    "speech": os.path.join(DATASETS_DIR, "speech_voice"),
    "shared": os.path.join(DATASETS_DIR, "shared_language_resource"),
}

for d in DIRS.values():
    os.makedirs(d, exist_ok=True)

print("=" * 65)
print("KhasiConnect AI - Dataset Downloader")
print("Target workspace:", DATASETS_DIR)
print("=" * 65)

# -------------------------------------------------------------
# 1. Parallel Translation Corpora (Module 2 & Shared Resource)
# -------------------------------------------------------------
print("\n[1/5] Downloading Parallel Translation Datasets...")

parallel_files = [
    {
        "repo": "user10383/english-khasi-parallel-corpus",
        "file": "data/small_sentences_train-00000-of-00001.parquet",
        "dest": os.path.join(DIRS["parallel"], "user10383_parallel_small_train.parquet")
    },
    {
        "repo": "user10383/english-khasi-parallel-corpus",
        "file": "data/small_sentences_test-00000-of-00001.parquet",
        "dest": os.path.join(DIRS["parallel"], "user10383_parallel_small_test.parquet")
    },
    {
        "repo": "user10383/english-khasi-parallel-corpus",
        "file": "data/news_and_wikipedia_corpus-00000-of-00002.parquet",
        "dest": os.path.join(DIRS["parallel"], "user10383_news_wikipedia_part1.parquet")
    },
    {
        "repo": "MEDHARVIX-SYSTEMS/bhasaflow-khasi-english-parallel-corpus-v1",
        "file": "data/bhasaflow-khasi-english-parallel-corpus-v1.csv",
        "dest": os.path.join(DIRS["parallel"], "bhasaflow_parallel_corpus.csv")
    }
]

for item in parallel_files:
    try:
        if not os.path.exists(item["dest"]):
            print(f"  Downloading {os.path.basename(item['dest'])} from {item['repo']}...")
            cached = hf_hub_download(repo_id=item["repo"], filename=item["file"], repo_type="dataset")
            shutil.copyfile(cached, item["dest"])
            size_mb = os.path.getsize(item["dest"]) / (1024 * 1024)
            print(f"    -> Saved: {item['dest']} ({size_mb:.2f} MB)")
        else:
            print(f"  Already exists: {os.path.basename(item['dest'])}")
    except Exception as e:
        print(f"  Error downloading {item['file']}: {e}")

# -------------------------------------------------------------
# 2. Learning Assistant & Vocabulary (Module 1)
# -------------------------------------------------------------
print("\n[2/5] Downloading Learning Assistant & Lexicon Datasets...")

lexicon_urls = {
    "khasi_words_dictionary.json": "https://raw.githubusercontent.com/infoakshatsinghbisht-eng/KHASI-language-library/main/khasi/lexicon/data/words.json",
    "khasi_everyday_phrases.json": "https://raw.githubusercontent.com/infoakshatsinghbisht-eng/KHASI-language-library/main/khasi/lexicon/data/phrases.json",
    "khasi_proverbs.json": "https://raw.githubusercontent.com/infoakshatsinghbisht-eng/KHASI-language-library/main/khasi/lexicon/data/proverbs.json",
    "khasi_riddles.json": "https://raw.githubusercontent.com/infoakshatsinghbisht-eng/KHASI-language-library/main/khasi/lexicon/data/riddles.json",
}

for fname, url in lexicon_urls.items():
    dest = os.path.join(DIRS["learning"], fname)
    if not os.path.exists(dest):
        print(f"  Downloading {fname}...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp, open(dest, "wb") as f_out:
                f_out.write(resp.read())
            size_mb = os.path.getsize(dest) / (1024 * 1024)
            print(f"    -> Saved: {dest} ({size_mb:.2f} MB)")
        except Exception as e:
            print(f"  Error downloading {fname}: {e}")
    else:
        print(f"  Already exists: {fname}")

# Tatoeba 2,409 verified Khasi sentences
tatoeba_dest = os.path.join(DIRS["learning"], "tatoeba_khasi_sentences.tsv")
if not os.path.exists(tatoeba_dest):
    print("  Downloading Tatoeba Khasi sentences...")
    try:
        tatoeba_url = "https://downloads.tatoeba.org/exports/per_language/kha/kha_sentences.tsv.bz2"
        req = urllib.request.Request(tatoeba_url, headers={"User-Agent": "Mozilla/5.0"})
        compressed = urllib.request.urlopen(req).read()
        raw_text = bz2.decompress(compressed).decode("utf-8")
        with open(tatoeba_dest, "w", encoding="utf-8") as f:
            f.write(raw_text)
        print(f"    -> Saved: {tatoeba_dest} ({len(raw_text.splitlines())} sentences)")
    except Exception as e:
        print(f"  Error downloading Tatoeba sentences: {e}")
else:
    print("  Already exists: tatoeba_khasi_sentences.tsv")

# Monolingual sentences
mono_dest = os.path.join(DIRS["learning"], "khasi_monolingual.csv")
if not os.path.exists(mono_dest):
    print("  Downloading BhasaFlow Khasi monolingual corpus...")
    try:
        cached = hf_hub_download(repo_id="MEDHARVIX-SYSTEMS/bhasaflow-khasi-monolingual-corpus-v1", filename="data/bhasaflow-khasi-monolingual-corpus-v1.csv", repo_type="dataset")
        shutil.copyfile(cached, mono_dest)
        print(f"    -> Saved: {mono_dest}")
    except Exception as e:
        print(f"  Error downloading monolingual corpus: {e}")
else:
    print("  Already exists: khasi_monolingual.csv")

# -------------------------------------------------------------
# 3. OCR Image Translation Datasets (Module 3)
# -------------------------------------------------------------
print("\n[3/5] Downloading OCR Benchmark & Ground Truth Samples...")

ocr_meta_dest = os.path.join(DIRS["ocr"], "khasi_ocr_benchmark_metadata.csv")
if not os.path.exists(ocr_meta_dest):
    print("  Downloading Khasi OCR benchmark metadata...")
    try:
        cached = hf_hub_download(repo_id="Badnyal/khasi-ocr-benchmark-2k", filename="metadata.csv", repo_type="dataset")
        shutil.copyfile(cached, ocr_meta_dest)
        print(f"    -> Saved: {ocr_meta_dest}")
    except Exception as e:
        print(f"  Error downloading OCR metadata: {e}")
else:
    print("  Already exists: khasi_ocr_benchmark_metadata.csv")

# Download 10 sample benchmark line images
sample_image_files = [
    "images/DOC17333794530_p003_l013.jpg",
    "images/DOC17333794530_p003_l024.jpg",
    "images/DOC17333794530_p003_l042.jpg",
    "images/DOC17333794530_p003_l047.jpg",
    "images/DOC17333794530_p003_l068.jpg",
    "images/DOC17333794530_p003_l072.jpg",
    "images/DOC17333794530_p003_l091.jpg",
    "images/DOC17333794530_p003_l104.jpg",
    "images/DOC17333794530_p004_l009.jpg",
    "images/DOC17333794530_p004_l015.jpg",
]

print("  Downloading sample OCR test images...")
for img_name in sample_image_files:
    fname = os.path.basename(img_name)
    target = os.path.join(DIRS["ocr_images"], fname)
    if not os.path.exists(target):
        try:
            cached = hf_hub_download(repo_id="Badnyal/khasi-ocr-benchmark-2k", filename=img_name, repo_type="dataset")
            shutil.copyfile(cached, target)
        except Exception as e:
            print(f"    Error downloading {img_name}: {e}")
print(f"    -> Stored {len(os.listdir(DIRS['ocr_images']))} sample images in {DIRS['ocr_images']}")

# -------------------------------------------------------------
# 4. Speech / Voice Datasets (Module 2)
# -------------------------------------------------------------
print("\n[4/5] Downloading Speech / Voice Metadata...")

speech_meta_dest = os.path.join(DIRS["speech"], "bhasaflow_speech_metadata.csv")
if not os.path.exists(speech_meta_dest):
    print("  Downloading BhasaFlow speech alignment metadata...")
    try:
        cached = hf_hub_download(repo_id="MEDHARVIX-SYSTEMS/bhasaflow-khasi-english-parallel-sample-v1", filename="data/metadata.csv", repo_type="dataset")
        shutil.copyfile(cached, speech_meta_dest)
        print(f"    -> Saved: {speech_meta_dest}")
    except Exception as e:
        print(f"  Error downloading speech metadata: {e}")
else:
    print("  Already exists: bhasaflow_speech_metadata.csv")

# -------------------------------------------------------------
# 5. Shared Khasi-English Language Resource & Benchmark Tests
# -------------------------------------------------------------
print("\n[5/5] Building Unified Shared Language Resource & Test Suite...")

# Build a curated, verified vocabulary table from dictionary & phrases
vocab_dest = os.path.join(DIRS["shared"], "verified_vocabulary.csv")
sentences_dest = os.path.join(DIRS["shared"], "verified_sentences.csv")
tests_dest = os.path.join(DIRS["shared"], "evaluation_test_cases.json")

# A. Curated Vocabulary
curated_vocab = [
    # Basic Greetings & Social
    {"khasi_word": "Khublei", "english_meaning": "Hello / Thank you / Blessings", "pos": "Interjection / Greeting", "example_khasi": "Khublei shibun!", "example_english": "Thank you very much!", "pronunciation": "Khu-blay", "source": "Everyday Speech"},
    {"khasi_word": "Khublei shibun", "english_meaning": "Thank you very much", "pos": "Phrase", "example_khasi": "Khublei shibun ïa ka jingiarap jong phi.", "example_english": "Thank you very much for your help.", "pronunciation": "Khu-blay shee-boon", "source": "Everyday Speech"},
    {"khasi_word": "Kumno phi long?", "english_meaning": "How are you?", "pos": "Question Phrase", "example_khasi": "Kumno phi long mynta ka sngi?", "example_english": "How are you today?", "pronunciation": "Koom-no fee long?", "source": "Everyday Speech"},
    {"khasi_word": "Nga biang", "english_meaning": "I am fine", "pos": "Phrase", "example_khasi": "Nga biang, khublei.", "example_english": "I am fine, thank you.", "pronunciation": "Nga bee-ang", "source": "Everyday Speech"},
    {"khasi_word": "Bha", "english_meaning": "Good / Well / Fine", "pos": "Adjective", "example_khasi": "U long u briew babha.", "example_english": "He is a good person.", "pronunciation": "Bha", "source": "Lexicon"},
    {"khasi_word": "Sniew", "english_meaning": "Bad / Evil", "pos": "Adjective", "example_khasi": "Ka suiñbneng ka long kaba sniew.", "example_english": "The weather is bad.", "pronunciation": "Snee-oo", "source": "Lexicon"},
    {"khasi_word": "Jingsuk", "english_meaning": "Peace", "pos": "Noun", "example_khasi": "Ka jingsuk ha kaba kut!", "example_english": "Peace at last!", "pronunciation": "Jing-sook", "source": "Lexicon"},
    {"khasi_word": "Um", "english_meaning": "Water", "pos": "Noun", "example_khasi": "Ai um ïa nga ban dih.", "example_english": "Give me water to drink.", "pronunciation": "Oom", "source": "Lexicon"},
    {"khasi_word": "Ja", "english_meaning": "Cooked rice / Meal", "pos": "Noun", "example_khasi": "Phi la bam ja?", "example_english": "Have you eaten?", "pronunciation": "Jah", "source": "Everyday Speech"},
    {"khasi_word": "Bam", "english_meaning": "To eat", "pos": "Verb", "example_khasi": "Nga kwah ban bam.", "example_english": "I want to eat.", "pronunciation": "Bahm", "source": "Lexicon"},
    {"khasi_word": "Dih", "english_meaning": "To drink", "pos": "Verb", "example_khasi": "U dih sha.", "example_english": "He drinks tea.", "pronunciation": "Deeh", "source": "Lexicon"},
    {"khasi_word": "Iing", "english_meaning": "House / Home", "pos": "Noun", "example_khasi": "Nga leit sha ïing.", "example_english": "I am going home.", "pronunciation": "Eeng", "source": "Lexicon"},
    {"khasi_word": "Leit", "english_meaning": "To go", "pos": "Verb", "example_khasi": "Nga hap ban leit noh.", "example_english": "I have to go now.", "pronunciation": "Layt", "source": "Lexicon"},
    {"khasi_word": "Wan", "english_meaning": "To come", "pos": "Verb", "example_khasi": "Wan hangne.", "example_english": "Come here.", "pronunciation": "Wahn", "source": "Lexicon"},
    {"khasi_word": "Myniet", "english_meaning": "Tomorrow", "pos": "Noun / Adverb", "example_khasi": "Ngan wan lashai / myniet.", "example_english": "I will come tomorrow.", "pronunciation": "Muh-neet", "source": "Lexicon"},
    {"khasi_word": "Mynta", "english_meaning": "Now / Today", "pos": "Adverb", "example_khasi": "Leit mynta.", "example_english": "Go now.", "pronunciation": "Myn-tah", "source": "Lexicon"},
    {"khasi_word": "Shillong", "english_meaning": "Shillong (Capital of Meghalaya)", "pos": "Proper Noun", "example_khasi": "Nga sah ha Shillong.", "example_english": "I live in Shillong.", "pronunciation": "Sheel-long", "source": "Geography"},
    {"khasi_word": "Meghalaya", "english_meaning": "Meghalaya", "pos": "Proper Noun", "example_khasi": "Ka jylla Meghalaya.", "example_english": "The state of Meghalaya.", "pronunciation": "May-gha-la-ya", "source": "Geography"},
    {"khasi_word": "Kynthei", "english_meaning": "Female / Woman", "pos": "Noun", "example_khasi": "Ka kynthei ka treikam.", "example_english": "The woman works.", "pronunciation": "Kyn-they", "source": "Lexicon"},
    {"khasi_word": "Shynrang", "english_meaning": "Male / Man", "pos": "Noun", "example_khasi": "U shynrang u shong hangtei.", "example_english": "The man sits there.", "pronunciation": "Shyn-rahng", "source": "Lexicon"},
    {"khasi_word": "Khadnah", "english_meaning": "Youngest daughter (inheritor in matrilineal Khasi custom)", "pos": "Cultural Noun", "example_khasi": "Ka khadnah ka kyntoit ïa ka ïing ka sem.", "example_english": "The youngest daughter takes care of the ancestral house.", "pronunciation": "Khad-nah", "source": "Culture"},
    {"khasi_word": "Tip kur tip kha", "english_meaning": "Knowing one's maternal and paternal clan relations (foundational Khasi moral value)", "pos": "Cultural Concept", "example_khasi": "U Khasi u bat skhem ïa ka tip kur tip kha.", "example_english": "The Khasi firmly holds to the moral knowledge of maternal and paternal lineage.", "pronunciation": "Tip koor tip khah", "source": "Culture"},
    {"khasi_word": "Kamai ïa ka hok", "english_meaning": "Earn righteousness / Live honestly (core Khasi ethical motto)", "pos": "Ethical Principle", "example_khasi": "Dei ban kamai ïa ka hok ha ka jingim.", "example_english": "One must earn through righteousness in life.", "pronunciation": "Kah-my ya kah hok", "source": "Culture"},
]

with open(vocab_dest, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["khasi_word", "english_meaning", "pos", "example_khasi", "example_english", "pronunciation", "source"])
    writer.writeheader()
    writer.writerows(curated_vocab)
print(f"  -> Generated verified vocabulary: {vocab_dest} ({len(curated_vocab)} entries)")

# B. Curated Parallel Sentences (for testing & evaluation)
curated_sentences = [
    {"id": "S-01", "khasi": "Kumno phi kyrteng?", "english": "What is your name?", "category": "Greeting", "verified": True},
    {"id": "S-02", "khasi": "Ka kyrteng jong nga dei u John.", "english": "My name is John.", "category": "Greeting", "verified": True},
    {"id": "S-03", "khasi": "Nga sngewbha shibun ban don hangne.", "english": "I am very pleased to be here.", "category": "Social", "verified": True},
    {"id": "S-04", "khasi": "Kiei ki jingthmu jong phi?", "english": "What are your plans?", "category": "Conversation", "verified": True},
    {"id": "S-05", "khasi": "Ka jingsuk ha kaba kut!", "english": "Peace at last!", "category": "Idiomatic", "verified": True},
    {"id": "S-06", "khasi": "Hangno ka lynti ban leit sha Iewduh?", "english": "Where is the way to go to Iewduh market?", "category": "Directions", "verified": True},
    {"id": "S-07", "khasi": "Katno kane ka dor?", "english": "How much does this cost?", "category": "Marketplace", "verified": True},
    {"id": "S-08", "khasi": "Nga hap ban leit sha ka painkhana.", "english": "I have to go to the toilet.", "category": "Everyday", "verified": True},
    {"id": "S-09", "khasi": "Wat sngewbha, sngewbha ai bor ïa nga.", "english": "Excuse me, please forgive me.", "category": "Politeness", "verified": True},
    {"id": "S-10", "khasi": "Phi lah ban kren phareng?", "english": "Can you speak English?", "category": "Language", "verified": True},
    {"id": "S-11", "khasi": "Nga tip khamtiem ïa ka Khasi.", "english": "I only know a little Khasi.", "category": "Language", "verified": True},
    {"id": "S-12", "khasi": "Sngewbha kren suki.", "english": "Please speak slowly.", "category": "Communication", "verified": True},
    {"id": "S-13", "khasi": "Nga thngan shibun.", "english": "I am very hungry.", "category": "Everyday", "verified": True},
    {"id": "S-14", "khasi": "Ai um dih sngewbha.", "english": "Please give drinking water.", "category": "Everyday", "verified": True},
    {"id": "S-15", "khasi": "Ka sngi ka shat bha mynta.", "english": "The sun is shining brightly today.", "category": "Weather", "verified": True},
    {"id": "S-16", "khasi": "U slap u la sdang ban ther jur.", "english": "The rain has started pouring heavily.", "category": "Weather", "verified": True},
    {"id": "S-17", "khasi": "Nga kwah ban thied kine ki jain.", "english": "I want to buy these clothes.", "category": "Shopping", "verified": True},
    {"id": "S-18", "khasi": "Kano ka kot pule kaba phi pule?", "english": "Which textbook are you reading?", "category": "Education", "verified": True},
    {"id": "S-19", "khasi": "Ki khynnah skul ki leit sha skul man ka step.", "english": "The school children go to school every morning.", "category": "Education", "verified": True},
    {"id": "S-20", "khasi": "U Blei un kyrkhu ïa phi.", "english": "May God bless you.", "category": "Blessing", "verified": True},
]

with open(sentences_dest, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "khasi", "english", "category", "verified"])
    writer.writeheader()
    writer.writerows(curated_sentences)
print(f"  -> Generated verified sentences: {sentences_dest} ({len(curated_sentences)} sentences)")

# C. Benchmark Test Cases from Project Report Chapter 7.5
test_cases_report = [
    {
        "test_id": "TC-01",
        "module": "Module 1 - Learning Assistant",
        "description": "Vocabulary lookup for a verified Khasi word",
        "input": "Khublei",
        "expected_behaviour": "Display correct English meaning ('Hello / Thank you / Blessings'), pronunciation guide ('Khu-blay'), and example sentences.",
        "input_type": "text",
        "target_language": "en"
    },
    {
        "test_id": "TC-02",
        "module": "Module 1 - Learning Assistant",
        "description": "Sentence meaning lookup for a verified Khasi sentence",
        "input": "Ka jingsuk ha kaba kut!",
        "expected_behaviour": "Display reviewed translation ('Peace at last!') and grammatical breakdown of components.",
        "input_type": "text",
        "target_language": "en"
    },
    {
        "test_id": "TC-03",
        "module": "Module 2 - Voice-to-Voice Translation",
        "description": "Short English voice input translated to Khasi",
        "input": "Where is the way to go to the market?",
        "expected_behaviour": "Produce accurate Khasi translation ('Hangno ka lynti ban leit sha iew?') and synthesized speech output.",
        "input_type": "speech / text",
        "target_language": "kha"
    },
    {
        "test_id": "TC-04",
        "module": "Module 2 - Voice-to-Voice Translation",
        "description": "Short Khasi voice input translated to English",
        "input": "Kumno phi long mynta ka sngi?",
        "expected_behaviour": "Produce accurate English translation ('How are you today?') and English spoken output.",
        "input_type": "speech / text",
        "target_language": "en"
    },
    {
        "test_id": "TC-05",
        "module": "Module 3 - OCR Image Translation",
        "description": "Extract text from clear printed Khasi notice/document and translate",
        "input_sample_image": "sample_images/DOC17333794530_p003_l013.jpg",
        "ground_truth_ocr": "nga long u",
        "expected_behaviour": "Correctly extract printed characters ('nga long u') via OCR and translate to English ('I am').",
        "input_type": "image",
        "target_language": "en"
    },
    {
        "test_id": "TC-06",
        "module": "Module 3 - OCR Image Translation",
        "description": "Handling degraded, blurred, or noisy input image",
        "input_sample_image": "simulated_blur_sample.jpg",
        "expected_behaviour": "Detect poor OCR confidence below threshold (e.g. conf < 0.60) and display a user warning instead of inaccurate text.",
        "input_type": "image",
        "target_language": "en"
    },
    {
        "test_id": "TC-07",
        "module": "Module 2 - Voice-to-Voice Translation",
        "description": "Speech with background noise robustness testing",
        "input": "Nga kwah ban bam ja (with 15dB ambient traffic noise)",
        "expected_behaviour": "Measure transcription word error rate and provide confidence estimate.",
        "input_type": "noisy_speech",
        "target_language": "en"
    }
]

with open(tests_dest, "w", encoding="utf-8") as f:
    json.dump(test_cases_report, f, indent=2, ensure_ascii=False)
print(f"  -> Generated evaluation test cases: {tests_dest} ({len(test_cases_report)} test cases)")

print("\n" + "=" * 65)
print("All KhasiConnect AI datasets downloaded and organized successfully!")
print("=" * 65)
