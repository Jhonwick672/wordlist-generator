#!/usr/bin/env python3
"""
Advanced Wordlist Generator for Cybersecurity
A comprehensive CLI tool for generating custom wordlists with various patterns and transformations.
"""

import itertools
import string
import argparse
import sys
from pathlib import Path
from datetime import datetime


class WordlistGenerator:
    def __init__(self):
        self.charset_map = {
            '?l': string.ascii_lowercase,
            '?u': string.ascii_uppercase,
            '?d': string.digits,
            '?s': string.punctuation,
            '?a': string.ascii_letters + string.digits + string.punctuation
        }
        self.leetspeak_map = {
            'a': ['4', '@'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7'],
            'l': ['1'],
            'g': ['9']
        }
        self.wordlist = set()
        
    def generate_from_pattern(self, pattern, count=None):
        """Generate words based on pattern like ?l?l?d?d"""
        print(f"[*] Generating from pattern: {pattern}")
        
        # Parse pattern into character sets
        char_sets = []
        i = 0
        while i < len(pattern):
            if pattern[i] == '?':
                if i + 1 < len(pattern):
                    key = pattern[i:i+2]
                    if key in self.charset_map:
                        char_sets.append(self.charset_map[key])
                        i += 2
                        continue
            char_sets.append([pattern[i]])
            i += 1
        
        if not char_sets:
            return
        
        # Generate combinations
        generated = 0
        for combo in itertools.product(*char_sets):
            word = ''.join(combo)
            self.wordlist.add(word)
            generated += 1
            
            if generated % 10000 == 0:
                print(f"[+] Generated {generated} words from pattern...")
            
            if count and generated >= count:
                break
        
        print(f"[✓] Pattern generation complete: {generated} words")
    
    def generate_from_charset(self, charset, min_len, max_len, count=None):
        """Generate words from custom character set with length range"""
        print(f"[*] Generating from charset with length {min_len}-{max_len}")
        
        generated = 0
        for length in range(min_len, max_len + 1):
            for combo in itertools.product(charset, repeat=length):
                word = ''.join(combo)
                self.wordlist.add(word)
                generated += 1
                
                if generated % 10000 == 0:
                    print(f"[+] Generated {generated} words...")
                
                if count and generated >= count:
                    return
        
        print(f"[✓] Charset generation complete: {generated} words")
    
    def add_personal_info_combinations(self, name=None, phone=None, dob=None, 
                                      father_name=None, mother_name=None, place=None):
        """Generate combinations from personal information"""
        print("[*] Generating from personal information...")
        
        base_words = []
        
        if name:
            base_words.extend([name, name.lower(), name.upper(), name.capitalize()])
        if father_name:
            base_words.extend([father_name, father_name.lower(), father_name.capitalize()])
        if mother_name:
            base_words.extend([mother_name, mother_name.lower(), mother_name.capitalize()])
        if place:
            base_words.extend([place, place.lower(), place.upper(), place.capitalize()])
        
        # Add DOB variations
        dob_variants = []
        if dob:
            # Assuming format: DD/MM/YYYY or DD-MM-YYYY
            dob_clean = dob.replace('/', '').replace('-', '')
            if len(dob_clean) >= 8:
                day = dob_clean[:2]
                month = dob_clean[2:4]
                year = dob_clean[4:8]
                year_short = year[2:]
                
                dob_variants.extend([
                    dob_clean, day + month + year, day + month + year_short,
                    year, year_short, day + month, month + year
                ])
        
        # Add phone variations
        phone_variants = []
        if phone:
            phone_clean = ''.join(filter(str.isdigit, phone))
            phone_variants.extend([
                phone_clean, phone_clean[-4:], phone_clean[-6:], phone_clean[-8:]
            ])
        
        # Combine base words with numbers and special chars
        common_suffixes = ['123', '1234', '12345', '!', '@', '#', '123!', '2023', '2024', '2025']
        common_prefixes = ['@', '#', 'my']
        
        initial_count = len(self.wordlist)
        
        for word in base_words:
            if not word:
                continue
            self.wordlist.add(word)
            
            # Add with common suffixes
            for suffix in common_suffixes:
                self.wordlist.add(word + suffix)
            
            # Add with common prefixes
            for prefix in common_prefixes:
                self.wordlist.add(prefix + word)
            
            # Combine with DOB
            for dob_var in dob_variants:
                self.wordlist.add(word + dob_var)
                self.wordlist.add(dob_var + word)
            
            # Combine with phone
            for phone_var in phone_variants:
                self.wordlist.add(word + phone_var)
                self.wordlist.add(phone_var + word)
        
        # Add combinations of different personal info
        if len(base_words) >= 2:
            for combo in itertools.combinations(base_words[:4], 2):
                self.wordlist.add(''.join(combo))
        
        new_words = len(self.wordlist) - initial_count
        print(f"[✓] Personal info combinations complete: {new_words} new words")
    
    def apply_leetspeak(self):
        """Apply leetspeak transformations to existing wordlist"""
        print("[*] Applying leetspeak transformations...")
        
        new_words = set()
        for word in list(self.wordlist):
            word_lower = word.lower()
            
            # Find positions where leetspeak can be applied
            leet_positions = []
            for i, char in enumerate(word_lower):
                if char in self.leetspeak_map:
                    leet_positions.append((i, char))
            
            # Generate combinations (limit to prevent explosion)
            if leet_positions and len(leet_positions) <= 4:
                for r in range(1, min(len(leet_positions) + 1, 3)):
                    for combo in itertools.combinations(leet_positions, r):
                        new_word = list(word)
                        for pos, char in combo:
                            for replacement in self.leetspeak_map[char]:
                                temp_word = new_word.copy()
                                temp_word[pos] = replacement
                                new_words.add(''.join(temp_word))
        
        self.wordlist.update(new_words)
        print(f"[✓] Leetspeak applied: {len(new_words)} variations added")
    
    def add_from_file(self, filepath):
        """Read base words from a file"""
        print(f"[*] Reading words from {filepath}...")
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                initial_count = len(self.wordlist)
                for line in f:
                    word = line.strip()
                    if word:
                        self.wordlist.add(word)
                
                new_words = len(self.wordlist) - initial_count
                print(f"[✓] Added {new_words} words from file")
        except FileNotFoundError:
            print(f"[!] File not found: {filepath}")
        except Exception as e:
            print(f"[!] Error reading file: {e}")
    
    def apply_prefix_suffix(self, prefix=None, suffix=None):
        """Apply prefix and/or suffix to all words"""
        if not prefix and not suffix:
            return
        
        print(f"[*] Applying prefix/suffix...")
        new_words = set()
        
        for word in self.wordlist:
            modified = word
            if prefix:
                modified = prefix + modified
            if suffix:
                modified = modified + suffix
            new_words.add(modified)
        
        self.wordlist.update(new_words)
        print(f"[✓] Prefix/suffix applied: {len(new_words)} words added")
    
    def filter_by_length(self, min_len, max_len):
        """Filter wordlist by length"""
        initial_count = len(self.wordlist)
        self.wordlist = {w for w in self.wordlist if min_len <= len(w) <= max_len}
        removed = initial_count - len(self.wordlist)
        print(f"[*] Filtered by length ({min_len}-{max_len}): {removed} words removed")
    
    def limit_wordcount(self, max_words):
        """Limit the number of words in the wordlist"""
        if len(self.wordlist) > max_words:
            self.wordlist = set(list(self.wordlist)[:max_words])
            print(f"[*] Limited to {max_words} words")
    
    def save_to_file(self, output_file):
        """Save wordlist to file"""
        print(f"[*] Saving wordlist to {output_file}...")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for word in sorted(self.wordlist):
                    f.write(word + '\n')
            
            print(f"[✓] Wordlist saved: {len(self.wordlist)} words written to {output_file}")
            print(f"[✓] File size: {Path(output_file).stat().st_size / 1024:.2f} KB")
        except Exception as e:
            print(f"[!] Error saving file: {e}")


def get_user_input():
    """Interactive mode to collect user inputs"""
    print("\n" + "="*60)
    print("           INTERACTIVE WORDLIST GENERATION")
    print("="*60)
    
    inputs = {}
    
    # Personal Information
    print("\n[STEP 1] Personal Information (Press Enter to skip)")
    print("-" * 60)
    inputs['name'] = input("Enter name: ").strip() or None
    inputs['phone'] = input("Enter phone number: ").strip() or None
    inputs['dob'] = input("Enter date of birth (DD/MM/YYYY): ").strip() or None
    inputs['father_name'] = input("Enter father's name: ").strip() or None
    inputs['mother_name'] = input("Enter mother's name: ").strip() or None
    inputs['place'] = input("Enter place/city: ").strip() or None
    
    # Special Characters
    print("\n[STEP 2] Special Characters & Patterns")
    print("-" * 60)
    add_special = input("Add special characters? (y/n): ").strip().lower()
    inputs['add_special'] = add_special == 'y'
    
    if inputs['add_special']:
        print("\nCommon special characters: ! @ # $ % & * _")
        custom_special = input("Enter custom special characters (or press Enter for common): ").strip()
        inputs['special_chars'] = custom_special if custom_special else "!@#$%&*_"
    else:
        inputs['special_chars'] = None
    
    # Patterns
    add_patterns = input("\nGenerate pattern-based words? (e.g., abc123) (y/n): ").strip().lower()
    if add_patterns == 'y':
        print("\nPattern syntax: ?l=lowercase, ?u=uppercase, ?d=digit, ?s=special")
        print("Example: ?l?l?d?d generates words like 'ab12', 'xy99'")
        pattern = input("Enter pattern (or press Enter to skip): ").strip()
        inputs['pattern'] = pattern if pattern else None
    else:
        inputs['pattern'] = None
    
    # Leetspeak
    leetspeak = input("\nApply leetspeak transformations? (a->4, e->3, etc.) (y/n): ").strip().lower()
    inputs['leetspeak'] = leetspeak == 'y'
    
    # Word Length
    print("\n[STEP 3] Word Length Configuration")
    print("-" * 60)
    while True:
        try:
            min_len = input("Minimum word length (default 4): ").strip()
            inputs['min_len'] = int(min_len) if min_len else 4
            if inputs['min_len'] < 1:
                print("Minimum length must be at least 1")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    while True:
        try:
            max_len = input("Maximum word length (default 12): ").strip()
            inputs['max_len'] = int(max_len) if max_len else 12
            if inputs['max_len'] < inputs['min_len']:
                print(f"Maximum length must be >= minimum length ({inputs['min_len']})")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    # Word Count
    print("\n[STEP 4] Wordlist Size")
    print("-" * 60)
    while True:
        try:
            max_words = input("Maximum number of words (e.g., 500, 1000, or press Enter for unlimited): ").strip()
            inputs['max_words'] = int(max_words) if max_words else None
            if inputs['max_words'] and inputs['max_words'] < 1:
                print("Word count must be at least 1")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    # Output Filename
    print("\n[STEP 5] Output Configuration")
    print("-" * 60)
    while True:
        output = input("Enter output filename (e.g., wordlist.txt): ").strip()
        if output:
            if not output.endswith('.txt'):
                output += '.txt'
            inputs['output'] = output
            break
        print("Output filename is required!")
    
    return inputs


def main():
    banner = """
╔═══════════════════════════════════════════════════════╗
║     Advanced Wordlist Generator v1.0                  ║
║     For Cybersecurity Research & Penetration Testing  ║
╚═══════════════════════════════════════════════════════╝
    """
    print(banner)
    
    # Check if running in interactive mode or CLI mode
    if len(sys.argv) == 1:
        # Interactive mode
        inputs = get_user_input()
        
        print("\n" + "="*60)
        print("           GENERATING WORDLIST...")
        print("="*60 + "\n")
        
        generator = WordlistGenerator()
        
        # Generate from personal information
        if any([inputs.get('name'), inputs.get('phone'), inputs.get('dob'), 
                inputs.get('father_name'), inputs.get('mother_name'), inputs.get('place')]):
            generator.add_personal_info_combinations(
                name=inputs.get('name'),
                phone=inputs.get('phone'),
                dob=inputs.get('dob'),
                father_name=inputs.get('father_name'),
                mother_name=inputs.get('mother_name'),
                place=inputs.get('place')
            )
        
        # Generate from pattern
        if inputs.get('pattern'):
            generator.generate_from_pattern(inputs['pattern'], count=inputs.get('max_words'))
        
        # Add special characters as suffix
        if inputs.get('add_special') and inputs.get('special_chars'):
            for char in inputs['special_chars']:
                generator.apply_prefix_suffix(suffix=char)
        
        # Apply transformations
        if inputs.get('leetspeak'):
            generator.apply_leetspeak()
        
        # Filter by length
        if generator.wordlist:
            generator.filter_by_length(inputs['min_len'], inputs['max_len'])
        
        # Limit word count
        if inputs.get('max_words'):
            generator.limit_wordcount(inputs['max_words'])
        
        # Save to file
        if generator.wordlist:
            generator.save_to_file(inputs['output'])
            print(f"\n[✓] Complete! Total words in wordlist: {len(generator.wordlist)}")
        else:
            print("[!] No words generated. Please provide at least one generation method.")
            sys.exit(1)
    
    else:
        # CLI mode with arguments
        parser = argparse.ArgumentParser(
            description='Generate custom wordlists for security testing',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Interactive mode (recommended)
  python wordlist_gen.py
  
  # CLI mode with arguments
  python wordlist_gen.py --name "Alex" --place "Mumbai" --phone "9123456789" -o wordlist.txt
        """
        )
        
        parser.add_argument('-p', '--pattern', help='Pattern like ?l?l?d?d')
        parser.add_argument('-c', '--charset', help='Custom character set')
        parser.add_argument('--name', help='Name for wordlist generation')
        parser.add_argument('--phone', help='Phone number')
        parser.add_argument('--dob', help='Date of birth (DD/MM/YYYY)')
        parser.add_argument('--father-name', dest='father_name', help='Father\'s name')
        parser.add_argument('--mother-name', dest='mother_name', help='Mother\'s name')
        parser.add_argument('--place', help='Place/city name')
        parser.add_argument('--min-len', type=int, default=4, help='Minimum word length')
        parser.add_argument('--max-len', type=int, default=12, help='Maximum word length')
        parser.add_argument('--max-words', type=int, help='Maximum number of words')
        parser.add_argument('--prefix', help='Prepend string to all words')
        parser.add_argument('--suffix', help='Append string to all words')
        parser.add_argument('--leetspeak', action='store_true', help='Apply leetspeak')
        parser.add_argument('-f', '--file', help='Read base words from file')
        parser.add_argument('-o', '--output', required=True, help='Output filename')
        
        args = parser.parse_args()
        
        generator = WordlistGenerator()
        
        if any([args.name, args.phone, args.dob, args.father_name, args.mother_name, args.place]):
            generator.add_personal_info_combinations(
                name=args.name, phone=args.phone, dob=args.dob,
                father_name=args.father_name, mother_name=args.mother_name,
                place=args.place
            )
        
        if args.pattern:
            generator.generate_from_pattern(args.pattern, count=args.max_words)
        
        if args.charset:
            generator.generate_from_charset(args.charset, args.min_len, args.max_len, count=args.max_words)
        
        if args.file:
            generator.add_from_file(args.file)
        
        if args.leetspeak:
            generator.apply_leetspeak()
        
        if args.prefix or args.suffix:
            generator.apply_prefix_suffix(prefix=args.prefix, suffix=args.suffix)
        
        if generator.wordlist:
            generator.filter_by_length(args.min_len, args.max_len)
        
        if args.max_words:
            generator.limit_wordcount(args.max_words)
        
        if generator.wordlist:
            generator.save_to_file(args.output)
            print(f"\n[✓] Complete! Total words in wordlist: {len(generator.wordlist)}")
        else:
            print("[!] No words generated. Please provide at least one generation method.")
            sys.exit(1)


if __name__ == '__main__':
    main()
