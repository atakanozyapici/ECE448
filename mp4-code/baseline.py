"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""
def findTag(dict, tag_dict, word):
    if(word in dict):
        tag_dict_word = dict[word]
        return max(tag_dict_word, key = tag_dict_word.get)
    else:
        return max(tag_dict, key = tag_dict.get)

def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    training_dict = {}
    tag_dict = {}

    for sent in train:
        for word_pair in sent:
            word = word_pair[0]
            tag = word_pair[1]
            if(tag in tag_dict):
                tag_dict[tag] = tag_dict[tag] + 1
            else:
                tag_dict[tag] = 1

            if(word not in training_dict):
                training_dict[word] = {tag : 1}
            else:
                if(tag in training_dict[word]):
                    training_dict[word][tag] = training_dict[word][tag] + 1
                else:
                    training_dict[word][tag] = 1

    ret_list = []

    for sent in test:
        sent_list = []
        for word in sent:
            tag = findTag(training_dict, tag_dict, word)
            sent_list.append((word, tag))
        ret_list.append(sent_list)
    return ret_list
