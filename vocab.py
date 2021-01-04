from collections import defaultdict
import json

class vocab(object):
    '''class to build a vocabylary object to use during numeralization
    it holds 
    tokenizer -> a function that gets a string and output a list
                tokens in string format'
    path -> path to the json file with the data
    i_feat -> name of the key of the json file which value is the text to use
            as feature
    sentence_split -> a string with simbols to split a text into a sentences
    frec -> dictionay with the frecuency of every token
    special tokens <pad> for pading and <unk> for unknown tokens
    <unk> -> 0
    <pad> -> 1
    stoi -> a dictionay mapping a token string (key) to the token index (value)
    itos -> a list where itos[index] -> token string
    mini_frec-> minimal frecuency for a token to be in vocabulary'''
    def __init__(self, tokenizer, path, i_feat, 
                    sentence_split=None, mini_frec=10):
        self.tokenizer= tokenizer
        self.path= path
        self.i_feat= i_feat
        self.sentence_split= sentence_split
        self.frec={}
        self.stoi = defaultdict(lambda : 0) 
        self.stoi['<pad>'] = 1
        self.itos=['<unk>', '<pad>']
        self.mini_frec= mini_frec

    def build_vocabulary(self):
        # first load the data
        data_file=  open(self.path,'r').readlines()
        #count frecuency of tokens in vocab
        for i_line in data_file:
            i_line= json.loads(i_line)
            for j_toke in self.tokenizer(i_line[self.i_feat]):
                if j_toke in self.frec:
                    self.frec[j_toke]+=1
                else:
                    self.frec[j_toke]=1
        #sort tokens by frecuency
        self.frec= {k: v for k, v in sorted(self.frec.items(), 
                    key=lambda item: item[1], reverse=True)}
        #populate the itos and stoi
        for key in self.frec:
            if self.frec[key] > self.mini_frec:
                self.itos.append(key)
                self.stoi[key] = self.itos.index(key)
        return None