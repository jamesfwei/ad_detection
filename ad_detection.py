# Global variable to store ads and garbage
known_ads = {}
ads = set()
garbage = set()


# If any of these garbage symbols appear in the answer, throw it out
# immediately.
garbage_symbols = ['●', '◆', '▔□▔', '�', '█', '★', '◎', '(#啊!)', '❤', 'づ',
                   'Ψ', 'Д', 'っ', '✎', '╜', '╙', '→', '∀', '∗', 'bitch', 'fuck',
                   'ass', 'shit', 'hell', 'slut', 'dick']

# All ASCII characters. Answers shouldn't have these symbols repeated too
# many times in a row.
ascii_characters = [chr(x) for x in range(32, 128)]

# Non ASCII characters that also shouldn't be repeated. Includes some weird
# symbols like '！' which is different from the normal '!'. Also found
# different ' ' and '＝'. We also don't want '哈' or '啊' repeated in excess.
other_symbols = [' ', '＝', '！', '？', '，', '…', '﹉', '哈', '啊', '😊', '😄',
                 '😂', '🌸', '👍', '😭', '😍', '🍁', '🌴', '🍃', '🌷', '✘', 'ㅋ']

# Phrases that are likely to appear in an ad and not a regular comment
ad_phrases = ['网游折', '重大通知', '优质盐雾', '恨不在', '咨询电话', '高薪职位',
              '新用户送', '豪华巨作', '商户优惠', '专业加工', '划算到爆', '正版授权',
              '点击下载', '免费下载', '免费咨询', '查看详情', '完美产品', '买的放心',
              '专业承建', '活动截止', '快来体验', '优惠活动', '欢迎亲临', '礼品赠送',
              '省钱又省心', '独家', '保证低价', '面向上班族', '等你战', '点此进入', 
              '永久免费', '免费试听', '免费安装下载', '省钱省力省时间', '即租即用', 
              '不容错过', '免费领取', '专业母婴护理', '奶茶培训', '海量福利',
              '不容错过', '高额返现']


def init_ads():
    """
    Initially populates ads with ads from manually_found_ads.txt
    :return: void
    """
    f = open("manually_found_ads.txt")
    for line in f:
        known_ads[line] = 0
    f.close()


def no_chinese(string):
    """
    Returns true if string has no Chinese characters in it. I chose 2000
    arbitrarily that characters less than it are considered "English".
    """
    for s in string:
        if ord(s) > 2000:
            return False
    return True


def generate_dictionary(filename):
    """
    Given a filename, generates a dictionary where questions are key and
    are stored as values in an array.

    If an answer is an ad, add it to the array of ads and don't add it to our
    dictionary.
    """

    print("working on", filename)
    f = open(filename)
    dict_ = {}
    for line in f:
        line_arr = line.split("|||******&&&&******|||")
        question = line_arr[0]
        answer = line_arr[1]

        # A QA pair can be thrown out for many reasons:
        #  1. Question or answer is too long
        #  2. Question or answer contains a link
        #  3. Question contains '视频来自：百度贴吧'
        #  4. Question or answer doesn't contain any Chinese
        #  5. Question is garbage (poorly formatted)
        if len(question) > 50 or len(answer) > 50:
            continue

        if 'http' in question or '.com' in question or 'http' in answer or \
                '.com' in answer:
            continue

        if '视频来自：百度贴吧' in question:
            continue

        if no_chinese(question) or no_chinese(answer):
            continue

        if is_garbage(question):
            continue

        # If the QA pair doesn't get thrown out it gets separated into three
        # categories:
        #  1. Answer is garbage and gets stored in the garbage.txt file
        #  2. Answer is an ad and gets stored in the ads.txt file
        #  3. None of the above so the answer is added into our dictionary
        if is_garbage(answer):
            garbage.add(answer)
        elif is_ad(answer):
            ads.add(answer)
        else:
            # If answer is not an ad, add it to the dictionary
            if question not in dict_:
                dict_[question] = set()
            dict_[question].add(answer)
    f.close()
    return dict_


def is_ad(answer):
    """
    Returns true if the given string is an ad.

    First, an ad must have a length greater than 15 characters.
    Second, if the answer contains any of the ad phrases, it is deemed an ad.
    """

    if len(answer) < 15:
        return False

    if answer in known_ads:
        known_ads[answer] += 1
        return True

    for phrase in ad_phrases:
        if phrase in answer:
            return True

    return False


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


def is_garbage(answer):
    """
    Answer needs to contain any of the garbage symbols or more than 3 of
    ascii_characters or other_symbols repeated in a row.
    """
    return check(garbage_symbols, answer, 1) or \
           check(ascii_characters, answer, 4) or check(other_symbols, answer, 4)


def get_next_file():
    """
    Generator that returns the filename of the next file to run ad
    detection on.
    """

    base = "baidutieba_"

    for first_letter in range(97, 106):
        for second_letter in range(97, 123):
            yield (base + chr(first_letter) + chr(second_letter))

    yield "baidutieba_ja"
    yield "baidutieba_jb"


def main():
    init_ads()
    for filename in get_next_file():
        dict_ = generate_dictionary("baidutieba/" + filename)
        f = open("clean/" + filename + "_clean.txt", 'w')
        for key in dict_:
            for value in dict_[key]:
                f.write(key.rstrip())
                f.write("|||******&&&&******|||")
                f.write(value.rstrip())
                f.write("\n")
        f.close()

    print("Writing to ads.txt")
    f = open("ads.txt", 'w')
    for ad in ads:
        f.write(ad.rstrip())
        f.write("\n")
    print("Finished writing to ads.txt")
    f.close()

    print("Writing to garbage.txt")
    f = open("garbage.txt", 'w')
    for garb in garbage:
        f.write(garb.rstrip())
        f.write("\n")
    print("Finished writing to garbage.txt")
    f.close()


if __name__ == "__main__":
    main()
