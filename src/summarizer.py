import re
from collections import Counter


class FrequencySummarizer:
    def __init__(self, domain_stopwords=None):
        # Standard English stopwords + your custom "Domain Noise" list
        self.base_stopwords = {"the", "a", "is", "of", "to", "and", "in", "that", "was", "for"}
        self.domain_stopwords = set(domain_stopwords) if domain_stopwords else set()
        self.all_stopwords = self.base_stopwords.union(self.domain_stopwords)

    def summarize(self, text, num_sentences=3):
        # 1. Clean and split into sentences
        sentences = re.split(r'(?<=[.!?]) +', text)

        # 2. Tokenize and Filter (Domain-Awareness happens here)
        words = re.findall(r'\w+', text.lower())
        filtered_words = [w for w in words if w not in self.all_stopwords]

        # 3. Calculate Word Frequency
        word_freq = Counter(filtered_words)

        # 4. Score Sentences based on word importance
        sentence_scores = {}
        for sentence in sentences:
            for word in re.findall(r'\w+', sentence.lower()):
                if word in word_freq:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_freq[word]

        # 5. Get top sentences
        sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        summary = " ".join([s[0] for s in sorted_sentences[:num_sentences]])

        return summary, word_freq.most_common(5)