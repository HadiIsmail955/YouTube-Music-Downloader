def print_menu():
    print("""
What do you want to download?

1) All albums
2) All singles
3) Albums + singles
4) Everything
5) Pick specific album(s)
6) Pick specific playlist(s)
7) Pick specific song(s)
8) Paste a direct link
9) Exit
10) Update / check for new content
""")


def pick_items(items, label):
    print(f"\nAvailable {label}:")
    for i, item in enumerate(items, 1):
        print(f"[{i}] {item['title']}")

    choices = input("\nEnter numbers (comma-separated): ")
    indexes = []

    for c in choices.split(","):
        c = c.strip()
        if c.isdigit():
            idx = int(c) - 1
            if 0 <= idx < len(items):
                indexes.append(idx)

    return [items[i] for i in indexes]
