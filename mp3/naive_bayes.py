# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for MP3. You should only modify code
within this file and the last two arguments of line 34 in mp3.py
and if you want-- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math

def getProbability(dict, word,total_count,alpha):
    if(word in dict):
        return dict[word]
    else:
        return math.log(alpha/(total_count + alpha * (len(dict)+1)))

def getbiProbability(dict, word_dict, word, next_word, total_count,alpha, total_count_word, alpha_word):
    key = word + "," + next_word
    if(key in dict):
        return dict[key]
    else:
        return getProbability(word_dict, word, total_count_word,alpha_word) + getProbability(word_dict, next_word, total_count_word,alpha_word)

def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter=1.0, pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter --laplace (1.0 by default)
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set
    #alpha const
    alpha = smoothing_parameter
    ##
    bag_positive = {}
    bag_negative = {}
    total_positive = 0
    total_negative = 0
    stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"}
    #create the bag of words
    for ind in range(0,len(train_set)):
        for word in train_set[ind]:
            word = word.lower()
            if(word not in stop_words):
                if(train_labels[ind]):
                    total_positive +=1
                    if(word in bag_positive):
                        bag_positive[word] = bag_positive[word]+1
                    else:
                        bag_positive[word] = 1
                else:
                    total_negative += 1
                    if(word in bag_negative):
                        bag_negative[word] = bag_negative[word]+1
                    else:
                        bag_negative[word] = 1

    #calculate the probabilities wiht laplace smoothing
    positive_like = {}
    negative_like = {}

    for pos in bag_positive:
        positive_like[pos] = math.log((bag_positive[pos] + alpha) / (total_positive+alpha*(len(bag_positive)+1)))

    for neg in bag_negative:
        negative_like[neg] = math.log((bag_negative[neg] + alpha) / (total_negative+alpha*(len(bag_negative)+1)))

    #predict the email
    return_list = []
    for dev in dev_set:
        positive = 0
        negative = 0
        for word in dev:
            word = word.lower()
            if(word not in stop_words):
                positive += getProbability(positive_like, word, total_positive, alpha)
                negative += getProbability(negative_like, word, total_negative, alpha)

        positive += math.log(pos_prior)
        negative += math.log(1-pos_prior)

        if(positive >= negative):
            return_list.append(1)
        else:
            return_list.append(0)

    return return_list

def bigramBayes(train_set, train_labels, dev_set, unigram_smoothing_parameter=1.0, bigram_smoothing_parameter=1.0, bigram_lambda=0.5,pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    unigram_smoothing_parameter - The smoothing parameter for unigram model (same as above) --laplace (1.0 by default)
    bigram_smoothing_parameter - The smoothing parameter for bigram model (1.0 by default)
    bigram_lambda - Determines what fraction of your prediction is from the bigram model and what fraction is from the unigram model. Default is 0.5
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set using a bigram model
    alpha = 0.1
    ##
    bag_positive = {}
    bag_negative = {}
    bibag_positive = {}
    bibag_negative = {}
    total_positive = 0
    total_negative = 0
    total_bipositive = 0
    total_binegative = 0
    stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"}
    #create the bag of words
    for ind in range(0,len(train_set)):
        for w_ind in range(0,len(train_set[ind])):
            next_word = ""
            next_flag = 0
            word = (train_set[ind][w_ind]).lower()
            if(w_ind +1 < len(train_set[ind])):
                next_word = (train_set[ind][w_ind+1]).lower()
                next_flag = 1
            if(train_labels[ind]):
                total_positive +=1
                if(word in bag_positive):
                    bag_positive[word] = bag_positive[word]+1
                else:
                    bag_positive[word] = 1
            else:
                total_negative += 1
                if(word in bag_negative):
                    bag_negative[word] = bag_negative[word]+1
                else:
                    bag_negative[word] = 1

            if(train_labels[ind]):
                if(next_flag):
                    key = word+","+next_word
                    total_bipositive += 1
                    if(key in bibag_positive):
                        bibag_positive[key] = bibag_positive[key]+1
                    else:
                        bibag_positive[key] = 1
            else:
                if(next_flag):
                    key = word+","+next_word
                    total_binegative += 1
                    if(key in bibag_negative):
                        bibag_negative[key] = bibag_negative[key]+1
                    else:
                        bibag_negative[key] = 1

    #calculate the probabilities wiht laplace smoothing
    positive_like = {}
    negative_like = {}
    bipositive_like = {}
    binegative_like = {}
    bigram_smoothing_parameter = 0.8

    for pos in bag_positive:
        positive_like[pos] = math.log((bag_positive[pos] + alpha) / (total_positive+alpha*(len(bag_positive)+1)))

    for neg in bag_negative:
        negative_like[neg] = math.log((bag_negative[neg] + alpha) / (total_negative+alpha*(len(bag_negative)+1)))

    for pos in bibag_positive:
        bipositive_like[pos] = math.log((bibag_positive[pos] + bigram_smoothing_parameter) / (total_bipositive+bigram_smoothing_parameter*(len(bibag_positive)+1)))

    for neg in bibag_negative:
        binegative_like[neg] = math.log((bibag_negative[neg] + bigram_smoothing_parameter) / (total_binegative+bigram_smoothing_parameter*(len(bibag_negative)+1)))

    lam = bigram_lambda

    return_list = []
    for dev in dev_set:
        positive = 0
        negative = 0
        for w_ind in range(0, len(dev)):
            word = dev[w_ind].lower()
            positive += (1-lam) * getProbability(positive_like, word, total_positive, alpha)
            negative += (1-lam) * getProbability(negative_like, word, total_negative, alpha)

            if(w_ind+1 < len(dev)):
                next_word = dev[w_ind+1].lower()
                positive += (lam) * getbiProbability(bipositive_like, positive_like, word, next_word, total_bipositive, bigram_smoothing_parameter, total_positive,alpha)
                negative += (lam) * getbiProbability(binegative_like, negative_like, word, next_word, total_binegative, bigram_smoothing_parameter, total_negative, alpha)

        positive += math.log(pos_prior)
        negative += math.log(1-pos_prior)

        if(positive >= negative):
            return_list.append(1)
        else:
            return_list.append(0)

    return return_list
