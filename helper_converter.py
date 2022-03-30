import re


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


