from numpy import cumsum, array, mean , zeros
from random import random

import re, string
#for text pre-processing
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')
#for model-building

# For visualization
import seaborn as sns
import matplotlib.pyplot as plt

class Processor():
    def __init__(self):
        self.snow = SnowballStemmer('english')
        self.wl = WordNetLemmatizer()
        self.word_tokenize = word_tokenize
    
    #convert to lowercase and remove punctuations and characters and then strip
    def preprocess(self, text):
        text = str(text).lower() #lowercase text
        text = text.strip()  #get rid of leading/trailing whitespace 
        text = re.compile('<.*?>').sub('', text) #Remove HTML tags/markups
        text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)  #Replace punctuation with space. Careful since punctuation can sometime be useful
        text = re.sub('\s+', ' ', text)  #Remove extra space and tabs
        # text = re.sub(r'\[[0-9]*\]',' ',text) #[0-9] matches any digit (0 to 10000...)
        text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
        # text = re.sub(r'\d',' ',text) #matches any digit from 0 to 100000..., \D matches non-digits
        text = re.sub(r'\s+',' ',text) #\s matches any whitespace, \s+ matches multiple whitespace, \S matches non-whitespace 
        
        return text

    #3. LEXICON-BASED TEXT PROCESSING EXAMPLES
    
    #1. STOPWORD REMOVAL
    def stopword(self, string):
        a= [i for i in string.split() if i not in stopwords.words('english')]
        return ' '.join(a)

    #2. STEMMING
    
    # Initialize the stemmer
    def stemming(self, string):
        a=[self.snow.stem(i) for i in word_tokenize(string) ]
        return " ".join(a)

    def one_hot_encode(self, labels):
        dictionary = {label: idx for idx, label in enumerate(sorted(labels))}
        return dictionary
    
    # This is a helper function to map NTLK position tags
    # Full list is available here: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    def get_wordnet_pos(self, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    # 3. LEMMATIZATION
    # Initialize the lemmatizer
    # Tokenize the sentence
    def lemmatizer(self, string):
        word_pos_tags = nltk.pos_tag(word_tokenize(string)) # Get position tags
        a=[self.wl.lemmatize(tag[0], self.get_wordnet_pos(tag[1])) 
           # Map the position tag and lemmatize the word/token
           for idx, tag in enumerate(word_pos_tags)] 
        return " ".join(a)

    def finalpreprocess(self, string:str):
        return self.lemmatizer(self.stopword(self.preprocess(string)))
    
    def visualize(self, data):
        """ visualize csv file """
        COLORS = [u'#1f77b4', u'#ff7f0e', u'#2ca02c', u'#9467bd', u'#d62728', 
          u'#8c564b', u'#e377c2', u'#7f7f7f', u'#bcbd22', u'#17becf',
          u'#1f77b4', u'#ff7f0e', u'#2ca02c']

        data.dropna(subset = ["label"], inplace=True)
        print('Shape: ', data.shape)
        # CLASS DISTRIBUTION
        #if dataset is balanced or not
        x = data['label'].value_counts()
        sns.set(rc={'figure.figsize':(2 * len(x), 8)})
        sns.barplot(x.index,x)
        #Missing values
        print("Missing data:\n", data.isna().sum())
        
        #1. WORD-COUNT
        data['word_count'] = data['text'].apply(lambda x: len(str(x).split()))
        labels = data['label'].unique()
        # print(labels)
        # for label in labels:
        #     print(label, ':', data[data['label']==label]['word_count'].mean()) 
        # print()
        #2. CHARACTER-COUNT
        data['char_count'] = data['text'].apply(lambda x: len(str(x)))
        # for label in labels:
        #     print(label, ':', data[data['label']==label]['char_count'].mean()) 
        # print()

        #3. UNIQUE WORD-COUNT
        data['unique_word_count'] = data['text'].apply(lambda x: len(set(str(x).split())))
        # for label in labels:
        #     print(label, ':', data[data['label']==label]['unique_word_count'].mean()) 
            
        """ Plotting word-count per tweet """
        ax = [[]] * len(labels)
        h = int((len(x) - 1) / 4 + 1)
        w = 4
        fig,(ax[:len(labels)])=plt.subplots(h, w, figsize=(h * 6, w * 4))
        for i, label in enumerate(labels):
            train_words=data[data['label']==label]['word_count']
            ax[int(i/4)][ i % 4].hist(train_words,color=COLORS[i])
            ax[int(i/4)][ i % 4].set_title(label)

        fig.suptitle('Words per tweet')
        plt.show()
        del data['char_count'], data['unique_word_count'], data['word_count']
    
#for converting sentence to vectors/numbers from word vectors result by Word2Vec
class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = len(next(iter(word2vec.values())))

    def fit(self, X, y):
        return self

    def transform(self, X):
        return array([
            mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [zeros(self.dim)], axis=0)
            for words in X
        ])

if __name__ == "__main__":
    proc = Processor()
    #1. Common text preprocessing
    text = "   This is a   message to be cleaned. It may involve some things like: <br>, ?, :, ''  adjacent spaces and tabs     .  "
    print(proc.finalpreprocess(text))
    w2v = Word2Vec(text)
    