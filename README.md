# Ad Detection
This repository is code I wrote during my 2018 summer internship at MIX in 
Beijing. It creates a cleaned version of data downloaded from 百度贴吧 
(BaiduTieba), the Chinese version of Reddit. In the folder baidutieba/ are the
original data files. Each data file contains 100,000 lines of QA pairs where the
questions are the posts and the answers are the comments from BaiduTieba. These
files are used to train a NLP model at MIX.

_Currently cannot upload baidutieba/ because of slow WiFi._

## Overview
The data is first cleaned by removing lines of "garbage" that weren't useful for
the model. The next task was to remove ads. I did this by finding specific
phrases typically found in ads and rarely found in regular comments. For
example, any comment including the phrases "点此进入" which translates to "click
here to enter" was flagged as an ad. To do this, run ad_detection.py
which creates the directory clean/ which contains the cleaned versions of each
data file. It also creates garbage.txt and ads.txt which stores the garbage and
ads found.

manually_found_ads.txt contains a bunch of ads I found by hand.

Next, I implemented a Naive Bayes classifer to supplement my inital ad detection
method. With reference from:
https://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html
I implemented NB classifier in naive.py. The training data is generated by 
get_data.py which takes a filename (I used baidutieba/baidutieba_aa). This file
separates the 100,000 lines into three cases found in the data/ folder. The
three cases are garabage, ads, and regular comments that can be used to train
the NLP model. From here, the ads.txt and comments.txt files were used to train
the NB classifier. I then ran the NB classifer using naive.py on all the cleaned
baidutieba files (clean/baidutieba_**_clean.txt) which separats each clean file
into a "more clean" file called naive/baidutieba_**_clean_nb.txt and the ads
found using the NB classifier into the file called 
naive_ad/baidutieba_**_ads.txt.

An example of an ad found using the NB classifier is:
别再买假学历了！4月起，北京正式开放成人大学录取通道，毕业就是本科学历. As this ad does
contain any of the "classical" ad phrases, it went undetected until I used the
NB classifer

## Prerequisites
jieba is used to parse sentences in Chinese into phrases. For example,
list(jieba.cut("我新欢吃水果")) = ['我', '喜欢', '吃水果']. To install on macOS, run
```
pip install jieba
```
