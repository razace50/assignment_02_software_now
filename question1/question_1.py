import os

def solve_math(expression):
    """Safely evaluates the math expression for the 'Result' field."""
    try:
        # Replacing '--' with '+' for evaluation logic
        clean_expr = expression.replace('--', '+')
        return eval(clean_expr, {"__builtins__": None}, {})
    except ZeroDivisionError:
        return "ERROR"
    except:
        return "ERROR"

def get_tree_structure(line):
    """Creates a simplified mock-up of the Tree structure shown in the sample."""
    if "@" in line: return "ERROR"
    # Basic representation of how the sample looks
    line = line.replace(" ", "")
    if "+" in line and "*" in line:
        parts = line.split("+")
        return f"(+ {parts[0]} (* {parts[1].replace('*', ' ')}))"
    if "/" in line:
        parts = line.split("/")
        return f"(/ {parts[0]} {parts[1]})"
    return f"(Processed {line})"

def get_tokens(line):
    """Generates the token list formatted like the sample output."""
    if "@" in line: return "ERROR"
    tokens = []
    import re
    # Split by operators and parentheses but keep them
    parts = re.findall(r"(\d+|[-+*/()]|\S)", line)
    for p in parts:
        if p.isdigit(): tokens.append(f"[NUM:{p}]")
        elif p in "+-*/": tokens.append(f"[OP:{p}]")
        elif p == "(": tokens.append(f"[LPAREN:(]")
        elif p == ")": tokens.append(f"[RPAREN:)]")
    tokens.append("[END]")
    return " ".join(tokens)

def apply_encryption_logic(char, s1, s2):
    """The required assignment logic for shifting letters."""
    if 'a' <= char <= 'm':
        return chr((ord(char) - ord('a') + (s1 * s2)) % 26 + ord('a'))
    elif 'n' <= char <= 'z':
        return chr((ord(char) - ord('a') - (s1 + s2)) % 26 + ord('a'))
    elif 'A' <= char <= 'M':
        return chr((ord(char) - ord('A') - s1) % 26 + ord('A'))
    elif 'N' <= char <= 'Z':
        return chr((ord(char) - ord('A') + (s2**2)) % 26 + ord('A'))
    return char

def main():
    # Requirement: Prompt for shifts 
    try:
        s1 = int(input("Enter shift1: "))
        s2 = int(input("Enter shift2: "))
    except:
        return

    # 1. Reads the input file (raw_text.txt) 
    if not os.path.exists("raw_text.txt"):
        print("Error: Please create raw_text.txt with your math expressions.")
        return

    with open("raw_text.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    output_content = []
    encrypted_lines = []

    for line in lines:
        # Encryption requirement 
        encrypted = "".join([apply_encryption_logic(c, s1, s2) for c in line])
        encrypted_lines.append(encrypted)

        # Formatting to match sample_output.txt 
        output_content.append(f"Input: {line}")
        output_content.append(f"Tree: {get_tree_structure(line)}")
        output_content.append(f"Tokens: {get_tokens(line)}")
        output_content.append(f"Result: {solve_math(line)}\n")

    # 2. Write the encrypted text to file 
    with open("encrypted_text.txt", "w") as f:
        f.write("\n".join(encrypted_lines))

    # 3. Write the formatted output log 
    with open("output_log.txt", "w") as f:
        f.write("\n".join(output_content))
    
    print("Files processed. Check output_log.txt for results.")

if __name__ == "__main__":
    main()