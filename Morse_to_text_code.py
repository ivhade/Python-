MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.',
    '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}


def string_to_morse(text):
    """Convert a string into Morse code."""
    morse_code = []
    for char in text.upper():
        if char in MORSE_DICT:
            morse_code.append(MORSE_DICT[char])
        else:
            morse_code.append('?')  # Unknown characters as '?'
    return ' '.join(morse_code)


# Main program
if __name__ == "__main__":
    user_input = input("Enter a string to convert into Morse Code: ")
    result = string_to_morse(user_input)
    print("Morse Code:", result)