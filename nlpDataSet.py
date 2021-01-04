import json
import re

class nlpDataSet(object):
    def __init__(self, vocab, trai_path,
                    targ_str, test_path=None):
        self.vocab= vocab
        self.trai_path= trai_path
        self.test_path= test_path
        self.targ_str= targ_str
        self.examples= self.load_examples()

    def load_examples(self):
        examples=[]
        data_file=  open(self.trai_path,'r').readlines()
        for i_line in data_file:
            temp= json.loads(i_line)
            if self.vocab.i_feat in temp and len(temp[self.vocab.i_feat]) > 0:
                    examples.append(self.make_example(temp))
        return examples
    
    def make_example(self, i_example):
        temp_targ= int(i_example[self.targ_str]) -1
        temp= re.split('[%s]'%self.vocab.sentence_split,
                    str(i_example[self.vocab.i_feat]))
        while '' in temp: temp.remove('')
        numb_sent= len(temp)
        temp=[self.vocab.tokenizer(i_sent) for i_sent in temp]
        leng= max([len(i_sent) for i_sent in temp])
        return {'targ':temp_targ, 'feat':temp, 
                'numb_sent':numb_sent, 'max_leng':leng}

    def __getitem__(self,indx):
        return self.examples[indx]

    def __len__(self):
        return len(self.examples)