import pandas as pd
import string
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import Counter

def removePunctuation(data):
    for char in data:
        if char in string.punctuation:
            data=data.replace(char,' ')
    return data

def removeApostrophe(data):
    for char in data:
        if char is "'":
            data=data.replace(char,'')
    return data

def removeSingleCharacters(data):
    words = nltk.word_tokenize(data)
    newText=""
    for word in words:
        if len(word)>1 or word=='i':
            newText=newText+" "+word
    return newText

def removeStopwords(data):
    affir=['am', 'is', 'are', 'was','were','would','can','could','should','do','does','did','will','shall']
    words = nltk.word_tokenize(data)
    stopwordslist= stopwords.words('english')
    stopwordslist.remove('what')
    stopwordslist.remove('when')
    stopwordslist.remove('who')
    newText=""
    for i in range(len(words)):
        if words[0] in affir and i==0:
            if words[1] in stopwordslist:
                newText+=" "+words[i]+" "+words[1]
        if words[i] not in stopwordslist:
            newText=newText+" "+words[i]
#    if words[-1] not in stopwordslist:
#        newText=newText+" "+words[-1]
    return newText

def removedigits(data):
    words = nltk.word_tokenize(data)
    newText=""
    for word in words:
        if word.isdigit() == False:
            newText=newText+" "+word
    return newText

def stemming(data):
    stemmer=PorterStemmer()
    words = nltk.word_tokenize(data)
    newText=""
    for word in words:
        word=stemmer.stem(word)
        newText=newText+" "+word
    return newText

def preprocess(data):
    data = removePunctuation(data)
    data = removeApostrophe(data)
    data = removeSingleCharacters(data)
    data = removeStopwords(data)
    data = removedigits(data)
    data = stemming(data)
    return data

def predict(dict4,dict1,dict2,dict3,whoNew,whatNew,whenNew,affirmationNew,question):
    words = nltk.word_tokenize(question)
    if question=='':
        return 'Invalid Input'
    score1=0
    score2=0
    score3=0
    score4=0
    for word in words:
        if word in whoNew:
            score4+=dict4[word]
        if word in whatNew:
            score1+=dict1[word]
        if word in whenNew:
            score2+=dict2[word]
        if word in affirmationNew:
            score3+=dict3[word]
    if max(score1,score2,score3,score4)==score1:
        predict1='what'
    elif max(score1,score2,score3,score4)==score2:
        predict1='when'
    elif max(score1,score2,score3,score4)==score3:
        predict1='affirmation'
    elif max(score1,score2,score3,score4)==score4:
        predict1='who'
    else:
        predict1='unknown'
    return predict1

df=pd.read_csv("LabelledData (1).txt",sep=' ,,, ',names=['question','label'])
questions=df['question']
labels=df['label']
who=[]
what=[]
when=[]
affirmation=[]

for i in range(len(questions)):
    questions[i]=preprocess(questions[i])
for j in range(len(questions)):
    words = nltk.word_tokenize(questions[j])
    if labels[j] == 'what':
        what=what+words
    elif labels[j] == 'when':
        when=when+words
    elif labels[j] == 'affirmation':
        affirmation=affirmation+words
    elif labels[j] == 'who':
        who=who+words
whoNew=list(set(who))
whatNew=list(set(what))
whenNew=list(set(when))
affirmationNew=list(set(affirmation))
duplicate=[whoNew, whatNew, whenNew, affirmationNew]

dict1=dict(zip(whatNew, (0 for k in whatNew)))
dict2=dict(zip(whenNew, (0 for k in whenNew)))
dict3=dict(zip(affirmationNew, (0 for k in affirmationNew)))
dict4=dict(zip(whoNew, (0 for k in whoNew)))
for x in what:
    dict1[x]+=1
for x in when:
    dict2[x]+=1
for x in affirmation:
    dict3[x]+=1
for x in who:
    dict4[x]+=1
#print(dict1,dict2,dict3)
#print(dict3)

dictionary=[dict4,dict1,dict2,dict3]
val=[]
for i in range(len(dictionary)):
    k=Counter(dictionary[i])
    vector=k.most_common(20)
    num=0
    for j in vector:
        num+=j[1]
    for word in duplicate[i]:
        val=dictionary[i][word]/num
        dictionary[i][word]=val


predicted=[]
for i in range(len(questions)):
    predicted.append(predict(dict4,dict1,dict2,dict3,whoNew,whatNew,whenNew,affirmationNew,questions[i]))


count=0
for i in range(len(labels)):
    if predicted[i]==labels[i]:
        count+=1
accuracy=(count/len(predicted))*100
print(accuracy)
input1=input("Enter the question: ")
input1=preprocess(input1.lower())
output=predict(dict4,dict1,dict2,dict3,whoNew,whatNew,whenNew,affirmationNew,input1)
print(output)
valid=input("Run again(y/n): ")
while(valid=='y' or valid=='Y'):
    input1=input("Enter the question: ")
    input1=preprocess(input1.lower())
    output=predict(dict4,dict1,dict2,dict3,whoNew,whatNew,whenNew,affirmationNew,input1)
    print(output)
    valid=input("Run again(y/n): ")