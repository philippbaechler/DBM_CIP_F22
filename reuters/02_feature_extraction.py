#!/usr/bin/env python3
'''Extracts features from previously downloaded html files and saves them on the table "reuters_src.csv".

The target features are: article_date_time, title, description, main_author, reporters, writers, editors, content_channel, key_words, text, url

Usage:
    $ python3 02_feature_extraction.py
    or 
    $ chmod +x 02_feature_extraction.py
    $ ./02_feature_extraction.py

Author:
    Philipp Bächler - 22.5.2022

License:
    "THE BEER-WARE LICENSE" (Revision 42):
    philipp.baechler@gmail.com wrote this file. As long as you retain this notice
    you can do whatever you want with this stuff. If we meet some day, and you 
    think this stuff is worth it, you can buy me a beer in return.
'''


# %%
import os
import re
import pandas as pd
import glob
from bs4 import BeautifulSoup as bs


# %%
# The articles_html is a list which contains all the paths to the html files which are 
# located in data/raw/reuters/.
curren_dir = os.path.abspath(os.getcwd())
path_to_data = "../data/raw/reuters/"
articles_html = [f for f in glob.glob(path_to_data + "**/**/*.html", recursive=True)]
print(len(articles_html))


# %%
# Some cleaning steps had to be done by hand. This can be for example when the author name consists
# of four names but it should have been two persones with each first and last name. This dictionary 
# "translates" the faulty strings which were found in the 40'000 articles
fix_name_dict = {"Roberta Rampton Susan Cornwell": "Roberta Rampton, Susan Cornwell",
                 "Steve Holland Amanda Becker": "Steve Holland, Amanda Becker",
                 "Emily Stephenson Timothy Ahmann": "Emily Stephenson, Timothy Ahmann",
                 "Caren Bohan David Brunnstrom": "Caren Bohan, David Brunnstrom",
                 "Amy Tennery Luciana Lopez": "Amy Tennery, Luciana Lopez",
                 "Sandra Maler Simon Cameron-Moore": "Sandra Maler, Simon Cameron-Moore",
                 "Amanda Becker Yasmeen Abutaleb": "Amanda Becker, Yasmeen Abutaleb",
                 "Nathan Layne Karen Freifeld": "Nathan Layne, Karen Freifeld",
                 "Phil Berlowitzand Leslie Adler": "Phil Berlowitzand, Leslie Adler",
                 "Sarah N. Lynch Mark Hosenball": "Sarah N. Lynch, Mark Hosenball",
                 "Cynthia Ostermanand Leslie Adler": "Cynthia Ostermanand, Leslie Adler",
                 "David Lawder Timothy Gardner": "David Lawder, Timothy Gardner",
                 "Alaa Swilam Nayera Abdallah": "Alaa Swilam, Nayera Abdallah",
                 "Rosalba O’Brienand Nick Zieminski": "Rosalba O'Brienand, Nick Zieminski",
                 "Yuka Obayashi Tim Kelly": "Yuka Obayashi, Tim Kelly",
                 "Tom Lasseter Julie Marquis": "Tom Lasseter, Julie Marquis",
                 "Noel Randewichin San Francisco": "Noel Randewichin in San Francisco",
                 "Gabrielle Tétrault-Farber Anton Kolodyazhnyy": "Gabrielle Tétrault-Farber, Anton Kolodyazhnyy",
                 "Bernadette Baumand Tom Brown": "Bernadette Baumand, Tom Brown",
                 "Peter Szekely Maria Caspani": "Peter Szekely, Maria Caspani",
                 "Tom Daly Gabriel Crossley": "Tom Daly, Gabriel Crossley",
                 "Abdel Nasser Aboul el-Fadl": "Abdel Nasser, Aboul el-Fadl",
                 "Susana Vera Guillermo Martinez": "Susana Vera, Guillermo Martinez",
                 "David Brunnstrom Jonathan Landay": "David Brunnstrom, Jonathan Landay",
                 "Jack Tarrant Mitch Phillips": "Jack Tarrant, Mitch Phillips",
                 "Joao Manuel Vicente Mauricio": "Joao Manuel, Vicente Mauricio",
                 "Pete Schroeder Svea Herbst-Bayliss": "Pete Schroeder, Svea Herbst-Bayliss",
                 "Andrea Shalal Jonathan Landay": "Andrea Shalal, Jonathan Landay",
                 "Ana Nicolaci da COsta": "Ana Nicolaci da Costa",
                 "Christinne Muschi Montreal": "Christinne Muschi in Montreal",
                 "Bill Berkrot Jonathan Oatis": "Bill Berkrot, Jonathan Oatis",
                 "Saumyadeb Chakrabarty Maju Samuel": "Saumyadeb Chakrabarty, Maju Samuel",
                 "Caroline Stauffer Matthew Lewis": "Caroline Stauffer Matthew Lewis",
                 "Adrian Portugal Peter Blaza": "Adrian Portugal, Peter Blaza	",
                 "Lisa Lambert David Morgan": "Lisa Lambert, David Morgan",
                 "Angus MacSwan Giles Elgood": "Angus MacSwan, Giles Elgood",
                 "Michael Erman iNew Jersey": "Michael Erman in New Jersey",
                 "Kirsten Donovan Muralikumar Anantharaman": "Kirsten Donovan, Muralikumar Anantharaman",
                 "Steve Holland Trevor Hunnicutt": "Steve Holland, Trevor Hunnicutt",
                 "David Shepardson Jonathan Landay": "David Shepardson, Jonathan Landay",
                 "Jonathan Oatisand Jonathan Oatis": "Jonathan Oatis",
                 "Vanessa OConnell Nick Zieminski": "Vanessa OConnell, Nick Zieminski",
                 "Peter Cooneyand Peter Cooney": "Peter Cooney",
                 "Doina Chiacu Susan Cornwell": "Doina Chiacu, Susan Cornwell",
                 "Angelo Amante Crispian Balmer": "Angelo Amante, Crispian Balmer",
                 "Cecile Mantovani Ayenat Mersie": "Cecile Mantovani, Ayenat Mersie",
                 "Kate Holton James Davey": "Kate Holton, James Davey",
                 "Anil DSilva Josephine Mason": "Anil DSilva, Josephine Mason",
                 "Hugh Lawson Mark Potter": "Hugh Lawson, Mark Potter",
                 "Laila Bassam Yasmin Hussein": "Laila Bassam, Yasmin Hussein",
                 "Matthew Lewisand Peter Cooney": "Matthew Lewisand, Peter Cooney",
                 "Mary Millikenm Grant McCool": "Mary Millikenm, Grant McCool",
                 "Mariya Gordeeva Robin Paxton": "Mariya Gordeeva, Robin Paxton",
                 "Steve Holland Nandita Bose": "Steve Holland, Nandita Bose",
                 "Dan Whitcomb Rajesh Kumar Singh": "Dan Whitcomb, Rajesh Kumar Singh",
                 "Suleiman Al-Khalidi Nandita Bose": "Suleiman Al-Khalidi, Nandita Bose",
                 "Maju Samuel Aditya Soni": "Maju Samuel, Aditya Soni",
                 "Bryan Woolston Kacper Pempel": "Bryan Woolston, Kacper Pempel",
                 "Susanne Neumayer-Remter Tanya Wood Petra Wischgoll": "Susanne Neumayer-Remter, Tanya Wood, Petra Wischgoll"}


