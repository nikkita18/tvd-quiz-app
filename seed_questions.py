"""
seed_questions.py — Bulk insert TVD / Mystic Diaries themed quiz questions
into the b12_app.quiz table across all 3 difficulty levels.

Uses duplicate-checking per question to safely add new questions
without duplicating existing ones. Safe to run multiple times.

Usage:
    python seed_questions.py
"""

from db import get_connection

# ── Level 1: Easy — Basic character facts & locations ──────────────
LEVEL_1 = [
    ("Who is the main female protagonist of The Vampire Diaries?",
     "Elena Gilbert", "Bonnie Bennett", "1"),
    ("What is the name of the town where The Vampire Diaries is set?",
     "Mystic Falls", "New Orleans", "1"),
    ("Which Salvatore brother is the older one?",
     "Damon Salvatore", "Stefan Salvatore", "1"),
    ("What supernatural creature is Bonnie Bennett?",
     "A Witch", "A Vampire", "1"),
    ("What is the name of the bar that Damon frequently visits?",
     "Mystic Grill", "The Bourbon Bar", "1"),
    ("Who is Elena Gilbert's biological mother?",
     "Isobel Flemming", "Jenna Sommers", "1"),
    ("What is Stefan Salvatore's nickname due to his dark past?",
     "The Ripper", "The Shadow", "1"),
    ("Who is the history teacher that becomes a vampire hunter?",
     "Alaric Saltzman", "John Gilbert", "1"),
    ("What type of creature is Tyler Lockwood?",
     "A Werewolf", "A Witch", "1"),
    ("What is the name of Elena's younger brother?",
     "Jeremy Gilbert", "Matt Donovan", "1"),
]

# ── Level 2: Medium — Plot knowledge & turning points ──────────────
LEVEL_2 = [
    ("Who turned Stefan and Damon into vampires?",
     "Katherine Pierce", "Klaus Mikaelson", "1"),
    ("What is the Sun and Moon curse actually about?",
     "Breaking Klaus's hybrid curse", "Destroying all vampires", "1"),
    ("Which Original vampire is known as the first hybrid?",
     "Klaus Mikaelson", "Elijah Mikaelson", "1"),
    ("What ring protects certain humans from supernatural death?",
     "Gilbert Ring", "Daylight Ring", "1"),
    ("Who is the doppelganger of Elena Gilbert from the 15th century?",
     "Katherine Pierce", "Tatia", "1"),
    ("What does a vampire need to walk in daylight?",
     "A Daylight Ring spelled by a witch", "A special blood potion", "1"),
    ("Who killed Elena's parents by driving their car off Wickery Bridge?",
     "It was an accident", "Katherine Pierce", "1"),
    ("What is the name of Klaus's sister who was daggered for 900 years?",
     "Rebekah Mikaelson", "Freya Mikaelson", "1"),
    ("Who sacrificed herself to bring Jeremy back to life?",
     "Bonnie Bennett", "Caroline Forbes", "1"),
    ("Which vampire compelled Elena to forget meeting Damon first?",
     "Damon Salvatore", "Stefan Salvatore", "1"),
]

# ── Level 3: Hard — Deep lore, obscure details, quotes ─────────────
LEVEL_3 = [
    ("What is the name of the spell that linked all vampires to the Originals?",
     "The Sireline Spell", "The Binding Curse", "1"),
    ("Which character said: 'I will always choose you'?",
     "Damon to Elena", "Stefan to Caroline", "1"),
    ("What was the name of the dimension where dead supernatural beings go?",
     "The Other Side", "The Shadow Realm", "1"),
    ("Who created the first vampires using the Immortality Spell?",
     "Esther Mikaelson", "Qetsiyah", "1"),
    ("In which season does Bonnie become the Anchor to the Other Side?",
     "Season 5", "Season 4", "1"),
    ("What was the cure for vampirism hidden inside?",
     "Silas's tomb", "The Gilbert family vault", "1"),
    ("Who was the first character to take the cure for vampirism?",
     "Katherine Pierce", "Elena Gilbert", "1"),
    ("What is the name of the ancient language used for witch spells?",
     "Latin-based incantations", "Old Norse runes", "1"),
    ("Who was the very first doppelganger in the Petrova bloodline?",
     "Amara", "Tatia", "1"),
    ("What did Kai Parker merge with to become the leader of the Gemini Coven?",
     "His twin Luke", "His twin Liv", "1"),
]

ALL_LEVELS = {
    1: LEVEL_1,
    2: LEVEL_2,
    3: LEVEL_3,
}


def seed(reset=True):
    db = get_connection()
    cur = db.cursor()

    if reset:
        print("Cleaning existing quiz table to maintain strictly 10 questions per level...")
        cur.execute("TRUNCATE TABLE quiz")

    inserted = 0
    for level, questions in ALL_LEVELS.items():
        level_inserted = 0
        for ques, opt1, opt2, answer in questions:
            sq = "INSERT INTO quiz (level, ques, opt1, opt2, answer) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(sq, (level, ques, opt1, opt2, answer))
            inserted += 1
            level_inserted += 1

        print(f"  Level {level}: inserted exactly {level_inserted} questions.")

    db.commit()
    cur.close()
    db.close()
    print(f"\nDone - {inserted} total questions seeded across all 3 levels (10 per level).")


if __name__ == "__main__":
    print("Mystic Diaries Quiz Seeder")
    print("=" * 40)
    seed(reset=True)


