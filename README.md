# WordSearch

A comprehensive Python tool for finding valid dictionary words and processing matrix glyph maps for word games and puzzles. This tool filters an wordlist containing english words based on your specific requirements.

Primary target : For solving glyphs of https://glyph.today/

## Features

- **Word Mode**: Perform dictionary lookups with advanced filtering options
  - Search by word length
  - Require specific letters to be present
  - Exclude specific letters
  - Filter by starting letter
  - Filter by ending letter

- **Glyph Mode**: Process visual glyph matrices to discover hidden letters
  - Read composite multi-letter glyph arrays from a file
  - Automatically extract all possible constituent letters
  - Find matching dictionary words using discovered letters
  - Apply additional constraints (excludes, starts with, ends with)

- **Fast Offline Search**: Uses a pre-loaded dictionary for instant lookups
- **Case-Insensitive Input**: All inputs are processed with automatic case normalization
- **Clear Output**: Results displayed in alphabetical order

## Installation

### Requirements
- Python 3.6 or higher
- Dictionary file: `words_alpha.txt`
- For Glyph Mode: `glyphs_map.txt` (optional) and `glyph_input.txt`

### Setup

1. Clone or download this repository:
```bash
git clone https://github.com/winson-mok/WordSearch.git
cd WordSearch
```

2. Download the English word dictionary:
```bash
# Download from the dwyl/english-words repository
curl -O https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
```

3. Place `words_alpha.txt` in the same directory as `wordsearch.py`

## Usage

### Running the Program

```bash
python wordsearch.py
```

You'll be presented with a menu to choose between Word Mode and Glyph Mode.

### Word Mode

Word Mode allows you to search the dictionary with multiple constraints:

```
--- Word Mode Configuration ---
Enter mandatory word length: 5
Enter letters that MUST exist in the word (or press enter to skip): A
Enter letters that MUST NOT exist in the word (or press enter to skip): E
Enter the known starting letter (or press enter to skip): 
Enter the known ending letter (or press enter to skip): S
```

This example finds 5-letter words that:
- Contain the letter 'A'
- Do NOT contain the letter 'E'
- End with 'S'

### Glyph Mode

Glyph Mode reads visual glyph matrices from `glyph_input.txt` and discovers which letters are represented:

1. Create a `glyph_input.txt` file with the target word length and 4 composite 5x5 matrices (separated by `-----`)
2. Create a `glyphs_map.txt` file defining the 5x5 stroke patterns for each letter
3. Run the program and select Glyph Mode
4. Apply additional filters as needed

#### Example `glyphs_map.txt` format:

```
[A]
01010
10001
11111
10001
10001
---
01110
10001
11110
10001
01110
---
10101
10101
10101
10101
10101
---
10101
01010
10101
01010
10101

[B]
...
```

Each letter block contains 4 5x5 matrices separated by `---`:
1. Horizontal strokes (--)
2. Vertical strokes (||)
3. Slash strokes (/)
4. Backslash strokes (\)

### Help

View the comprehensive manual:

```bash
python wordsearch.py -h
```

or

```bash
python wordsearch.py --help
```

## File Structure

```
WordSearch/
├── wordsearch.py          # Main program
├── words_alpha.txt        # Dictionary file (370,000+ words)
├── glyphs_map.txt         # Glyph definitions for each letter (optional)
├── glyph_input.txt        # Input glyph matrices for analysis (optional)
└── README.md              # This file
```

## How It Works

### Word Mode Algorithm

1. Loads the complete word dictionary
2. Filters words by specified length
3. Applies each constraint:
   - Checks if word contains all required letters
   - Removes words with excluded letters
   - Verifies starting and ending letters
4. Returns matching words in alphabetical order

### Glyph Mode Algorithm

1. Parses input glyph matrices from `glyph_input.txt`
2. Loads glyph definitions from `glyphs_map.txt`
3. For each letter in the alphabet:
   - Checks if its stroke pattern is contained within the composite input
   - If all strokes match, adds the letter to the possible pool
4. Filters dictionary using possible letters and additional constraints
5. Returns matching words in alphabetical order

## Examples

### Example 1: Find 6-letter words starting with 'B'

```
Word Mode
Word length: 6
Contains: (skip)
Excludes: (skip)
Starts with: B
Ends with: (skip)
```

Result: BACONS, BADGES, BAGELS, BAILED, BAITED, BAKERS, BALLED, ...

### Example 2: Find 5-letter words with 'A' and 'E', excluding 'S'

```
Word Mode
Word length: 5
Contains: AE
Excludes: S
Starts with: (skip)
Ends with: (skip)
```

Result: ABODE, ACHED, ACNED, ADORE, AFIRE, AGILE, AGAVE, ...

## Performance

- Word lookup: ~1-2 seconds (varies by system and constraint complexity)
- Dictionary size: 370,000+ words
- Memory footprint: ~5-10 MB

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Improve documentation
- Add more test cases

## License

This project is open source and available under the MIT License.

## Author

Created by [bin4rythr33](https://github.com/bin4rythr33)

## Acknowledgments

- English word list sourced from [dwyl/english-words](https://github.com/dwyl/english-words)

## Troubleshooting

### Error: "Required wordlist file 'words_alpha.txt' was not found!"
- **Solution**: Download `words_alpha.txt` from the [dwyl/english-words repository](https://github.com/dwyl/english-words) and place it in the same directory as `wordsearch.py`

### Error: "Required glyph definition file 'glyphs_map.txt' was not found!"
- **Solution**: Create `glyphs_map.txt` with glyph definitions (only needed for Glyph Mode)

### No results found
- Try relaxing your constraints (remove excludes, skip starts_with/ends_with)
- Verify your input length is reasonable
- Check that at least some of your filter criteria match common English words
