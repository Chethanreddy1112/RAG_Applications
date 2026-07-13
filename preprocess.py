import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load scraped cards
with open("scraped_data/cards.json", "r", encoding="utf-8") as f:
    cards = json.load(f)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = []
chunk_id = 0

for card in cards:

    text = f"""
Card Name: {card['card_name']}

Category: {card['category']}

Benefits:
{card['benefits']}

Rewards:
{card['rewards']}

Rates & Fees:
{card['rates_fees']}
"""

    split_text = splitter.split_text(text)

    for chunk in split_text:

        chunks.append({
            "id": chunk_id,
            "text": chunk,
            "card_name": card["card_name"],
            "category": card["category"],
            "source": card["source"]
        })

        chunk_id += 1

with open("scraped_data/chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print(f"Created {len(chunks)} chunks")