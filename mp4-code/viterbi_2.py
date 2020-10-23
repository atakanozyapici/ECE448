"""
Part 3: Here you should improve viterbi to use better laplace smoothing for unseen words
This should do better than baseline and your first implementation of viterbi, especially on unseen words
"""

"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""
import math

def smoothingLog(cnt, unique, total, alpha):
    return math.log((cnt + alpha) / (total+alpha*(unique+1)))

def buildProbability(dict, alpha):
    prob_dict = {}

    for taga in dict:
        prob_dict[taga] = {'unk' : smoothingLog(0, len(dict[taga]), sum(dict[taga].values()), alpha)}
        for tagb in dict[taga]:
            prob_dict[taga][tagb] = smoothingLog(dict[taga][tagb], len(dict[taga]), sum(dict[taga].values()), alpha)

    return prob_dict

def hapaxProb(dict):
    over_cnt = 0
    scale_dict = {}
    for key in dict:
        count = 0
        for word in dict[key]:
            if(dict[key][word] == 1):
                count += 1
                over_cnt += 1
        if(count == 0):
            count = 0.00001
        scale_dict[key] = count

    for tag in scale_dict:
        scale_dict[key] = scale_dict[key] / over_cnt
    return scale_dict

def buildEmissionProbability(dict, alpha):
    prob_dict = {}
    scale_dict = hapaxProb(dict)
    for taga in dict:
        scale_alpha = scale_dict[taga]
        prob_dict[taga] = {'unk' : smoothingLog(0, len(dict[taga]), sum(dict[taga].values()), alpha * scale_alpha)}
        for tagb in dict[taga]:
            prob_dict[taga][tagb] = smoothingLog(dict[taga][tagb], len(dict[taga]), sum(dict[taga].values()), alpha * scale_alpha)

    return prob_dict

def insertToDict(dict, key, key2):
    if(key in dict):
        if(key2 in dict[key]):
            dict[key][key2] = dict[key][key2] + 1
        else:
            dict[key][key2] = 1
    else:
        dict[key] = {key2 : 1}

def calculateProbs(prev_column, transition_prob, emission_prob, word):
    b_col = {}
    cur_col = {}
    for tag in prev_column:
        start_flag = 1
        for tag_it in prev_column:
            if(start_flag):
                start_flag = 0
                max_tag = tag_it
                max_prob = prev_column[tag_it] + transition_prob[tag_it].get(tag, transition_prob[tag_it]['unk']) + emission_prob[tag].get(word, emission_prob[tag]['unk'])
            else:
                temp_prob = prev_column[tag_it] + transition_prob[tag_it].get(tag, transition_prob[tag_it]['unk']) + emission_prob[tag].get(word, emission_prob[tag]['unk'])
                if(temp_prob > max_prob):
                    max_prob = temp_prob
                    max_tag = tag_it
        b_col[tag] = max_tag
        cur_col[tag] = max_prob

    return cur_col, b_col


def viterbi_2(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    alpha = 0.000001

    transition_dict = {}
    emission_dict = {}

    for sent in train:
        for ind in range(0, len(sent)):
            word = sent[ind][0]
            tag = sent[ind][1]

            insertToDict(emission_dict, tag, word)

            if(tag != 'END'):
                next_tag = sent[ind+1][1]
                insertToDict(transition_dict, tag, next_tag)

    transition_prob = buildProbability(transition_dict, alpha)
    emission_prob = buildEmissionProbability(emission_dict, alpha)

    start_column = {}
    for tag in transition_dict:
        if(tag == 'START'):
            start_column[tag] = smoothingLog(1,1,1,alpha)
        else:
            start_column[tag] = smoothingLog(0,1,1,alpha)

    ret_list = []

    for sent in test:
        b_array = []
        for word in sent:
            if(word == 'START'):
                prev_column = start_column.copy()
                b_col = {}
            else:
                cur_column, b_col = calculateProbs(prev_column, transition_prob, emission_prob, word)
                prev_column = cur_column
            b_array.append(b_col)

        temp_sent = []
        for ind in range(len(sent)-1, -1 , -1):
            if(ind == len(sent)-1):
                word_tag = max(prev_column, key = prev_column.get)
                next_tag = b_array[ind][word_tag]
            else:
                word_tag = next_tag
                next_tag = b_array[ind].get(word_tag)
            temp_sent.insert(0, (sent[ind], word_tag))
        ret_list.append(temp_sent)

    return ret_list
