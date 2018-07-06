# This Python file uses the Naive Bayes classifier to determine if answers in
# QA pairs from BaiduTieba are ads or just regular comments. First, we use a
# training file, typically baidutieba/baidutieba_aa and importing the
# get_data.python file, we first throw out the garbage and then get a
# probability value for ads and comments that we will use as a benchmark for
# all the other files. get_data also separates all the non-garbage answers
# into ads and comments which go into the data_ad.txt and data_comment.txt
# files respectively. Then, we learn from the training file by breaking each
# comments into phrases using jieba. Each term is added to a dictionary with
# its value as the number of occurrences. So we have two dictionaries,
# one to store the ads and one to store the comments. We then combine ALL
# terms into a set because we will need the size of our vocabulary later.
# Then, we proceed to calculate which class an answer will belong to
# according to the Naive Bayes classifier.


import math
import jieba
import get_data

training_file = "baidutieba/baidutieba_aa"
p_ad = get_data.main(training_file)
p_not_ad = 1 - p_ad
ads = {}
comments = {}
vocab = set()


def add_to_dictionary(dict_, val):
    dict_[val] = dict_[val] + 1 if val in dict_ else 1


def learn():
    print("Learning...", end="")
    # Learning ads
    with open("data/data_ad.txt") as a:
        for line in a:
            for term in jieba.cut(line):
                add_to_dictionary(ads, term)

    # Learning comments
    with open("data/data_comment.txt") as c:
        for line in c:
            for term in jieba.cut(line):
                add_to_dictionary(comments, term)

    # Adding all terms into a set to find the size of the vocabulary
    for key in ads.keys():
        vocab.add(key)
    for key in comments.keys():
        vocab.add(key)
    print("finished.")


def prob_term_given_class(class_, term):
    return ((class_[term] if term in class_ else 0) + 1) / \
           (len(class_.keys()) + len(vocab))


def is_ad(comment):
    split = jieba.cut(comment)
    prob_ad = math.log(p_ad)
    prob_comment = math.log(p_not_ad)
    for val in split:
        prob_ad += math.log(prob_term_given_class(ads, val))
        prob_comment += math.log(prob_term_given_class(comments, val))

    return 1 if prob_ad > prob_comment else 0


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
    learn()

    for filename in get_next_file():
        print("Working on " + filename)
        f = open("clean/" + filename + "_clean.txt")
        g = open("naive/" + filename + "_clean_nb.txt", 'w')
        h = open("naive_ad/" + filename + "_ads.txt", 'w')
        for line in f:
            line_arr = line.split("|||******&&&&******|||")
            question = line_arr[0].rstrip()
            answer = line_arr[1].rstrip()

            if is_ad(answer):
                h.write(question)
                h.write("|||******&&&&******|||")
                h.write(answer)
                h.write("\n")
            else:
                g.write(question)
                g.write("|||******&&&&******|||")
                g.write(answer)
                g.write("\n")

        f.close()
        g.close()
        h.close()


if __name__ == "__main__":
    main()