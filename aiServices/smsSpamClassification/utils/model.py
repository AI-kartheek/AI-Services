import argparse
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle
from bs4 import BeautifulSoup
import re
import unicodedata
import contractions as cont # to fix the contractions we use this library
import pandas as pd
import copy

model_path = "F:/Python Web Projects/FLASK/AI Services/aiServices/smsSpamClassification/utils/savedmodels/model.h5"
Model = load_model(model_path)

tokenizer_path = "F:/Python Web Projects/FLASK/AI Services/aiServices/smsSpamClassification/utils/savedmodels/tokenizer.pkl"
tokenizer = pickle.load(open(tokenizer_path, 'rb'))

def DataCleaner(x):
    x = BeautifulSoup(x, 'html.parser').get_text() # remove html tags
    x = re.sub(r'(http|ftp|https)\S+\s*', '', x)  # remove URLs
    x = re.sub(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', '', x) # remove Emails
    x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore') # remove Accented Text
    x = " ".join([cont.fix(word.lower()) for word in x.split()]) # we expand the contraction of words
    x = re.sub('[^a-zA-Z0-9]+', ' ', x) # here we replace all with a space character except for alphaNumericals.
    x = " ".join([word.lower() for word in x.split()])  # remove extra whitespace around the words.
    return x

def getPrediction(txt, maxlen):
    x = copy.deepcopy(txt)
    x = DataCleaner(x)
    x = tokenizer.texts_to_sequences([x])
    x = pad_sequences(x, maxlen=maxlen)
    return Model.predict(x)[0][0]

def getBatchPrediction(input_file_path, output_file_path, maxlen):
    df = pd.read_csv(input_file_path)
    df_copy = df.copy()
    df.columns = ['review']
    x = df['review'].apply(lambda x: DataCleaner(x)).values
    x = tokenizer.texts_to_sequences(x)
    x = pad_sequences(x, maxlen=maxlen)
    output = Model.predict(x)
    df_copy['spam_score'] = output ## attach output to the copy of dataframe
    df_copy.to_csv(output_file_path, index=False)
    spam = (output > 0.5).sum()
    ham = output.shape[0] - spam 
    return spam, ham

spamText = "I'm gonna be home soon and i don't want to talk about this stuff anymore tonight, k? I've cried enough today."
hamText = "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's"
maxlen = 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', help="1 if batch prediction 0 otherwise")
    parser.add_argument('--input_data', help="pass input for getPrediction()")
    parser.add_argument('--input_file_path', help="pass csv file path to read")
    parser.add_argument('--output_file_path', help="pass csv file path to save")
    args = parser.parse_args()

    if args.batch == '1':
        spam, ham = getBatchPrediction(args.input_file_path, args.output_file_path, maxlen)
        print(f'{spam},{ham}', end='') 
    else:
        output = getPrediction(args.input_data, maxlen)
        print(output, end='')