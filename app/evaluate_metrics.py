from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

rouge = Rouge()

# ✅ Compute BLEU Score
def calculate_bleu(reference, candidate):
    if not reference.strip():
        return "NA"
    try:
        return round(sentence_bleu([reference.split()], candidate.split()), 3)
    except:
        return "NA"

# ✅ Compute ROUGE-L Score
def calculate_rouge(reference, candidate):
    if not reference.strip():
        return "NA"
    try:
        return round(rouge.get_scores(candidate, reference, avg=True)['rouge-l']['f'], 3)
    except:
        return "NA"
