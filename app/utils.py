# ✅ Function to truncate long context text
def truncate_context(docs, max_words=600):
    truncated = []
    total_words = 0
    for doc in docs:
        words = doc.split()
        if total_words + len(words) > max_words:
            break
        truncated.append(doc)
        total_words += len(words)
    return "\n\n".join(truncated)

# ✅ Load list of questions from a text file
def load_questions(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
