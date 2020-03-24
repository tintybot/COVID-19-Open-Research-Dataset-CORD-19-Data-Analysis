import os
import json
import pandas as pd
from tqdm import tqdm
import numpy as np
from nltk.corpus import wordnet
import re
import matplotlib.pyplot as plt
from nltk.corpus import stopwords 
from geotext import GeoText
#lets say we are searching for 'transmission'
synonyms=["spread","transmit","transmission","transmitted"]
for syn in wordnet.synsets("transmission"):
    for name in syn.lemma_names():
        if name not in synonyms:
        	synonyms.append(name)

for syn in wordnet.synsets("spread"):
    for name in syn.lemma_names():
        if name not in synonyms:
        	synonyms.append(name)

#print(synonyms)

#load a file
dirs_=["biorxiv_medrxiv\\biorxiv_medrxiv",
"comm_use_subset\\comm_use_subset",
"noncomm_use_subset\\noncomm_use_subset",
"pmc_custom_license\\pmc_custom_license"]

data_=list()
for dir_ in dirs_:
	for filename in tqdm(os.listdir(dir_)):

		#reading the file
		with open(os.path.join(dir_,filename)) as file:
			data=json.loads(file.read())
		
		#take out the data from the json format
		paper_id=data['paper_id']
		meta_data=data['metadata']
		abstract=data['abstract']
		abstract_text=""
		for text in abstract:
			abstract_text+=text['text']+" "
		body_text=data['body_text']
		full_text=""
		for text in body_text:
			full_text+=text['text']+" "
		back_matter=data['back_matter']
		#store everything to a dataframe
		data_.append([paper_id,abstract_text,full_text])

df=pd.DataFrame(data_,columns=['paper_id','abstract','full_text'])
#save as a csv
#df.to_csv('biorxiv_medrxiv.csv', index = True)
#a data frame for my complete body.


#############################################################################################

synonyms_=["coronavirus","Covid-19","COVID 19","Coronavirus","Corona virus","COVID 19"]
#transmission and its synonyms related body are taken for consideration
transmission_synonym=df[df['full_text'].str.contains('|'.join(synonyms_))]
keys_=["transmitted","transmits"]
my_data=list()
#looping through each paper
for texts in transmission_synonym['full_text']:

	#looping through each sentence
	for tex in texts.split(". "):

		#checking if my keyswords is present in those sentences or not
		for wor_ in keys_:
			if wor_ in tex:
				#print(tex)
				#print()
				#print()
				my_data.append(tex)


###############################################################################################

#print(len(my_data))
#create a word bucket
#remove stop words and punctions
punctuations='''!()[,]{\};:'"<>./?@#$%^&*_~'''
stopwords=set(stopwords.words('english'))
#print(stopwords)
word_bucket=dict()
string=""
#loop through lines
for lines in my_data:
	#loop through words of each line
	for words in lines.split(" "):

		#for all non-alphanumeric words
		if words.isalpha() == False:

			#remove punctions
			for chrs in words:
				if chrs in punctuations:
					words=words.replace(chrs,"")

			#convert to lower case
			words=words.lower()

			#removing names of citiesfrom geotext import GeoText
			places = GeoText(words)
			city=places.cities
			country=places.countries

			#remove the stopwords
			if words not in stopwords and len(re.findall("\d|transmi|also",words))==0 and len(words)>3 and (len(city)+len(country))==0:

				lexemes=re.findall(words,string)
				#print(lexemes)

				if words not in word_bucket.keys() and len(lexemes)==0:
					#add new elemnts
					word_bucket[words]=1
					string=string+" "+words
				else:
					#freq of occurances
					try:
						word_bucket[words]=word_bucket[words]+1
					except:
						pass



analytics=dict()
for keys in word_bucket:
	#print(keys)
	if int(word_bucket[keys])>4:
		analytics[keys]=word_bucket[keys]
		#print(keys)

#print(len(analytics))
############################################################################################################
common_words=[]
with open("commonwords.txt") as file:
	rows=file.read()
for w_ in rows.split("\n"):
	common_words.append(w_)

#bar graphs
freq=[]
for w_ in common_words:
	if w_ in analytics.keys():
		freq.append(analytics[w_])
#print(freq)
plt.barh(common_words,freq)
plt.xlabel("Frequency")
plt.ylabel("Factors of transmission")
plt.title("Probable causes of Transmission")
plt.show()
		
