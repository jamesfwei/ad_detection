import os

# Data collection
num_ad = 0
num_comment = 0

# Global variable to store ads and garbage
known_ads = set()
ads = set()

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
    """
    with open("manually_found_ads.txt") as f:
        for line in f:
            known_ads.add(line)

    with open("new_repeat_sent.txt") as f:
        for line in f:
            pair = eval(line)
            key = pair[0]
            value = pair[1]
            if int(value) >= 5 and len(key) > 20:
                known_ads.add(key)

            if int(value) <= 4:
                break


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
    global num_comment
    global num_ad
    for line in f:
        line_arr = line.split("|||******&&&&******|||")
        question = line_arr[0]
        answer = line_arr[1]

        # If the QA pair doesn't get thrown out it gets separated into two
        # categories:
        #  1. Answer is an ad and gets stored in the ads.txt file
        #  2. Answer is not ad and therefore a regular comment
        if is_ad(answer):
            num_ad += 1
            ads.add(answer)
        else:
            num_comment += 1
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
        return True

    for phrase in ad_phrases:
        if phrase in answer:
            return True

    return False


def print_out(question, answer):
    return question.strip() + '|||******&&&&******|||' + answer.strip() + "\n"


def main():
    init_ads()
    for root, dirs, files in os.walk("no_garbage"):
        for file in sorted(files):
            if file == ".DS_Store":
                continue
            dict_ = generate_dictionary("no_garbage/" + file)
            with open("clean/" + file + "_clean.txt", 'w') as f:
                for key in dict_:
                    for value in dict_[key]:
                        f.write(print_out(key, value))

    print("Writing to ads.txt")
    with open("ads.txt", 'w') as f:
        for ad in ads:
            f.write(ad.strip() + "\n")

    print("# of ads", num_ad)
    print("# of comments", num_comment)
    print("total", num_ad + num_comment)


if __name__ == "__main__":
    main()
