# The Maharaja's Secret Script - Writeup

## Challenge Overview

**Category:** Cryptography 
**Flag:** `mcsc{FRQNCYANALYSISDEVANAGARI}` (Note: Case-Insesnsitive Flag)

This challenge presents a substitution cipher where English letters have been replaced with Devanagari (Sanskrit/Hindi) characters. The cipher uses a rank-based frequency mapping, making it solvable through frequency analysis.

## Challenge Description

We are given a text file (`scroll.txt`) containing what appears to be a long message written entirely in Devanagari script. The challenge requires us to decode this ancient script to reveal hidden English messages, including the flag.

## Analysis

### Understanding the Cipher

The challenge implements a **rank-based substitution cipher** with the following characteristics:

1. **Substitution Cipher**: Each English letter is consistently replaced with a unique Devanagari character
2. **Frequency Preservation**: The cipher maintains the statistical frequency distribution of English letters
3. **Rank-Based Mapping**: The most frequent English letter (E) maps to the most frequent Devanagari character, and so on

## Solution Approach

### Step 1: Character Frequency Analysis

First, we need to count the frequency of each Devanagari character in the cipher text:

```python
from collections import Counter

def analyze_cipher_character_frequencies(cipher_text):
    # Extract only Devanagari characters (Unicode range 0x0900-0x097F)
    devanagari_chars = [c for c in cipher_text if 0x0900 <= ord(c) <= 0x097F]
    
    # Count frequencies
    char_counts = Counter(devanagari_chars)
    total_chars = len(devanagari_chars)
    
    # Calculate percentage frequencies
    char_frequencies = {}
    for char, count in char_counts.items():
        frequency_percentage = (count / total_chars) * 100
        char_frequencies[char] = {
            'count': count,
            'frequency': frequency_percentage
        }
    
    # Get characters ranked by frequency
    ranked_chars = [char for char, count in char_counts.most_common()]
    
    return ranked_chars, char_frequencies
```

### Step 2: Create Rank-Based Mapping

Using the known English letter frequency ranks, we create a mapping:

```python
ENGLISH_FREQUENCY_RANKS = [
    'E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 
    'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 
    'V', 'K', 'J', 'X', 'Q', 'Z'
]

def create_rank_based_mapping(ranked_cipher_chars, char_frequencies):
    mapping = {}
    
    for rank, cipher_char in enumerate(ranked_cipher_chars):
        if rank < len(ENGLISH_FREQUENCY_RANKS):
            english_letter = ENGLISH_FREQUENCY_RANKS[rank]
            mapping[cipher_char] = english_letter
    
    return mapping
```

### Step 3: Decode the Cipher Text

Apply the mapping to decode the entire cipher text:

```python
def decode_cipher_text(cipher_text, mapping):
    decoded = []
    for char in cipher_text:
        if char in mapping:
            decoded.append(mapping[char])
        else:
            decoded.append(char)  # Keep spaces and other characters
    
    return ''.join(decoded)
```

### Step 4: Extract the Flag

Search for flag patterns in the decoded text:

```python
import re

def find_flag_patterns(decoded_text):
    flag_patterns = [
        r'MCSC\{[A-Z]+\}',
    ]
    
    found_flags = []
    for pattern in flag_patterns:
        matches = re.findall(pattern, decoded_text, re.IGNORECASE)
        found_flags.extend(matches)
    
    return list(dict.fromkeys(found_flags))
```

### Step 5: Analyze the flag text

```
THE FLAY IS MCSC{FRQNCGANALGSISDEVANAYARI} 
```
This is present in the decoded output. As we can see there is an error where instead of FLAG ot says FLAY. This is to provide a more realistic scenario where the character mapping is not necessarily perfect and tells us 'G' and 'Y' need to be interchanged.

Therefore the same line would say:
```
THE FLAg IS MCSC{FRQNCYANALYSISDEVANAGARI} 
```

There are more english phrases throughout 'scroll.txt' to help ensure the mapping is correct.

## Complete Solution Script

The complete solution is in (`solve_challenge.py`).