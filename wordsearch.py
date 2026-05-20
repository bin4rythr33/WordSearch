import os
import string
import sys

# Global configuration variables for local files
WORDLIST_FILE = "words_alpha.txt" # Sourced from "https://github.com/dwyl/english-words/blob/master/words_alpha.txt"
GLYPH_MAP_FILE = "glyphs_map.txt"
GLYPH_INPUT_FILE = "glyph_input.txt" # Edit content of this file with target glyph. 

# Help
def show_guidance():
    """Prints the comprehensive guidance, usage rules, and examples."""
    guidance_text = """
=======================================================================================================
                                 WORDSEARCH HELPER MANUAL (-h)
=======================================================================================================
Description:
  This tool helps you find valid dictionary words or process matrix glyph maps for guessing games.
  It filters an offline database of over 370,000+ words matching your specific requirements.

Operational Modes:
  1. Word Mode  : Performs comprehensive dictionary word lookups matching lengths and filters.
  2. Glyph Mode : Reads a composite multi-letter glyph array from glyph_input.txt, extracts all 
                  possible constituent letters, and searches the local dictionary for matching words.

Input Constraints & Formatting Rules:
  - Word Length  : Must be a mandatory positive integer greater than 0.
  - Filter Inputs: Characters are case-insensitive. All outputs are processed and shown in UPPERCASE.
  - Glyph Inputs : Loaded via 'glyph_input.txt' using space-separated blocks and '-----' dividers.
=======================================================================================================
by bin4rythr33 (https://github.com/bin4rythr33)
=======================================================================================================
"""
    print(guidance_text)


# Load words_alpha.txt
def load_local_wordlist():
    """Loads the dictionary from the local file path. Throws error if missing."""
    if not os.path.exists(WORDLIST_FILE):
        print(f"\n[ERROR]: Required wordlist file '{WORDLIST_FILE}' was not found!", file=sys.stderr)
        print(f"Please place your downloaded file inside: {os.getcwd()}", file=sys.stderr)
        sys.exit(1)

    with open(WORDLIST_FILE, "r", encoding="utf-8") as f:
        return set(line.strip().upper() for line in f if line.strip())