# %%
def fix_unknown_characters(string_input):
    string_input = string_input.replace("&#039;", "'")
    string_input = string_input.replace("&#39;", "'")
    string_input = string_input.replace("&quot;", "\"")
    string_input = string_input.replace("&rsquo;", "’")
    string_input = string_input.replace("&lsquo;", "‘")
    string_input = string_input.replace("&rdquo;", "”")
    string_input = string_input.replace("&ldquo;", "“")
    string_input = string_input.replace("&amp;", "&")
    string_input = string_input.replace("\xa0", " ")
    string_input = string_input.replace("&nbsp;", " ")
    return string_input


def remove_html_content(string_input):
    html_contents = re.findall(r"<(.*?)>", string_input)
    for content in html_contents:
        string_input = string_input.replace(("<" + content + ">"), " ")
    return string_input


def remove_new_line_character(string_input):
    return string_input.replace("\n", "")


def join_paragraphs_to_text(list_of_paragraphs):
    return ' '.join(list_of_paragraphs)



# %%
# For each feature we want to extract is here a short function defined. As it might be that some
# html pages are structured different or that some elements cannot be found on the page, we use
# the "try - except" functionality on each function. If something did not work as expected, we
# simply return an NaN, [] or "".  

def get_key_words(article_soup):
    try:
        return article_soup.find("meta", attrs={'name':'keywords'}).attrs["content"].split(",")
    except:
        return []


def get_title(article_soup):
    try:
        title = article_soup.find("meta", attrs={'name':'analyticsAttributes.title'})
        if title == None:
            title = article_soup.find("meta", attrs={'property':'og:title'})
        return title.attrs["content"]
    except:
        return ""
    

def get_article_date_time(article_soup):
    try:
        article_datetime = article_soup.find("meta", attrs={'name':'analyticsAttributes.articleDate'})
        if article_datetime == None:
            article_datetime = article_soup.find("meta", attrs={'name':'article:published_time'})
        return pd.to_datetime(article_datetime.attrs["content"])
    except:
        return ""


