# Wordlist_gen
Professional wordlist generation tool for authorized security testing. Combines personal information, intelligent patterns, and transformations to create comprehensive password lists for penetration testing and security audits.

Features
Core Capabilities

* Personal Information Based: Generate wordlists from names, dates, phone numbers, and locations
* Pattern Generation: Support for custom patterns using placeholders (?l, ?u, ?d, ?s)
* Leetspeak Transformations: Automatic character substitutions (a→4, e→3, i→1, o→0, etc.)
* Customizable Length: Set minimum and maximum word lengths
* Word Count Limiting: Control the exact number of words in your wordlist
* Special Character Integration: Add custom special characters to password combinations
* Interactive Mode: User-friendly step-by-step input collection
* CLI Mode: Scriptable command-line arguments for automation
* Progress Indicators: Real-time feedback during generation

🔧 Generation Methods
1. Personal Info Combinations: Smart combinations of personal data
2. Pattern-Based: Generate words from custom patterns
3. Character Set: Create words from custom character sets
4. File Import: Read base words from existing files
5. Transformations: Apply prefixes, suffixes, and leetspeak

📦 Installation
*Python 3.6 or higher


Clone the Repository
git clone https://github.com/yourusername/wordlist-generator.git
cd wordlist-generator

🚀 Usage
Interactive Mode
python wordlist_gen.py

You'll be prompted for:

1. Personal Information: Name, phone, DOB, father's name, mother's name, place
2. Special Characters: Whether to include special symbols
3. Patterns: Custom generation patterns
4. Word Length: Minimum and maximum length
5. Word Count: Maximum number of words
6. Output File: Filename for the wordlist

CLI Mode Examples

python wordlist_gen.py \
  --name "John" \
  --dob "15/08/1990" \
  --phone "9876543210" \
  --place "Mumbai" \
  --min-len 6 \
  --max-len 12 \
  --max-words 500 \
  -o john_wordlist.txt

  📚 Pattern Syntax
  Use these placeholders to create custom patterns:

  Placeholder  Description                        Example Characters
  ?l           Lowercase letters                  a, b, c, ... z
  ?u           Uppercase letters                  A, B, C, ... Z
  ?d           Digits                             0, 1, 2, ... 9
  ?s           Special characters                 !, @, #, $, %, &
  ?a           All (letters + digits + special)   Combined set

  Pattern Examples
* ?l?l?l?d?d?d → abc123, xyz789
* ?u?l?l?l?d?d → Alex99, John01
* ?l?l?l?s?d?d → abc!12, xyz@99


Command-Line Options
Personal Information:
  --name NAME              Target's name
  --phone PHONE           Phone number
  --dob DOB               Date of birth (DD/MM/YYYY)
  --father-name NAME      Father's name
  --mother-name NAME      Mother's name
  --place PLACE           City or location

Generation Options:
  -p, --pattern PATTERN   Pattern using ?l, ?u, ?d, ?s
  -c, --charset CHARSET   Custom character set
  -f, --file FILE         Read base words from file

Length Options:
  --min-len LENGTH        Minimum word length (default: 4)
  --max-len LENGTH        Maximum word length (default: 12)

Transformations:
  --leetspeak             Apply leetspeak transformations
  --prefix PREFIX         Prepend string to all words
  --suffix SUFFIX         Append string to all words

Limits:
  --max-words COUNT       Maximum number of words

Output:
  -o, --output FILE       Output filename (required)


***** Development Setup
git clone https://github.com/Jhonwick672/wordlist-generator
cd wordlist-generator
# Make your changes
python wordlist_gen.py  # Test your changes
