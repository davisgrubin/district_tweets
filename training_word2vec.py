from gensim.models import Word2Vec, word2vec
import sys, os
#make sure we are using Cython to utilize mutltiple cores
assert word2vec.FAST_VERSION > -1

#Generator object for reading tweets line by line
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()





if __name__ == '__main__':
    '''python training_word2vec.py tweets_filepath'''
    sentences = MySentences('test_folder')
    model = Word2Vec(sentences,iter=15,workers=4)
    model.save('first_model')
