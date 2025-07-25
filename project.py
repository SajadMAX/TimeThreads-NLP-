
import spacy
import requests
import wikipediaapi
from spacy.matcher import Matcher
from dateutil.parser import parse
import pandas as pd
import re
from prettytable import PrettyTable



nlp = spacy.load("en_core_web_sm")

user_agent = "MyProjectName/1.0"

def main():

    while True:
        query = input("Enter a name: ").strip()
        if not query:
            print("Name cannot be empty.")
        elif not any(char.isalpha() for char in query):
            print("Invalid name. Must contain at least one letter.")
        else:
            break

    # Retrieve Wikipedia page by using wikipedia api
    page = get_wiki_page(query, user_agent)
    if not page:
        print(f"Could not Find Wikipedia page for: {query}")
        return

    wikipedia_text = page.summary
    try:
        # Extract and process timeline
        timeline = extract_timeline_with_topics(wikipedia_text)

        # Validate timeline extraction results
        if not timeline:
            print(f"It Seems {query} Is NOT A Valid Name ")
            return

        df = pd.DataFrame(timeline)

        # Check for required Date column
        if "Date" not in df.columns:
            print(f"It Seems {query} Is NOT A Valid Name (missing the date )")
            return

        # Process and output timeline
        df = df.drop_duplicates()
        df = df.sort_values("Date")
        df = df.reset_index(drop=True)
        generate_pretty_table(df, output_file="timeline.txt")

    except (KeyError, TypeError) as e:
        print(f"It Seems {query} Is NOT A Valid Name---> error: {str(e)}")






def get_wiki_page(user_query, user_agent):
    # Initialize Wikipedia API
    wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent=user_agent,
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    # Preprocess query
    clean_query = re.sub(r'[^a-zA-Z0-9 ]', ' ', user_query)  # Remove special chars
    clean_query = re.sub(r'\s+', ' ', clean_query).strip().title()  # Normalize spaces

    # Strategy 1: Try direct access (handles redirects)
    page = wiki.page(clean_query)
    if page.exists():
        return page



    return None  # No match found




def extract_timeline_with_topics(wikipedia_text):
    doc = nlp(wikipedia_text)
    timeline = []

    for sent in doc.sents:
        # Skip short sentences
        if len(sent.text) < 20:
            continue

        # Find dates
        dates = []
        for ent in sent.ents:
            if ent.label_ == "DATE":
                try:
                    # Skip durations and age references
                    if any(x in ent.text.lower() for x in ["century", "ages", "decade", "years", "age"]):
                        continue
                    dt = parse(ent.text, fuzzy=True)
                    dates.append(dt.strftime("%Y"))
                except:
                    continue

        if dates:
            # Clean event text
            event_text = re.sub(r'\[\d+\]', '', sent.text).strip()

            # Determine topic
            topic = classify_topic(event_text)

            # Use earliest date
            event_date = sorted(dates)[0]

            timeline.append({
                "Date": event_date,
                "Topic": topic,
                "Event": event_text
            })

    return timeline

def classify_topic(sent):
    """Enhanced topic classification with context rules for various professions"""
    text = sent.lower()
    doc = nlp(sent)  # Process sentence for linguistic features

    # 1. Birth and Early Life
    if "born" in text and any(t in text for t in ["date", "year", "month"]):
        if text.find("born") == text.index("born"):
            return "BIRTH"

    # 2. Education
    if any(word in text for word in ["study", "graduate", "degree", "phd", "university", "college"]):
        return "EDUCATION"

    # 3. Career/Profession Specific
    if "actor" in text or "actress" in text or any(word in text for word in ["film", "movie", "role", "character"]):
        return "ACTING"

    if "athlete" in text or "player" in text or any(word in text for word in ["sport", "team", "championship", "medal", "olympic"]):
        return "SPORTS"

    if "politician" in text or any(word in text for word in ["election", "senator", "president", "minister", "party", "government"]):
        return "POLITICS"

    if any(word in text for word in ["join", "work", "hire", "research", "scientist", "professor"]):
        return "CAREER"

    # 4. Creative Works
    if "podcast" in text or "interview" in text:
        return "PODCAST"

    if any(word in text for word in ["publish", "book", "paper", "article"]):
        return "PUBLICATION"

    if any(word in text for word in ["album", "song", "music", "release", "single"]):
        return "MUSIC"

    # 5. Life Events
    if any(word in text for word in ["move", "relocate", "settle"]):
        return "MOVE"

    if any(word in text for word in ["marry", "divorce", "wedding", "spouse"]):
        return "PERSONAL_LIFE"

    # 6. Achievements
    if any(word in text for word in ["award", "prize", "honor", "oscar", "grammy", "nobel"]):
        return "AWARD"

    if any(word in text for word in ["found", "create", "establish", "startup"]):
        return "PROJECT"

    # 7. Controversies
    if any(word in text for word in ["controversy", "scandal", "accuse", "criticize"]):
        return "CONTROVERSY"

    # 8. Health
    if any(word in text for word in ["health", "illness", "diagnose", "hospital"]):
        return "HEALTH"

    # 9. Death
    if "die" in text or "death" in text or "pass away" in text:
        return "DEATH"

    # 10. Financial Events
    if any(word in text for word in ["invest", "acquire", "valuation", "ipo", "fortune"]):
        return "FINANCE"

    # Try to detect profession from entity context
    for ent in doc.ents:
        if ent.label_ == "ORG":
            if "studio" in ent.text.lower() or "pictures" in ent.text.lower():
                return "ACTING"
            if "sport" in ent.text.lower() or "fc" in ent.text.lower() or "olympic" in ent.text.lower():
                return "SPORTS"
            if "senate" in ent.text.lower() or "congress" in ent.text.lower() or "parliament" in ent.text.lower():
                return "POLITICS"

    # Check for profession nouns
    profession_keywords = {
        "ACTING": ["actor", "actress", "star"],
        "SPORTS": ["athlete", "player", "coach"],
        "POLITICS": ["politician", "senator", "representative"]
    }

    for token in doc:
        for topic, keywords in profession_keywords.items():
            if token.lemma_ in keywords:
                return topic

    return " -"






def generate_pretty_table(df, output_file="timeline.txt"):
    if df.empty:
        print("No events")
        return


    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y')


    table = PrettyTable()
    table.field_names = ["Date", "Topic", "Event"]
    table.align["Event"] = "l"

    for _, row in df.iterrows():
        table.add_row([row['Date'], row['Topic'], row['Event']])

    with open(output_file, 'w') as f:
        f.write(str(table))
    print(f"Saved table to {output_file}")



if __name__ == "__main__":
    main()
