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

model_path = "F:/Python Web Projects/FLASK/AI Services/aiServices/fakeNewsClassification/utils/savedmodels/model.h5"
Model = load_model(model_path)

tokenizer_path = "F:/Python Web Projects/FLASK/AI Services/aiServices/fakeNewsClassification/utils/savedmodels/tokenizer.pkl"
tokenizer = pickle.load(open(tokenizer_path, 'rb'))

def DataCleaner(x):
    x = BeautifulSoup(x, 'html.parser').get_text() # remove html tags
    x = re.sub(r'(http|ftp|https)\S+\s*', '', x)  # remove URLs
    x = re.sub(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', '', x) # remove Emails
    x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore') # remove Accented Text
    x = " ".join([cont.fix(word.lower()) for word in x.split()]) # we expand the contraction of words
    x = re.sub('[^a-zA-Z0-9]+', ' ', x) # here we replace all with a space character except for Alpha numericals.
    x = x.lower()
    
    # removing unwanted words that has a text length of 1 like 't', 's' etc
    useful_chars = ['a', 'i', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    x = " ".join([word for word in x.split() if len(word) != 1 or word in useful_chars])
    
    # correct some words like 're' to 'are' etc
    correct = {'re' : 'are', 'couldn' : 'could not'}
    x = " ".join([correct[word] if word in correct.keys() else word for word in x.split()])
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
    new_cols = ['text']
    col_map = dict(zip(df.columns, new_cols))
    df.rename(col_map, axis=1, inplace=True)
    x = df['text'].apply(lambda x: DataCleaner(x)).values
    x = tokenizer.texts_to_sequences(x)
    x = pad_sequences(x, maxlen=maxlen)
    output = Model.predict(x)
    df_copy['fake_score'] = output ## attach output to the copy of dataframe
    df_copy.to_csv(output_file_path, index=False)
    fake = (output > 0.5).sum()
    real = output.shape[0] - fake 
    return fake, real

fakeText = str("""Donald Trump Sends Out Embarrassing New Year's Eve Message; This is Disturbing, Donald Trump just couldn t wish all Americans a Happy New Year and leave it at that. Instead, he had to give a shout out to his enemies, haters and  the very dishonest fake news media.  The former reality show star had just one job to do and he couldn t do it. As our Country rapidly grows stronger and smarter, I want to wish all of my friends, supporters, enemies, haters, and even the very dishonest Fake News Media, a Happy and Healthy New Year,  President Angry Pants tweeted.  2018 will be a great year for America! As our Country rapidly grows stronger and smarter, I want to wish all of my friends, supporters, enemies, haters, and even the very dishonest Fake News Media, a Happy and Healthy New Year. 2018 will be a great year for America!  Donald J. Trump (@realDonaldTrump) December 31, 2017Trump s tweet went down about as welll as you d expect.What kind of president sends a New Year s greeting like this despicable, petty, infantile gibberish? Only Trump! His lack of decency won t even allow him to rise above the gutter long enough to wish the American citizens a happy new year!  Bishop Talbert Swan (@TalbertSwan) December 31, 2017no one likes you  Calvin (@calvinstowell) December 31, 2017Your impeachment would make 2018 a great year for America, but I ll also accept regaining control of Congress.  Miranda Yaver (@mirandayaver) December 31, 2017Do you hear yourself talk? When you have to include that many people that hate you you have to wonder? Why do the they all hate me?  Alan Sandoval (@AlanSandoval13) December 31, 2017Who uses the word Haters in a New Years wish??  Marlene (@marlene399) December 31, 2017You can t just say happy new year?  Koren pollitt (@Korencarpenter) December 31, 2017Here s Trump s New Year s Eve tweet from 2016.Happy New Year to all, including to my many enemies and those who have fought me and lost so badly they just don t know what to do. Love!  Donald J. Trump (@realDonaldTrump) December 31, 2016This is nothing new for Trump. He s been doing this for years.Trump has directed messages to his  enemies  and  haters  for New Year s, Easter, Thanksgiving, and the anniversary of 9/11. pic.twitter.com/4FPAe2KypA  Daniel Dale (@ddale8) December 31, 2017Trump s holiday tweets are clearly not presidential.How long did he work at Hallmark before becoming President?  Steven Goodine (@SGoodine) December 31, 2017He s always been like this . . . the only difference is that in the last few years, his filter has been breaking down.  Roy Schulze (@thbthttt) December 31, 2017Who, apart from a teenager uses the term haters?  Wendy (@WendyWhistles) December 31, 2017he s a fucking 5 year old  Who Knows (@rainyday80) December 31, 2017So, to all the people who voted for this a hole thinking he would change once he got into power, you were wrong! 70-year-old men don t change and now he s a year older.Photo by Andrew Burton/Getty Images.,News, December 31, 2017""")
realText = """"As U.S. budget fight looms, Republicans flip their fiscal script","WASHINGTON (Reuters) - The head of a conservative Republican faction in the U.S. Congress, who voted this month for a huge expansion of the national debt to pay for tax cuts, called himself a “fiscal conservative” on Sunday and urged budget restraint in 2018. In keeping with a sharp pivot under way among Republicans, U.S. Representative Mark Meadows, speaking on CBS’ “Face the Nation,” drew a hard line on federal spending, which lawmakers are bracing to do battle over in January. When they return from the holidays on Wednesday, lawmakers will begin trying to pass a federal budget in a fight likely to be linked to other issues, such as immigration policy, even as the November congressional election campaigns approach in which Republicans will seek to keep control of Congress. President Donald Trump and his Republicans want a big budget increase in military spending, while Democrats also want proportional increases for non-defense “discretionary” spending on programs that support education, scientific research, infrastructure, public health and environmental protection. “The (Trump) administration has already been willing to say: ‘We’re going to increase non-defense discretionary spending ... by about 7 percent,’” Meadows, chairman of the small but influential House Freedom Caucus, said on the program. “Now, Democrats are saying that’s not enough, we need to give the government a pay raise of 10 to 11 percent. For a fiscal conservative, I don’t see where the rationale is. ... Eventually you run out of other people’s money,” he said. Meadows was among Republicans who voted in late December for their party’s debt-financed tax overhaul, which is expected to balloon the federal budget deficit and add about $1.5 trillion over 10 years to the $20 trillion national debt. “It’s interesting to hear Mark talk about fiscal responsibility,” Democratic U.S. Representative Joseph Crowley said on CBS. Crowley said the Republican tax bill would require the  United States to borrow $1.5 trillion, to be paid off by future generations, to finance tax cuts for corporations and the rich. “This is one of the least ... fiscally responsible bills we’ve ever seen passed in the history of the House of Representatives. I think we’re going to be paying for this for many, many years to come,” Crowley said. Republicans insist the tax package, the biggest U.S. tax overhaul in more than 30 years,  will boost the economy and job growth. House Speaker Paul Ryan, who also supported the tax bill, recently went further than Meadows, making clear in a radio interview that welfare or “entitlement reform,” as the party often calls it, would be a top Republican priority in 2018. In Republican parlance, “entitlement” programs mean food stamps, housing assistance, Medicare and Medicaid health insurance for the elderly, poor and disabled, as well as other programs created by Washington to assist the needy. Democrats seized on Ryan’s early December remarks, saying they showed Republicans would try to pay for their tax overhaul by seeking spending cuts for social programs. But the goals of House Republicans may have to take a back seat to the Senate, where the votes of some Democrats will be needed to approve a budget and prevent a government shutdown. Democrats will use their leverage in the Senate, which Republicans narrowly control, to defend both discretionary non-defense programs and social spending, while tackling the issue of the “Dreamers,” people brought illegally to the country as children. Trump in September put a March 2018 expiration date on the Deferred Action for Childhood Arrivals, or DACA, program, which protects the young immigrants from deportation and provides them with work permits. The president has said in recent Twitter messages he wants funding for his proposed Mexican border wall and other immigration law changes in exchange for agreeing to help the Dreamers. Representative Debbie Dingell told CBS she did not favor linking that issue to other policy objectives, such as wall funding. “We need to do DACA clean,” she said.  On Wednesday, Trump aides will meet with congressional leaders to discuss those issues. That will be followed by a weekend of strategy sessions for Trump and Republican leaders on Jan. 6 and 7, the White House said. Trump was also scheduled to meet on Sunday with Florida Republican Governor Rick Scott, who wants more emergency aid. The House has passed an $81 billion aid package after hurricanes in Florida, Texas and Puerto Rico, and wildfires in California. The package far exceeded the $44 billion requested by the Trump administration. The Senate has not yet voted on the aid. ",politicsNews,"December 31, 2017" """
maxlen = 1000

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', help="1 if batch prediction 0 otherwise")
    parser.add_argument('--input_data', help="pass input for getPrediction()")
    parser.add_argument('--input_file_path', help="pass csv file path to read")
    parser.add_argument('--output_file_path', help="pass csv file path to save")
    args = parser.parse_args()

    if args.batch == '1':
        fake, real = getBatchPrediction(args.input_file_path, args.output_file_path, maxlen)
        print(f'{fake},{real}', end='') 
    else:
        output = getPrediction(args.input_data, maxlen)
        print(output, end='')