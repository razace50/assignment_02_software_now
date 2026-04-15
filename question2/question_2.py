import os

# -------- TOKENIZER -------- #

def tokenize(expr):
    tokens = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        if ch.isspace():
            i += 1
            continue

       if ch.isdigit():
    num = ch
    dot_seen = False  
    i += 1
    while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
        if expr[i] == '.':
            if dot_seen:   # ---- prevent multiple dots-----
                return None
            dot_seen = True
        num += expr[i]
        i += 1
    tokens.append(("NUM", float(num)))
    continue
        if ch in "+-*/":
            tokens.append(("OP", ch))
            i += 1
            continue

        if ch == "(":
            tokens.append(("LPAREN", ch))
            i += 1
            continue

        if ch == ")":
            tokens.append(("RPAREN", ch))
            i += 1
            continue

        # invalid character found
        return None

    tokens.append(("END", None))
    return tokens


# -------- PARSER (Recursive Descent) -------- #

def parse(tokens):
    pos = 0

    def peek():
        return tokens[pos]

    def consume():
        nonlocal pos
        t = tokens[pos]
        pos += 1
        return t

    def parse_factor():
        t = peek()

        # unary minus
        if t[0] == "OP" and t[1] == "-":
            consume()
            node = parse_factor()
            return ("neg", node)

        if t[0] == "NUM":
            consume()
            return ("num", t[1])

        if t[0] == "LPAREN":
            consume()
            node = parse_expr()
            if peek()[0] != "RPAREN":
                raise Exception("Missing closing bracket")
            consume()
            return node

        raise Exception("Invalid expression")

    def parse_term():
        node = parse_factor()

        while True:
            t = peek()

            # implicit multiplication (like 2(3+4))
            if t[0] in ("NUM", "LPAREN"):
                right = parse_factor()
                node = ("*", node, right)
                continue

            if t[0] == "OP" and t[1] in "*/":
                op = consume()[1]
                right = parse_factor()
                node = (op, node, right)
            else:
                break

        return node

    def parse_expr():
        node = parse_term()

        while True:
            t = peek()
            if t[0] == "OP" and t[1] in "+-":
                op = consume()[1]
                right = parse_term()
                node = (op, node, right)
            else:
                break

        return node

    tree = parse_expr()

    if peek()[0] != "END":
        raise Exception("Extra input at end")

    return tree


# -------- TREE FORMAT -------- #

def format_tree(node):
    if node[0] == "num":
        val = node[1]
        return str(int(val)) if val.is_integer() else str(round(val, 4))

    if node[0] == "neg":
        return f"(neg {format_tree(node[1])})"

    op, left, right = node
    return f"({op} {format_tree(left)} {format_tree(right)})"


# -------- EVALUATION -------- #

def evaluate(node):
    if node[0] == "num":
        return node[1]

    if node[0] == "neg":
        return -evaluate(node[1])

    op, left, right = node
    l = evaluate(left)
    r = evaluate(right)

    if op == "+":
        return l + r
    if op == "-":
        return l - r
    if op == "*":
        return l * r
    if op == "/":
        if r == 0:
            raise Exception("Division by zero")
        return l / r


# -------- TOKEN STRING FORMAT -------- #

def tokens_to_string(tokens):
    parts = []

    for t in tokens:
        if t[0] == "NUM":
            val = int(t[1]) if t[1].is_integer() else t[1]
            parts.append(f"[NUM:{val}]")

        elif t[0] == "OP":
            parts.append(f"[OP:{t[1]}]")

        elif t[0] == "LPAREN":
            parts.append("[LPAREN:(]")

        elif t[0] == "RPAREN":
            parts.append("[RPAREN:)]")

        elif t[0] == "END":
            parts.append("[END]")

    return " ".join(parts)


# -------- MAIN FUNCTION -------- #

def evaluate_file(input_path: str):
    results = []

    output_path = os.path.join(os.path.dirname(input_path), "output.txt")

    with open(input_path, "r") as f:
        lines = f.readlines()

    with open(output_path, "w") as out:
        for line in lines:
            expr = line.strip()

            if not expr:
                continue

            try:
                tokens = tokenize(expr)
                if tokens is None:
                    raise Exception()

                tree = parse(tokens)
                value = evaluate(tree)

                tree_str = format_tree(tree)
                token_str = tokens_to_string(tokens)

                if value == int(value):
                    value = int(value)
                else:
                    value = round(value, 4)

            except:
                tree_str = "ERROR"
                token_str = "ERROR"
                value = "ERROR"

            out.write(f"Input: {expr}\n")
            out.write(f"Tree: {tree_str}\n")
            out.write(f"Tokens: {token_str}\n")
            out.write(f"Result: {value}\n\n")

            results.append({
                "input": expr,
                "tree": tree_str,
                "tokens": token_str,
                "result": value
            })

    return results


# -------- RUN PROGRAM -------- #

if __name__ == "__main__":
    evaluate_file("input.txt")