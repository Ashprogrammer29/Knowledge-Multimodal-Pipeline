from src.input_layer import InputAbstractionLayer
from src.summarizer import FrequencySummarizer
from src.metadata_processor import MetadataEngine
import os


def run_pipeline(file_path, domain_noise):
    print("--- Initializing Week 1 Pipeline ---")
    metadata = MetadataEngine()

    try:
        # 1. Extraction via IAL
        ial = InputAbstractionLayer(file_path)
        text = ial.extract_text()
        metadata.record_decision("IAL", f"Processed {file_path}", f"Extracted {len(text.split())} words.")

        # 2. Summarization with Domain Suppression
        summarizer = FrequencySummarizer(domain_stopwords=domain_noise)
        summary, keywords = summarizer.summarize(text)
        metadata.record_decision("Summarizer", f"Suppressed: {domain_noise}",
                                 "Applied Domain-Awareness to prioritize niche technical terms.")

        # 3. Final Output and Metadata Export
        print(f"\n[SYSTEM SUMMARY]:\n{summary}")
        print(f"\n[TOP KEYWORDS]: {', '.join([k[0] for k in keywords])}")

        metadata.export()
        print("\n--- Success: Results saved to output/metadata.json ---")

    except Exception as e:
        print(f"PIPELINE ERROR: {e}")
        metadata.record_decision("System", "Crash", str(e))
        metadata.export()


if __name__ == "__main__":
    # RELATIVE PATH: Works on any computer/Docker
    TARGET_FILE = os.path.join("data", "your_test_file.txt")

    # Configure Domain Noise for Biology textbook
    BIOLOGY_NOISE = ["cell", "cells", "organism", "life", "biology"]

    run_pipeline(TARGET_FILE, domain_noise=BIOLOGY_NOISE)