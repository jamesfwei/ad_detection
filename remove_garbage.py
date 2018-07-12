# For each baidutieba file, rewrite it into no_garbage/ without garbage as
# determined by QA_is_garbage

import os

# If any of these garbage symbols appear in the answer, throw it out
# immediately.
garbage_symbols = ['●', '◆', '▔□▔', '�', '█', '★', '◎', '(#啊!)', '❤', 'づ',
                   'Ψ', 'Д', 'っ', '✎', '╜', '╙', '→', '∀', '∗', 'bitch',
                   'fuck', 'ass', 'shit', 'hell', 'slut', 'dick']

# All ASCII characters. Answers shouldn't have these symbols repeated too
# many times in a row.
ascii_characters = [chr(x) for x in range(32, 128)]

# Non ASCII characters that also shouldn't be repeated. Includes some weird
# symbols like '！' which is different from the normal '!'. Also found
# different ' ' and '＝'. We also don't want '哈' or '啊' repeated in excess.
other_symbols = [' ', '＝', '！', '？', '，', '…', '﹉', '哈', '啊', '😊', '😄',
                 '😂', '🌸', '👍', '😭', '😍', '🍁', '🌴', '🍃', '🌷', '✘', 'ㅋ']


def no_chinese(string):
    """
    Returns true if string has no Chinese characters in it. I chose 2000
    arbitrarily that characters less than it are considered "English".
    """
    for s in string:
        if ord(s) > 2000:
            return False
    return True


def check(lst, answer, rep):
    """
    Helper function that checks if any member of lst is in answer.
    :param lst: list of elements to check
    :param answer: string to check against
    :param rep: number of times to repeat elements in lst
    :return: boolean if members of lst are found in answer
    """
    for ele in lst:
        if (ele * rep) in answer:
            return True

    return False


def is_garbage(string):
    """
    Answer needs to contain any of the garbage symbols or more than 3 of
    ascii_characters or other_symbols repeated in a row.
    """
    return check(garbage_symbols, string, 1) \
           or check(ascii_characters, string, 4) \
           or check(other_symbols, string, 4)


def QA_is_garbage(question, answer):
    # A QA pair can be considered garbage for many reasons:
    # Question or answer is too long
    if len(question) > 50 or len(answer) > 50:
        return True

    # Question or answer contains a link or video
    if 'http' in question or '.com' in question or 'http' in answer or \
            '.com' in answer or '视频来自：百度贴吧' in question:
        return True

    # Question or answer doesn't contain any Chinese
    if no_chinese(question) or no_chinese(answer):
        return True

    # Question is garbage (poorly formatted)
    if is_garbage(question) or is_garbage(answer):
        return True

    return False


def main():
    for root, dirs, files in os.walk("baidutieba"):
        for file in sorted(files):
            print(file)
            if file == ".DS_Store":
                continue

            f = open("baidutieba/" + file)
            w = open("no_garbage/" + file, 'w')

            for line in f:
                line_arr = line.split("|||******&&&&******|||")
                question = line_arr[0]
                answer = line_arr[1]

                if not QA_is_garbage(question, answer):
                    w.write(print_out(question, answer))

            f.close()
            w.close()


if __name__ == '__main__':
    main()