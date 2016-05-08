import string

def read_file(filename):
    r"""Assume the file is the format
    word \t tag
    word \t tag
    [[blank line separates sentences]]
    
    This function reads the file and returns a list of sentences.  each
    sentence is a pair (tokens, tags), each of which is a list of strings of
    the same length.
    """

    sentences = open(filename).read().strip().split("\n\n") #separate tweets
    ret = []
    for sent in sentences:
        lines = sent.split("\n") #each word in the tweet
        pairs = [L.split("\t") for L in lines] #Funniest    O
        tokens = [tok for tok,tag in pairs]
        tags = [tag for tok,tag in pairs]
        ret.append( (tokens,tags) )
    return ret

#When it's not labeled, so only one column of data, no tags
def read_file_unlabeled(filename):
    r"""Assume the file is the format
    word \t tag
    word \t tag
    [[blank line separates sentences]]
    
    This function reads the file and returns a list of sentences.  each
    sentence is a pair (tokens, tags), each of which is a list of strings of
    the same length.
    """

    sentences = open(filename).read().strip().split("\n\n") #separate tweets
    ret = []
    for sent in sentences:
        lines = sent.split("\n") #each word in the tweet
        ret.append( (lines) )
    return ret

def get_pos_tags(posfile):
    #Creating dictionary for POS tags
    with open(posfile) as file:
        postags = [x.strip('\n') for x in file.readlines()]

    posDictionary = {}

    for i, line in enumerate(postags):
        if line != "":
            pairs = line.split("\t")
            word = pairs[0] 
            postag = pairs[1]
            posDictionary[word] = postag

    return posDictionary

def clean_str(s):
    """Clean a word string so it doesn't contain special crfsuite characters"""
    return s.replace(":","_COLON_").replace("\\", "_BACKSLASH_")

def extract_features_for_sentence1(tokens, postags):
    N = len(tokens)
    feats_per_position = [set() for i in range(N)]
    for t in range(N):
        w = clean_str(tokens[t])
        feats_per_position[t].add("word=%s" % w)
        feats_per_position[t].add("word.lower=%s" % w.lower()) #lowered word bc capitalization is inconsistent
        feats_per_position[t].add("word[-2:]=%s" % w[-2:]) #neither of these increased F score
        feats_per_position[t].add("word[-3:]=%s" % w[-3:])

        feats_per_position[t].add("word.isupper=%s" % w.isupper())
        feats_per_position[t].add("word.istitle=%s" % w.istitle())
        feats_per_position[t].add("word.isdigit=%s" % w.isdigit()) #didn't increase F score

        #Adding in Twitter POS Tags
        if w in postags:
            feats_per_position[t].add("postag=" + postags[w])
        else:
            feats_per_position[t].add("postag=" + "#") #give random tag for unknown values

        #Adding in contextual information from word behind
        if t > 0:
            behind = clean_str(tokens[t-1])
            feats_per_position[t].add("behind.lower=%s" % behind.lower())
            feats_per_position[t].add("behind.istitle=%s" % behind.istitle())
            feats_per_position[t].add("behind.isupper=%s" % behind.isupper())
            
            if behind in postags:
                feats_per_position[t].add("behind.postag=" + postags[behind])
            else:
                feats_per_position[t].add("behind.postag=" + "#")
        elif t == 0:
            feats_per_position[t].add("beginning") #is beginning of sentence

        #Adding in contextual information from word in front
        if t < len(tokens) - 1:
            infront = clean_str(tokens[t + 1])
            feats_per_position[t].add("infront.lower=%s" % infront.lower())
            feats_per_position[t].add("infront.istitle=%s" % infront.istitle())
            feats_per_position[t].add("infront.isupper=%s" % infront.isupper())

            if infront in postags:
                feats_per_position[t].add("infront.postag=" + postags[infront])
            else:
                feats_per_position[t].add("infront.postag=" + "#")
        elif t == len(tokens) - 1:
            feats_per_position[t].add("end") #is the end of the sentence

    return feats_per_position

extract_features_for_sentence = extract_features_for_sentence1

def extract_features_for_file(input_file, output_file, posfile):
    """This runs the feature extractor on input_file, and saves the output to
    output_file."""
    if not unlabeled:
        sents = read_file(input_file)
    else:
        sents = read_file_unlabeled(input_file)
    postags = get_pos_tags(posfile)
    with open(output_file,'w') as output_fileobj:
        if not unlabeled:
            for tokens,goldtags in sents:
                feats = extract_features_for_sentence(tokens, postags)
                for t in range(len(tokens)):
                    feats_tabsep = "\t".join(feats[t])
                    print>>output_fileobj, "%s\t%s" % (goldtags[t], feats_tabsep)
                print>>output_fileobj, ""
        else:
            for tokens in sents:
                feats = extract_features_for_sentence(tokens, postags)
                for t in range(len(tokens)):
                    feats_tabsep = "\t".join(feats[t])
                    print>>output_fileobj, "%s" % (feats_tabsep) #for nolabels dat
                print>>output_fileobj, ""

unlabeled = False
extract_features_for_file("combineddata.txt", "combineddata.feats", "cleanPosCombinedData.txt")
unlabeled = True
extract_features_for_file("DevNoLabels.txt", "DevNoLabels.feats", "cleanPosDevNoLabels.txt")
