import re
from collections import Counter

ENGLISH_FREQUENCY_RANKS = [
    'E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 
    'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 
    'V', 'K', 'J', 'X', 'Q', 'Z'
]

def load_cipher_text():
    try:
        with open('scroll.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("Error: scroll.txt not found!")
        return None

def analyze_cipher_character_frequencies(cipher_text):
    devanagari_chars = [c for c in cipher_text if 0x0900 <= ord(c) <= 0x097F]
    
    char_counts = Counter(devanagari_chars)
    total_chars = len(devanagari_chars)
    
    char_frequencies = {}
    for char, count in char_counts.items():
        frequency_percentage = (count / total_chars) * 100
        char_frequencies[char] = {
            'count': count,
            'frequency': frequency_percentage
        }
    
    ranked_chars = [char for char, count in char_counts.most_common()]
    
    return ranked_chars, char_frequencies

def create_rank_based_mapping(ranked_cipher_chars, char_frequencies):
    mapping = {}
    
    for rank, cipher_char in enumerate(ranked_cipher_chars):
        if rank < len(ENGLISH_FREQUENCY_RANKS):
            english_letter = ENGLISH_FREQUENCY_RANKS[rank]
            mapping[cipher_char] = english_letter
    
    return mapping

def decode_cipher_text(cipher_text, mapping):
    decoded = []
    for char in cipher_text:
        if char in mapping:
            decoded.append(mapping[char])
        else:
            decoded.append(char)
    
    return ''.join(decoded)

def find_flag_patterns(decoded_text):
    flag_patterns = [
        r'MCSC\{[A-Z]+\}',
    ]
    
    found_flags = []
    for pattern in flag_patterns:
        matches = re.findall(pattern, decoded_text, re.IGNORECASE)
        found_flags.extend(matches)
    
    unique_flags = list(dict.fromkeys(found_flags))
    return unique_flags

def main():
    print("Frequency Analysis Solver")
    
    cipher_text = load_cipher_text()
    if not cipher_text:
        return
    
    ranked_chars, char_frequencies = analyze_cipher_character_frequencies(cipher_text)
    
    if not ranked_chars:
        print("No characters to analyze!")
        return
    
    mapping = create_rank_based_mapping(ranked_chars, char_frequencies)
    
    decoded_text = decode_cipher_text(cipher_text, mapping)
    
    flags_found = find_flag_patterns(decoded_text)
    
    if flags_found:
        print(f"FLAG(S) FOUND:")
        for flag in flags_found:
            print(f"   {flag}")
    else:
        print(f"No flags found")
    
    with open('frequency_analysis_solution.txt', 'w', encoding='utf-8') as f:
        f.write("RANK-BASED FREQUENCY ANALYSIS SOLUTION\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("MAPPING (Devanagari -> English):\n")
        f.write("-" * 35 + "\n")
        for i, (cipher_char, english_letter) in enumerate(mapping.items(), 1):
            freq_data = char_frequencies[cipher_char]
            f.write(f"Rank {i:2}: {cipher_char} -> {english_letter} ({freq_data['frequency']:.2f}%, {freq_data['count']} occurrences)\n")
        
        if flags_found:
            f.write(f"\n\nFLAGS FOUND:\n")
            f.write("-" * 20 + "\n")
            for flag in flags_found:
                f.write(f"{flag}\n")
        
        f.write(f"\n\nCOMPLETE DECODED TEXT:\n")
        f.write("-" * 30 + "\n")
        f.write(decoded_text)
    
    print(f"\nAnalysis saved to 'frequency_analysis_solution.txt'")
    
    if flags_found:
        print(f"\nSolved!")
    else:
        print(f"\nReview the decoded text")

if __name__ == "__main__":
    main()