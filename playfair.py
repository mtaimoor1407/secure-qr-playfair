# ══════════════════════════════════════════
#  PLAYFAIR CIPHER — PYTHON IMPLEMENTATION
# ══════════════════════════════════════════

def build_grid(keyword):
    keyword = keyword.upper().replace("J", "I")
    keyword = ''.join(c for c in keyword if c.isalpha())
    seen = set()
    grid = []
    for ch in keyword:
        if ch not in seen:
            seen.add(ch)
            grid.append(ch)
    for i in range(65, 91):
        ch = chr(i)
        if ch == "J":
            continue
        if ch not in seen:
            seen.add(ch)
            grid.append(ch)
    return grid


def get_pos(grid, letter):
    idx = grid.index(letter)
    return idx // 5, idx % 5


def prepare_text(text):
    text = text.upper().replace("J", "I")
    text = ''.join(c for c in text if c.isalpha())
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 >= len(text):
            b = "X"
            i += 1
        elif text[i] == text[i + 1]:
            b = "X"
            i += 1
        else:
            b = text[i + 1]
            i += 2
        pairs.append((a, b))
    return pairs


def encrypt_pair(grid, a, b):
    ra, ca = get_pos(grid, a)
    rb, cb = get_pos(grid, b)
    if ra == rb:
        # Same row — shift right
        return grid[ra * 5 + (ca + 1) % 5], grid[rb * 5 + (cb + 1) % 5]
    elif ca == cb:
        # Same column — shift down
        return grid[((ra + 1) % 5) * 5 + ca], grid[((rb + 1) % 5) * 5 + cb]
    else:
        # Rectangle — swap corners
        return grid[ra * 5 + cb], grid[rb * 5 + ca]


def decrypt_pair(grid, a, b):
    ra, ca = get_pos(grid, a)
    rb, cb = get_pos(grid, b)
    if ra == rb:
        # Same row — shift left
        return grid[ra * 5 + (ca - 1) % 5], grid[rb * 5 + (cb - 1) % 5]
    elif ca == cb:
        # Same column — shift up
        return grid[((ra - 1) % 5) * 5 + ca], grid[((rb - 1) % 5) * 5 + cb]
    else:
        # Rectangle — swap corners
        return grid[ra * 5 + cb], grid[rb * 5 + ca]


def clean_decrypted(text):
    # Remove trailing X padding
    if text.endswith("X"):
        text = text[:-1]
    # Remove X inserted between duplicate letters
    result = ""
    i = 0
    while i < len(text):
        if (text[i] == "X" and
                i > 0 and
                i < len(text) - 1 and
                text[i - 1] == text[i + 1]):
            i += 1
            continue
        result += text[i]
        i += 1
    return result


def encrypt(message, keyword):
    grid = build_grid(keyword)
    pairs = prepare_text(message)
    result = []
    for a, b in pairs:
        ca, cb = encrypt_pair(grid, a, b)
        result.extend([ca, cb])
    return ''.join(result)


def decrypt(cipher, keyword):
    grid = build_grid(keyword)
    cipher = cipher.upper()
    cipher = ''.join(c for c in cipher if c.isalpha())
    pairs = []
    for i in range(0, len(cipher) - 1, 2):
        pairs.append((cipher[i], cipher[i + 1]))
    result = []
    for a, b in pairs:
        da, db = decrypt_pair(grid, a, b)
        result.extend([da, db])
    raw = ''.join(result)
    return clean_decrypted(raw)


def get_grid_data(keyword):
    grid = build_grid(keyword)
    # Return as 5x5 list of rows
    return [grid[i * 5:(i + 1) * 5] for i in range(5)]


def get_encryption_steps(message, keyword):
    grid = build_grid(keyword)
    pairs = prepare_text(message)
    steps = []
    for a, b in pairs:
        ra, ca = get_pos(grid, a)
        rb, cb = get_pos(grid, b)
        ca_enc, cb_enc = encrypt_pair(grid, a, b)
        if ra == rb:
            rule = "Same Row → shift right"
        elif ca == cb:
            rule = "Same Column → shift down"
        else:
            rule = "Rectangle → swap corners"
        steps.append({
            "pair": a + b,
            "encrypted": ca_enc + cb_enc,
            "rule": rule
        })
    return steps


def get_keyword_strength(keyword):
    keyword = ''.join(c for c in keyword if c.isalpha())
    score = 0
    unique = len(set(keyword.upper()))
    if len(keyword) >= 3:  score += 1
    if len(keyword) >= 6:  score += 1
    if len(keyword) >= 10: score += 1
    if unique >= 4: score += 1
    if unique >= 7: score += 1
    vowels = set("AEIOU")
    has_vowel = any(c.upper() in vowels for c in keyword)
    has_consonant = any(c.upper() not in vowels for c in keyword)
    if has_vowel and has_consonant: score += 1
    return score  # 0 to 6