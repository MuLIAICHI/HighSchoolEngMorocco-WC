import streamlit as st
import requests
from html.parser import HTMLParser
import nlp_rake
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set Title
st.title('MAROCZN SCHOOLS WORD CLOUD')

# Step 1: Getting the Data
st.subheader('Step 1: Getting the Data')
user_input = 'https://fr.wikipedia.org/wiki/%C3%89cole_des_sciences_de_l%27information'
text = requests.get(user_input).content.decode('utf-8')
st.write(text[:1000])  # Displaying a preview of the fetched text

# Step 2: Transforming the Data
st.subheader('Step 2: Transforming the Data')
class MyHTMLParser(HTMLParser):
    script = False
    res = ""

    def handle_starttag(self, tag, attrs):
        if tag.lower() in ["script", "style"]:
            self.script = True

    def handle_endtag(self, tag):
        if tag.lower() in ["script", "style"]:
            self.script = False

    def handle_data(self, data):
        if str.strip(data) == "" or self.script:
            return
        self.res += ' ' + data.replace('[ edit ]', '')

parser = MyHTMLParser()
parser.feed(text)
text = parser.res
st.write(text[:1000])  # Displaying a preview of the parsed text

# Step 3: Getting Insights
st.subheader('Step 3: Getting Insights')
extractor = nlp_rake.Rake(max_words=2, min_freq=3, min_chars=5)
res = extractor.apply(text)
st.write(res)

# Step 4: Visualizing the Result (Bar Plot)
st.subheader('Step 4: Visualizing the Result (Bar Plot)')

def plot_bar(pair_list):
    k, v = zip(*pair_list)
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(k)), v)
    plt.xticks(range(len(k)), k, rotation='vertical')
    plt.xlabel('Keywords')
    plt.ylabel('Score')
    plt.title('Keyword Extraction')
    st.pyplot()

plot_bar(res)

# Step 5: Visualizing the Result (Word Cloud)
st.subheader('Step 5: Visualizing the Result (Word Cloud)')
wc = WordCloud(background_color='white', width=800, height=600)
wc.generate_from_frequencies({k: v for k, v in res})
plt.figure(figsize=(15, 7))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
st.pyplot()
