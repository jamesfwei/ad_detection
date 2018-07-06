known_ads = []

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
                 '😂', '🌸', '👍', '😭', '😍']

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
        known_ads.append(line)
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


def is_ad(answer):
    """
    Returns true if the given string is an ad.

    First, an ad must have a length greater than 15 characters.
    Second, if the answer contains any of the ad phrases, it is deemed an ad.
    """

    if len(answer) < 15:
        return False

    if answer in known_ads:
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


def main(filename):
    init_ads()
    garbage = 0
    ad = 0
    comment = 0
    f = open(filename)
    g = open("data/garbage.txt", 'w')
    a = open("data/ad.txt", 'w')
    c = open("data/comment.txt", 'w')
    for line in f:
        line_arr = line.split("|||******&&&&******|||")
        question = line_arr[0]
        answer = line_arr[1]

        if len(question) > 50 or len(answer) > 50 or 'http' in question or \
                '.com' in question or 'http' in answer or '.com' in answer or\
                '视频来自：百度贴吧' in question or no_chinese(question) or \
                no_chinese(answer) or is_garbage(question) or \
                is_garbage(answer):
            garbage += 1
            g.write(question + "|||******&&&&******|||" + answer)
        elif is_ad(answer):
            ad += 1
            a.write(answer)
        else:
            comment += 1
            c.write(answer)
    f.close()
    g.close()
    a.close()
    c.close()
    p_ad = (ad / (ad + comment))
    return p_ad


if __name__ == "__main__":
    print("Probability of an ad is: %1.4f." % main("baidutieba/baidutieba_aa"))