def get_main_authors(article_soup):
    try:
        author_names = article_soup.find("meta", attrs={'name':'analyticsAttributes.author'})
        if author_names == None:
            author_names = article_soup.find("meta", attrs={'name':'article:author'})
        return author_names.attrs["content"].split(",")
    except:
        return ""


def split_author_names(names):
    for key, value in fix_name_dict.items():
        if key in names:
            names = names.replace(key, value)
    return re.split(' and |,and | amd | anf | anfd | And | nd | nad | abd | asnd | ad | an | & |, |,|，|/| aboard ', names)


def get_reporters_writers_and_editors(article_soup):
    # In the end of almost each article a line of attribution like the following can be found. 
    # "Reporting by Brenda Goh, Albee Zhang and Tony Munroe; Writing by Justyna Pawlak; Editing by William Mallard, William Maclean"
    # This function returns a lists for reporters, writers and editors. 
    try:
        substrings = article_soup.find("body").get_text()
        substrings = re.split('\n|; |Our Standards', substrings)
        reporters = []
        editors = []
        writers = []
        
        for substring in substrings:
            if "reporting by" in substring.lower():
                reporter = re.findall(r"[rR]eporting\sby\s(.*)", substring)
                if len(reporter) != 0:
                    reporters.append(split_author_names(reporter[0]))
            elif "editing by" in substring.lower():
                editor = re.findall(r"[eE]diting\sby\s(.*)", substring)
                if len(editor) != 0:
                    editors.append(split_author_names(editor[0]))
            elif "writing by" in substring.lower():
                writer = re.findall(r"[wW]riting\sby\s(.*)", substring)
                if len(writer) != 0:
                    writers.append(split_author_names(writer[0]))
        return sum(reporters, []), sum(writers, []), sum(editors, [])
    except:
        return [],[],[]


def get_url(article_soup):
    try:
        article_url = article_soup.find("meta", attrs={'name':'analyticsAttributes.canonicalUrl'})
        if article_url == None:
            article_url = article_soup.find("meta", attrs={'property':'og:url'})
        return article_url.attrs["content"]
    except:
        return ""


def get_contentChannel(article_soup):
    try:
        return article_soup.find("meta", attrs={'name':'analyticsAttributes.topicChannel'}).attrs["content"]
    except:
        return ""


def get_description(article_soup):
    try:
        return article_soup.find("meta", attrs={'name':'description'}).attrs["content"]
    except:
        return ""


def get_paragraphs(article_soup):
    paragraphs = article_soup.find_all("p")
    if len(paragraphs) > 0:
        paragraphs = [paragraph.get_text() for paragraph in paragraphs]
        paragraphs = [remove_html_content(paragraph) for paragraph in paragraphs]
        paragraphs = [remove_new_line_character(paragraph) for paragraph in paragraphs]
        paragraphs = [re.sub("([ ]{2,})", "", paragraph) for paragraph in paragraphs]
        if "Min Read" in paragraphs[0]:
            paragraphs.pop(0)
        return paragraphs
    else:
        return []


def get_article_id(article_url):
    return article_url.split("-id")[-1].replace(".html", "")


# %%
# Here we loop over the list of article htmls, open it and extract the desired features by calling the previously
# defined functions. For each article all features are combined in a dictionary and appended to the articles list. 

articles = []

for idx, article in enumerate(articles_html):
    if idx >= 1000: # for debugging
        break
    with open(article) as data:
        data = data.read()
        data = fix_unknown_characters(data)
        soup = bs(data, 'html.parser')
        key_words = get_key_words(soup)
        title = get_title(soup)
        article_date_time = get_article_date_time(soup)
        main_author = get_main_authors(soup)
        reporters, writers, editors = get_reporters_writers_and_editors(soup)
        article_url = get_url(soup)
        content_channel = get_contentChannel(soup)
        description = get_description(soup)
        paragraphs = get_paragraphs(soup)
        article_text = join_paragraphs_to_text(paragraphs)
        articles.append({"article_date_time": article_date_time, "title": title, "description": description, \
                         "main_author": main_author, "reporters": reporters, \
                         "writers": writers, "editors": editors, "content_channel": content_channel, \
                         "key_words": key_words, "text": article_text, "url": article_url})


# %%
# Convert the articles into an pandas dataframe.
df = pd.DataFrame(articles)
df = df.astype(str).drop_duplicates().reset_index(drop=True)
df.head(10)


# %%
# Save the dataframe in a csv.
df.to_csv("../data/output/reuters_src.csv")


# %%
