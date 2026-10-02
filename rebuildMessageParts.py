def rebuildMessageParts(parts):
    # Map the first character of each part to that part
    starts_with = {}

    for part in parts:
        starts_with[part[0]] = part
    print(starts_with)

    # The message always starts with A
    current = starts_with['A']
    message = current

    # Continue until the reconstructed message ends with Z
    while message[-1] != 'Z':
        next_part = starts_with[current[-1]]

        # Avoid adding the matching character twice
        message += next_part[1:]

        current = next_part

    return message


# parts = [
#     "AB",
#     "BC",
#     "CZ"
# ]

parts = ["Abc", "bcz", "Abcz", "Apple", "Axyz", "testz"
]
"Abcplexyz"
print(rebuildMessageParts(parts))

