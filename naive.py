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


import os
import math
import jieba
from ad_detection import init_ads, print_out, is_ad
from remove_garbage import QA_is_garbage

# Data collection
num_ad = 0
num_comment = 0

ads = {}
comments = {}
vocab = set()


def learn(filename):
    """
    This method learns from the training data. It populates the ads and
    comments dictionary with the term as the key and number of occurrences as
    the value.
    This method also adds all terms into a set called vocab because we will
    need the size of the vocabulary later.
    """
    print("Learning...", end="")
    init_ads()
    num_ads = 0
    num_comments = 0
    with open(filename) as f:
        for line in f:
            # Find QA in each line
            line_arr = line.split("|||******&&&&******|||")
            question = line_arr[0]
            answer = line_arr[1]

            # If we find garbage, ignore it because we won't use it in our data
            if QA_is_garbage(question, answer):
                continue
            # For each ad, add each term to our dictionary. Key is the term
            # and value is the number of occurrences.
            elif is_ad(answer):
                num_ads += 1
                for term in jieba.cut(line):
                    ads[term] = ads[term] + 1 if term in ads else 1
            # Do the same for regular comments.
            else:
                num_comments += 1
                for term in jieba.cut(line):
                    comments[term] = comments[term] + 1 if term in comments \
                        else 1

    # Adding all terms into a set to find the size of the vocabulary
    for key in ads.keys():
        vocab.add(key)
    for key in comments.keys():
        vocab.add(key)
    print("finished.")
    return num_ads / (num_ads + num_comments)


def prob_term_given_class(class_, term):
    """
    This helper function calculates P(term | class_). We can interpret this
    as a measure of how much evidence term contributes that class_ is the
    correct class.
    This method also uses add-one or Laplace smoothing as demonstrated by
    adding 1 in the numerator and adding the length of the vocabulary in the
    denominator.
    :return: a probability value that estimates the relative frequency of
    term in documents belong to class class_
    """
    return ((class_[term] if term in class_ else 0) + 1) / \
           (len(class_.keys()) + len(vocab))


def naive_is_ad(p_ad, answer):
    """
    This method determines if the given answer is an ad or not using a NB
    classifier, which takes into account the probability of any answer being
    an ad using the training data as a reference. Then, dividing the comment
    into terms, it takes into account the contribution of each term to the
    entire answer being in a particular class.
    prob_ad and prob_comment are not true probabilities because it is
    necessary to take the log of each term and there add its value instead of
    multiplying because Python cannot handle multiplying many small floating
    point numbers.
    Then, it chooses the larger value of prob_ad and prob_comment because
    that class will have a higher relative probability.
    """
    prob_ad = math.log(p_ad)
    prob_comment = math.log(1 - p_ad)
    for val in jieba.cut(answer):
        prob_ad += math.log(prob_term_given_class(ads, val))
        prob_comment += math.log(prob_term_given_class(comments, val))

    return prob_ad > prob_comment


def main():
    global num_ad
    global num_comment
    p_ad = learn("baidutieba/baidutieba_aa")

    for root, dirs, files in os.walk("clean"):
        for file in sorted(files):
            if file == ".DS_Store":
                continue
            print("Working on " + file)
            # Open f to read from and write the comments to g and the ads to
            # h as determined by the Bayes classifier
            with open("test/" + file) as f, \
                 open("naive/" + file, 'w') as g, \
                 open("naive_ad/" + file[0:13] + "_ads.txt", 'w') as h:
                for line in f:
                    [question, answer] = line.split("|||******&&&&******|||")
                    if naive_is_ad(p_ad, answer):
                        num_ad += 1
                        h.write(print_out(question, answer))
                    else:
                        num_comment += 1
                        g.write(print_out(question, answer))

    print("# of ads", num_ad, "percentage: ", (num_ad / (num_ad + num_comment)))
    print("# of comments", num_comment)
    print("total", num_ad + num_comment)


if __name__ == "__main__":
    main()
