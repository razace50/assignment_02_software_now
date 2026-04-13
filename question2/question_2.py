import os

def tokenize(expression):
    """
    Manually converts the input string into a list of tokens.
    Uses basic loops and branching to identify NUM, OP, and PAREN.
    """
    tokens = []
    i = 0
    expression = expression.strip()
    
    while i < len(expression):
        char = expression[i]
        
        if char.isspace():
            i += 1
            continue
            
        if char.isdigit() or char == '.':
            num_str = ""
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num_str += expression[i]
                i += 1
            tokens.append(('NUM', num_str))
            continue
            
        if char in "+-*/":
            tokens.append(('OP', char))
        elif char == '(':
            tokens.append(('LPAREN', '('))
        elif char == ')':
            tokens.append(('RPAREN', ')'))
        else:
            return None
        i += 1
        
    tokens.append(('END', ''))
    return tokens

def format_tokens(tokens):
    if tokens is None: return "ERROR"
    parts = []
    for t_type, t_val in tokens:
        if t_type == 'END':
            parts.append("[END]")
        else:
            parts.append(f"[{t_type}:{t_val}]")
    return " ".join(parts)

# FIX 1: Use a variable 'input_path' here instead of a string literal
def evaluate_file(input_path):
    output_data = []
    
    def parse_expression(token_list, index):
        idx, left_tree, left_val = parse_term(token_list, index)
        while idx < len(token_list) and token_list[idx][0] == 'OP' and token_list[idx][1] in "+-":
            op = token_list[idx][1]
            idx, right_tree, right_val = parse_term(token_list, idx + 1)
            left_tree = f"({op} {left_tree} {right_tree})"
            if op == '+': left_val += right_val
            else: left_val -= right_val
        return idx, left_tree, left_val

    def parse_term(token_list, index):
        idx, left_tree, left_val = parse_factor(token_list, index)
        while idx < len(token_list):
            op = None
            if token_list[idx][0] == 'OP' and token_list[idx][1] in "*/":
                op = token_list[idx][1]
                idx += 1
            elif token_list[idx][0] in ['LPAREN', 'NUM']:
                op = '*'
            else:
                break
            idx, right_tree, right_val = parse_factor(token_list, idx)
            left_tree = f"({op} {left_tree} {right_tree})"
            if op == '*': 
                left_val *= right_val
            else:
                if right_val == 0: raise ZeroDivisionError
                left_val /= right_val
        return idx, left_tree, left_val

    def parse_factor(token_list, index):
        if token_list[index][0] == 'OP':
            if token_list[index][1] == '-':
                idx, tree, val = parse_factor(token_list, index + 1)
                return idx, f"(neg {tree})", -val
            elif token_list[index][1] == '+':
                raise ValueError("Unary + not supported")
        return parse_primary(token_list, index)

    def parse_primary(token_list, index):
        token_type, token_val = token_list[index]
        if token_type == 'NUM':
            v = float(token_val)
            display_val = str(int(v)) if v.is_integer() else str(v)
            return index + 1, display_val, v
        if token_type == 'LPAREN':
            idx, tree, val = parse_expression(token_list, index + 1)
            if token_list[idx][0] != 'RPAREN':
                raise Exception("Missing RPAREN")
            return idx + 1, tree, val
        raise Exception("Unexpected Token")

    # FIX 2: Use the variable 'input_path' to open the file
    try:
        with open(input_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    # FIX 3: Correctly identify the directory to save output.txt 
    output_dir = os.path.dirname(input_path)
    output_file_path = os.path.join(output_dir, "output.txt") if output_dir else "output.txt"
    
    with open(output_file_path, 'w') as out_f:
        for line in lines:
            raw_input = line.strip()
            if not raw_input: continue
            
            tokens = tokenize(raw_input)
            entry = {"input": raw_input, "tree": "ERROR", "tokens": format_tokens(tokens), "result": "ERROR"}
            
            if tokens:
                try:
                    _, res_tree, res_val = parse_expression(tokens, 0)
                    entry["tree"] = res_tree
                    entry["result"] = res_val
                except:
                    pass 

            output_data.append(entry)
            
            out_f.write(f"Input: {entry['input']}\n")
            out_f.write(f"Tree: {entry['tree']}\n")
            out_f.write(f"Tokens: {entry['tokens']}\n")
            
            res_str = entry["result"]
            if isinstance(res_str, float):
                if res_str.is_integer():
                    res_str = str(int(res_str))
                else:
                    res_str = f"{res_str:.4f}".rstrip('0').rstrip('.')
            
            out_f.write(f"Result: {res_str}\n\n")

    return output_data

# RUNNING THE CODE
if __name__ == "__main__":
    # Based on your file structure, 'input.txt' is in the same folder [cite: 3, 4]
   results = evaluate_file("input.txt")
   import os
   print(f"Success! Output file is created at: {os.path.abspath('output.txt ')}")