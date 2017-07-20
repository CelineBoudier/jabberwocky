from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import nltk
import os


class Antonimizer(object):

    def __init__(self, depth):
        self.conv_tag = {'NN':wordnet.NOUN,'JJ':wordnet.ADJ,'VB':wordnet.VERB,'RB':wordnet.ADV}
        self.corpus_dir = os.path.join(os.getcwd(), "corpus")
        self.res_dir = os.path.join(os.getcwd(), "results")
        self.depth = depth

    def antonimize_dir(self):
        if os.path.isdir(self.corpus_dir):
            song_files = [f for f in os.listdir(self.corpus_dir)
                          if os.path.isfile(os.path.join(self.corpus_dir, f))]
            for song_file in song_files:
                with open(os.path.join(self.corpus_dir, song_file)) as song:
                    if not os.path.isfile(os.path.join(self.res_dir, str(self.depth) + song_file)):
                        with open(os.path.join(self.res_dir, str(self.depth) + song_file), 'wb') as res_file:
                            for text in song:
                                ant_text = self.antonimize_text(text)
                                res_file.write(ant_text+'\n')
                        res_file.close()
                song.close()

    def find_antonym(self, word, tag, depth=1):
        if tag[:2] in self.conv_tag:
            for syn in wordnet.synsets(word, pos=self.conv_tag[tag[:2]]):
                for lemma in syn.lemmas():
                    if lemma.antonyms():
                        return lemma.antonyms()[0].name()
        if depth<=1:
            return word
        else:
            definition = nltk.pos_tag(word_tokenize(self.find_definition(word, tag)))
            return " ".join([self.find_antonym(w, t, depth-1) for w, t in definition])

    def find_definition(self, word, tag):
        if tag[:2] in self.conv_tag:
            for syn in wordnet.synsets(word, pos=self.conv_tag[tag[:2]]):
                if syn.definition():
                    return syn.definition().split(";")[0]
        return word

    def antonimize_text(self, text):
        tokens = word_tokenize(text)
        tagged_tokens = nltk.pos_tag(tokens)
        antonimized_words = []
        for word, tag in tagged_tokens:
            antonimized_words.append(self.find_antonym(word, tag, self.depth))
        return " ".join(antonimized_words)

for i in xrange(1,4):
    Antonimizer(i).antonimize_dir()
