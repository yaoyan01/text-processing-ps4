import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def main_parser(url, num):
    # initializing the url, page and its parser
    URL = url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    category_pages = []
    for h2 in soup.find_all("h2"):
        if "Pages in category" in h2.text:
            for a in h2.find_all_next("a", href=True, limit=num):
                if "wiki" in a["href"]:
                    category_pages.append(a["href"])

    final_text = [''] * num
    index = 0

    for c in category_pages:
        newURL = "https://en.wikipedia.org" + c

        # 1. go to the page
        newPage = requests.get(newURL)
        newSoup = BeautifulSoup(newPage.content, "html.parser")

        # 2. extract the text
        for info in newSoup.find_all("p"):
            final_text[index] += info.get_text()
        index += 1

    index = 0
    for strings in final_text:
        # 3. Replace all new lines with a single space.
        strings = strings.replace("\n", " ")

        # 4. Remove anything within square brackets or angle brackets.
        strings = re.sub(r'\[.*?\]', ' ', strings)
        strings = re.sub(r'\{.*?\}', ' ', strings)

        # 5. Save all of that as a string.
        # 6. Save that to the list of strings.
        final_text[index] = strings
        index += 1

    # creating a list of lists of tokens
    token_list = [] * num
    for string in final_text:
        listoftokens = nltk.word_tokenize(string)
        token_list.append(listoftokens)

    # creating stop words and adding more to them
    removed_stopwords_list = [] * num
    stoplist = stopwords.words('english')
    stoplist.extend([".", ",", "?", "'",
                    "!", ";", ":'", '"', "WikiProject", "wikiproject", "Category",
                     "category", "also", "(", ")", "[", "]", "{", "}" "Wikipedia", "article",
                     "Categories", "pages", "%", "may", "find", "soon", 'wikipedia', "e.g", "readers", "see", ":",
                     "however", "link", "introduction", "Similarly", "without", "categories", "help", ])

    # creating a list of list with all of the stop words removed from them
    for list in token_list:
        allcontenttokens = [x for x in list if x.lower() not in stoplist]
        removed_stopwords_list.append(allcontenttokens)

    # initliazing word lemmatizer
    all_lemmas_list = [] * num
    lemmatizer = WordNetLemmatizer()

    # creating a list of list after lemmatizing them
    for list in removed_stopwords_list:
        all_lemmas = [lemmatizer.lemmatize(x) for x in list]
        all_lemmas_list.append(all_lemmas)

    # creating text of the most common lemmas in the list
    for lemmas in all_lemmas_list:
        fdist = nltk.FreqDist(lemmas)
        text = " ".join(fdist)

    # generating the wordcloud
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    import sys
    main_parser(sys.argv[1], int(sys.argv[2]))