# Load glyph_map.txt
def load_dual_glyph_mapping():
    """Parses custom file containing exactly 4 stroke matrices per alphabet letter, forcing keys to uppercase."""
    if not os.path.exists(GLYPH_MAP_FILE):
        print(f"\n[ERROR]: Required glyph definition file '{GLYPH_MAP_FILE}' was not found!", file=sys.stderr)
        print(f"Please create '{GLYPH_MAP_FILE}' inside: {os.getcwd()}", file=sys.stderr)
        sys.exit(1)

    glyph_dict = {}
    current_char = None
    character_lines = []

    with open(GLYPH_MAP_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            
            if not line or line.startswith("#"):
                continue
            
            if line.startswith("[") and line.endswith("]"):
                if current_char and character_lines:
                    glyph_dict[current_char] = process_character_block(current_char, character_lines)
                
                current_char = line[1:-1].upper()
                character_lines = []
            else:
                character_lines.append(line)
                
        if current_char and character_lines:
            glyph_dict[current_char] = process_character_block(current_char, character_lines)

    return glyph_dict

# glyph character processor
def process_character_block(char_name, line_list):
    """Splits a single character text block into 4 distinct 5x5 stroke matrices."""
    full_block = "\n".join(line_list)
    
    if "---" not in full_block:
        print(f"[FORMAT ERROR]: Letter '[{char_name}]' missing the '---' array separation dividers.", file=sys.stderr)
        sys.exit(1)
        
    parts = full_block.split("---")
    
    if len(parts) != 4:
        print(f"[FORMAT ERROR]: Letter '[{char_name}]' must have exactly 4 stroke arrays (-, |, /, \\). Found {len(parts)}.", file=sys.stderr)
        sys.exit(1)
        
    horizontal_matrix = [row.strip() for row in parts[0].strip().split("\n") if row.strip()]
    vertical_matrix = [row.strip() for row in parts[1].strip().split("\n") if row.strip()]
    slash_matrix = [row.strip() for row in parts[2].strip().split("\n") if row.strip()]
    backslash_matrix = [row.strip() for row in parts[3].strip().split("\n") if row.strip()]
    
    matrices = [horizontal_matrix, vertical_matrix, slash_matrix, backslash_matrix]
    labels = ["Horizontal", "Vertical", "Slash", "Backslash"]
    
    for idx, mat in enumerate(matrices):
        if len(mat) != 5:
            print(f"[DATA ERROR]: {labels[idx]} matrix in '[{char_name}]' must have exactly 5 rows. Found {len(mat)}.", file=sys.stderr)
            sys.exit(1)
        for r_idx, row in enumerate(mat, 1):
            if len(row) != 5:
                print(f"[DATA ERROR]: Row {r_idx} of {labels[idx]} matrix in '[{char_name}]' must be exactly 5 columns wide. Found {len(row)}.", file=sys.stderr)
                sys.exit(1)
        
    return {
        "horizontal": horizontal_matrix,
        "vertical": vertical_matrix,
        "slash": slash_matrix,
        "backslash": backslash_matrix
    }

# Load glyph_input.txt
def parse_glyph_input_file():
    """Reads glyph_input.txt and extracts word length and 4 distinct 5x5 composite matrices."""
    if not os.path.exists(GLYPH_INPUT_FILE):
        print(f"\n[ERROR]: Input file '{GLYPH_INPUT_FILE}' was not found!", file=sys.stderr)
        print(f"Please create it inside: {os.getcwd()}", file=sys.stderr)
        sys.exit(1)

    with open(GLYPH_INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        print(f"[INPUT ERROR]: '{GLYPH_INPUT_FILE}' is completely empty.", file=sys.stderr)
        sys.exit(1)

    tokens = content.split()

    try:
        word_length = int(tokens[0])
        if word_length <= 0:
            raise ValueError
    except (ValueError, IndexError):
        print("[INPUT ERROR]: The first entry in glyph_input.txt must be a positive integer word length.", file=sys.stderr)
        sys.exit(1)

    matrix_payload = " ".join(tokens[1:])
    parts = matrix_payload.split("-----")

    if len(parts) != 4:
        print(f"[INPUT ERROR]: Expected exactly 4 matrices separated by '-----'. Found {len(parts)}.", file=sys.stderr)
        sys.exit(1)

    matrices = []
    labels = ["Horizontal", "Vertical", "Slash", "Backslash"]

    for idx, raw_part in enumerate(parts):
        rows = raw_part.split()
        if len(rows) != 5:
            print(f"[INPUT ERROR]: {labels[idx]} matrix must have exactly 5 rows. Found {len(rows)}.", file=sys.stderr)
            sys.exit(1)
        for r_idx, row in enumerate(rows, 1):
            if len(row) != 5 or not all(char in "01" for char in row):
                print(f"[INPUT ERROR]: Row {r_idx} of {labels[idx]} matrix must be 5 binary bits wide.", file=sys.stderr)
                sys.exit(1)
        matrices.append(rows)

    return word_length, matrices[0], matrices[1], matrices[2], matrices[3]

# Alphabet letter checker via glyph strokes
def is_glyph_contained(letter_stroke, composite_input):
    """Checks if all active ('1') bits of a base letter are satisfied by the composite input glyph matrix."""
    for r in range(5):
        for c in range(5):
            if letter_stroke[r][c] == "1" and composite_input[r][c] != "1":
                return False
    return True

# Generate glyph for display
def generate_combined_preview(h_arr, v_arr, s_arr, b_arr):
    """Layers the 4 distinct 5x5 structural arrays together, doubling each stroke 

    horizontally and doubling each row vertically.
    Priority sequence display layout order matches: || // -- \\
    """
    print("\n--- Preview of Combined 5x5 Composite Input Array ---")
    
    for r_idx in range(5):
        row_chars = []
        for c_idx in range(5):
            h_bit = h_arr[r_idx][c_idx] == "1"
            v_bit = v_arr[r_idx][c_idx] == "1"
            s_bit = s_arr[r_idx][c_idx] == "1"
            b_bit = b_arr[r_idx][c_idx] == "1"
            
            active_symbols = []
            if v_bit: active_symbols.append("||")
            if s_bit: active_symbols.append("//")
            if h_bit: active_symbols.append("--")
            if b_bit: active_symbols.append("\\\\")
            
            if len(active_symbols) == 0:
                row_chars.append("  ")
            elif len(active_symbols) == 1:
                row_chars.append(active_symbols[0])
            else:
                row_chars.append("".join(active_symbols))
                
        compiled_line = "  " + "  ".join(row_chars)
        print(compiled_line)
        print(compiled_line)


def generate_preview_from_letters(letters, glyphs_map):
    """Builds a composite 5x5 glyph from multiple alphabet letters and prints the preview.

    Args:
        letters: iterable or string of alphabet letters to combine (e.g., "ABC" or ["A","B"]).
        glyphs_map: mapping returned by `load_dual_glyph_mapping()` containing stroke matrices.

    Returns:
        A tuple of four lists (horizontal, vertical, slash, backslash) each containing 5 string rows.
    """
    comp_h = [["0"] * 5 for _ in range(5)]
    comp_v = [["0"] * 5 for _ in range(5)]
    comp_s = [["0"] * 5 for _ in range(5)]
    comp_b = [["0"] * 5 for _ in range(5)]

    for ch in letters:
        if not ch:
            continue
        ch = ch.upper()
        if ch not in glyphs_map:
            print(f"[WARN]: Letter '{ch}' not found in glyph map; skipping.")
            continue

        stroke = glyphs_map[ch]
        for r in range(5):
            for c in range(5):
                if stroke["horizontal"][r][c] == "1":
                    comp_h[r][c] = "1"
                if stroke["vertical"][r][c] == "1":
                    comp_v[r][c] = "1"
                if stroke["slash"][r][c] == "1":
                    comp_s[r][c] = "1"
                if stroke["backslash"][r][c] == "1":
                    comp_b[r][c] = "1"

    h_rows = ["".join(row) for row in comp_h]
    v_rows = ["".join(row) for row in comp_v]
    s_rows = ["".join(row) for row in comp_s]
    b_rows = ["".join(row) for row in comp_b]

    generate_combined_preview(h_rows, v_rows, s_rows, b_rows)

    return h_rows, v_rows, s_rows, b_rows


def compare_composite_outputs(a, b):
    """Compare two composite glyph outputs and return True if they match exactly.

    Args:
        a, b: Each should be an iterable/tuple of four matrices in the order
              (horizontal, vertical, slash, backslash). Each matrix may be
              a list of 5 strings (e.g. '01010') or a list of 5 lists of '0'/'1'.

    Returns:
        True if all four matrices match exactly row-for-row, False otherwise.
    """
    def _normalize(mat):
        if mat is None or not isinstance(mat, (list, tuple)):
            return None
        rows = []
        for row in mat:
            if isinstance(row, str):
                rows.append(row)
            else:
                rows.append("".join(str(c) for c in row))
        return rows

    if not (isinstance(a, (list, tuple)) and isinstance(b, (list, tuple))):
        return False
    if len(a) != 4 or len(b) != 4:
        return False

    for i in range(4):
        ma = _normalize(a[i])
        mb = _normalize(b[i])
        if ma is None or mb is None:
            return False
        if len(ma) != 5 or len(mb) != 5:
            return False
        for r in range(5):
            if ma[r] != mb[r]:
                return False

    return True


def build_composite_from_letters(letters, glyphs_map):
    """Build composite 5x5 stroke matrices from given letters (no preview).

    Args:
        letters: iterable or string of letters.
        glyphs_map: mapping from `load_dual_glyph_mapping()`.

    Returns:
        Tuple of four lists: (horizontal_rows, vertical_rows, slash_rows, backslash_rows)
    """
    comp_h = [["0"] * 5 for _ in range(5)]
    comp_v = [["0"] * 5 for _ in range(5)]
    comp_s = [["0"] * 5 for _ in range(5)]
    comp_b = [["0"] * 5 for _ in range(5)]

    for ch in letters:
        if not ch:
            continue
        ch = ch.upper()
        if ch not in glyphs_map:
            continue
        stroke = glyphs_map[ch]
        for r in range(5):
            for c in range(5):
                if stroke["horizontal"][r][c] == "1":
                    comp_h[r][c] = "1"
                if stroke["vertical"][r][c] == "1":
                    comp_v[r][c] = "1"
                if stroke["slash"][r][c] == "1":
                    comp_s[r][c] = "1"
                if stroke["backslash"][r][c] == "1":
                    comp_b[r][c] = "1"

    h_rows = ["".join(row) for row in comp_h]
    v_rows = ["".join(row) for row in comp_v]
    s_rows = ["".join(row) for row in comp_s]
    b_rows = ["".join(row) for row in comp_b]

    return h_rows, v_rows, s_rows, b_rows


def find_words_matching_input_glyph(possible_words, input_glyph, glyphs_map=None):
    """Return list of words whose composite glyph equals `input_glyph` exactly.

    Args:
        possible_words: iterable of words (strings) to test.
        input_glyph: four matrices [horizontal, vertical, slash, backslash], each list of 5 strings.
        glyphs_map: optional glyph mapping; if None it will be loaded.

    Returns:
        List of words from `possible_words` whose built composite matches `input_glyph`.
    """
    if glyphs_map is None:
        glyphs_map = load_dual_glyph_mapping()

    matches = []
    # Normalize input_glyph into same shape expected by compare_composite_outputs
    target = input_glyph

    for w in possible_words:
        comp = build_composite_from_letters(w, glyphs_map)
        if compare_composite_outputs(comp, target):
            matches.append(w)

    return matches


def save_glyph_output(results, filename="glyph.output.txt"):
    """Save a word list to a file in the current script directory and return the file path."""
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
        if results:
            f.write("\n")
    return output_path

# Alphabet character Checker
def get_valid_alpha_input(prompt_message):
    """Prompt user for optional alphabetic input, rejecting non-alphabets and converting to uppercase."""
    while True:
        user_input = input(prompt_message).strip()
        if not user_input:
            return ""
        if user_input.isalpha():
            return user_input.upper()
        print("[INPUT ERROR]: Invalid characters detected. Please enter letters only.")

# Function to filter words based on constraints
def filter_words_by_constraints(word_length, possible_letters, contains="", excludes="", starts_with="", ends_with=""):
    """Filters words from dictionary based on length, character pool, and optional constraints.
    
    Args:
        word_length: Target word length
        possible_letters: Set/list of allowed letters to search within
        contains: Letters that MUST exist in the word
        excludes: Letters that MUST NOT exist in the word
        starts_with: Optional starting letter
        ends_with: Optional ending letter
    
    Returns:
        Sorted list of matching words
    """
    raw_words = load_local_wordlist()
    possible_set = set(possible_letters) if possible_letters else set(string.ascii_uppercase)
    contains_set = set(contains.upper()) if contains else set()
    excludes_set = set(excludes.upper()) if excludes else set()
    starts_with = starts_with.upper() if starts_with else ""
    ends_with = ends_with.upper() if ends_with else ""
    
    matching_words = []
    
    for word in raw_words:
        # Check length
        if len(word) != word_length:
            continue
        
        # Check if word is alphabetic
        if not word.isalpha():
            continue
        
        word_upper = word.upper()
        word_set = set(word_upper)
        
        # Check if word only uses letters from possible_letters pool
        if not word_set.issubset(possible_set):
            continue
        
        # Check contains constraint
        if contains_set and not contains_set.issubset(word_set):
            continue
        
        # Check excludes constraint
        if excludes_set and not word_set.isdisjoint(excludes_set):
            continue
        
        # Check starts_with constraint
        if starts_with and not word_upper.startswith(starts_with):
            continue
        
        # Check ends_with constraint
        if ends_with and not word_upper.endswith(ends_with):
            continue
        
        matching_words.append(word_upper)
    
    return sorted(matching_words)

# Display results
def display_word_results(results):
    """Displays word search results.
    
    Args:
        results: List of matching words
    """
    print(f"\nFound {len(results)} matching dictionary words (Alphabetical Order):")
    if results:
        print("\n".join(results))
    else:
        print("No matching dictionary words found.")

# Word Mode Workflow
def run_word_mode():
    # Retained standard word mode flow
    print("\n--- Word Mode Configuration ---")
    while True:
        try:
            length_input = input("Enter mandatory word length: ").strip()
            length = int(length_input)
            if length > 0:
                break
            print("[INPUT ERROR]: Word length must be a positive integer greater than 0.")
        except ValueError:
            print("[INPUT ERROR]: Invalid format. Please enter a valid number.")

    contains = get_valid_alpha_input("Enter letters that MUST exist in the word (or press enter to skip): ")
    excludes = get_valid_alpha_input("Enter letters that MUST NOT exist in the word (or press enter to skip): ")
    starts_with = get_valid_alpha_input("Enter the known starting letter (or press enter to skip): ")
    ends_with = get_valid_alpha_input("Enter the known ending letter (or press enter to skip): ")
    
    # Use common function to filter and get results
    results = filter_words_by_constraints(
        word_length=length,
        possible_letters=set(string.ascii_uppercase),
        contains=contains,
        excludes=excludes,
        starts_with=starts_with,
        ends_with=ends_with
    )
    
    # Display results
    display_word_results(results)


# Glyph mode Workflow
def run_glyph_mode():
    """Reads composite arrays from glyph_input.txt, discovers subset letters, and finds cross-referenced dictionary words."""
    print("\n--- Glyph Mode Activation (Composite Matrix Stream) ---")
    
    # Step 1: Parse the stacked input matrices
    word_length, user_h, user_v, user_s, user_b = parse_glyph_input_file()
    print(f"Loaded Target Word Length from file: {word_length}")
    
    # Step 2: Load dictionary character blueprints
    glyphs = load_dual_glyph_mapping()
    
    # Step 3: Print visual composite layout
    generate_combined_preview(user_h, user_v, user_s, user_b)

    input_glyph = [user_h, user_v, user_s, user_b]
    
    # Step 4: Discover all alphabet sub-components hidden in the composite array
    possible_letters = []
    for character, stroke_data in glyphs.items():
        if (is_glyph_contained(stroke_data["horizontal"], user_h) and
            is_glyph_contained(stroke_data["vertical"], user_v) and
            is_glyph_contained(stroke_data["slash"], user_s) and
            is_glyph_contained(stroke_data["backslash"], user_b)):
            possible_letters.append(character.upper())

    print(f"\n--- Resolved Constituent Alphabet Pool ---")
    if not possible_letters:
        print("No matching alphabet components fit within this visual glyph signature.")
        return
    
    print(f"Possible letters found hidden inside input glyph: {', '.join(sorted(possible_letters))}")
    
    # Step 5: Request for user inputs for optional constraints
    contains = get_valid_alpha_input("Enter letters that MUST exist in the word (or press enter to skip): ")
    excludes = get_valid_alpha_input("Enter letters that MUST NOT exist in the word (or press enter to skip): ")
    starts_with = get_valid_alpha_input("Enter the known starting letter (or press enter to skip): ")
    ends_with = get_valid_alpha_input("Enter the known ending letter (or press enter to skip): ")
    
    # Step 6: Use common function to filter and get results
    possible_words = filter_words_by_constraints(
        word_length=word_length,
        possible_letters=possible_letters,
        contains=contains,
        excludes=excludes,
        starts_with=starts_with,
        ends_with=ends_with
    )

    results = find_words_matching_input_glyph(
        possible_words=possible_words,
        input_glyph=input_glyph,
        glyphs_map=glyphs
    )

    if results:
        output_path = save_glyph_output(results)
        print(f"\nExact glyph matches saved to: {output_path}")
        display_word_results(results)
    else:
        output_path = save_glyph_output(possible_words)
        print("\n[NOTICE]: No exact glyph match word found. Outputting fallback possible words instead.")
        print(f"Possible words saved to: {output_path}")
        display_word_results(possible_words)

def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        show_guidance()
        sys.exit(0)

    print("=========================================")
    print("Welcome to WordSearch Engine Console")
    print("=========================================")
    print("Please select an operational mode:")
    print("  1. Word Mode")
    print("  2. Glyph Mode")
    print("=========================================")
    
    while True:
        mode_choice = input("Enter your selection (1/2 or Word/Glyph): ").strip().upper()
        if mode_choice in ["1", "WORD"]:
            run_word_mode()
            break
        elif mode_choice in ["2", "GLYPH"]:
            run_glyph_mode()
            break
        else:
            print("Invalid selection. Please enter '1', '2', 'Word', or 'Glyph'.")


if __name__ == "__main__":
    main()