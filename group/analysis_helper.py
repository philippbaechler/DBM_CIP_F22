def convert_string_to_list(string_input):
    return string_input.replace("'", "")\
                       .replace("[", "")\
                       .replace("]", "")\
                       .split(", ")


def check_if_word_occures_in_text(string_input, search_word):
    string_input = string_input.replace(".", "")
    words_list = string_input.split(" ")
    return any([word == search_word for word in words_list])


def count_occurences_in_text(string_input, search_word):
    string_input = string_input.replace(".", "")
    words_list = string_input.split(" ")
    return sum([word == search_word for word in words_list])


def is_search_word_in_text_from_df(df, search_word):
    occurences = []
    for row in df.iterrows():
        word_occures = check_if_word_occures_in_text(row[1]["text"], search_word)
        occurences.append(word_occures)
    return occurences


def get_occurences_per_month(df, search_word):
    df["occurences"] = is_search_word_in_text_from_df(df, search_word)
    return df.groupby(by=[df["year_month"]])["occurences"].sum().to_frame().reset_index()

