import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap

# Section 1 General Stat Functions
def __display_paper_yearly__(data):
    '''
    Display histogram of yearly news amount
    :param data: df with col 'publication year and amount'
    :return: a plot
    '''
    # matplotlib inline
    import matplotlib.pyplot as plt
    # fig = plt.figure()
    plt.figure(figsize=(35, 15))
    # plt.style.use('ggplot')

    # x = list(data.year)
    x = list(data['Publication Year'])
    y = list(data.amount)
    x_pos = [i for i, _ in enumerate(x)]

    # '#469EB4', '#4E62AB'
    # plt.bar(x_pos, y, width=0.80, color='#43a2ca')
    plt.bar(x_pos, y, width=0.80, color='#95A2C3')
    # plt.bar(x_pos, y, width=0.80, color='#469EB4')
    plt.xlabel("Year", fontsize=24, fontname="Arial")
    plt.ylabel("Paper Count", fontsize=24, fontname="Arial")

    plt.xticks(x_pos, x, fontsize=18)
    plt.yticks(fontsize=20)

    plt.gcf().autofmt_xdate()  # italics of x label

    plt.grid(True, linestyle='--', zorder=0)  # Dashed grid lines behind plot
    plt.gca().set_axisbelow(True)  # Set the grid lines below the bars
    plt.show()


def __count_authors__(data_col):
    '''
    Count the number of authors for each paper using the number of semicolon,
        num + 1 is the final number of author,
        if no semicolon, single author work
    :param data_col: author column
    :return: number of authors for each paper
    '''

    semicolon_count = data_col.count(';')
    if semicolon_count > 0:
        #print(semicolon_count)
        return semicolon_count + 1
    else:
        #print('No semicolon')
        return 1


def __display_authorship_yearly__(data):
    '''
    Display histogram of authorship_yearly
    :param data: df with col 'publication year and a_amount'
    :return: a plot
    '''

    import matplotlib.pyplot as plt

    # fig = plt.figure()
    plt.figure(figsize=(35, 15))
    # plt.style.use('ggplot')

    # x = list(data.year)
    x = list(data['Publication Year'])
    y = list(data.a_amount)
    x_pos = [i for i, _ in enumerate(x)]

    # '#469EB4', '#4E62AB'
    # plt.bar(x_pos, y, width=0.80, color='#43a2ca')
    # plt.bar(x_pos, y, width=0.80, color='#469EB4')

    # plt.plot(x_pos, y, marker='o', linestyle='-', color='#469EB4')
    plt.plot(x_pos, y, marker='o', linestyle='-', color='#95A2C3')

    # plt.scatter(x_pos, y, color= 'red')

    plt.xlabel("Year", fontsize=24, fontname="Arial")
    plt.ylabel("AVG Author", fontsize=24, fontname="Arial")

    plt.xticks(x_pos, x, fontsize=18)
    plt.yticks(fontsize=20)  # Adjust y tick labels size

    plt.gcf().autofmt_xdate()  # italics of x label
    plt.grid(True, linestyle='--')
    plt.show()

# End of Section 1

# create a data frame with topic number along with its freq and all words
def __get_topic_allwords__(all_topics, t_model):
    '''
    get all ll word representing the topic
    :param all_topics: topics from freq df
    :param t_model: topic model
    :return: df with topic number, freq, all word representing the topic
    '''

    #create 3 empty list
    topic_list = []
    freq_list = []
    words_list = []

    for topic in all_topics:
        #topic_name = "Topic" + str(topic)
        #topic_list.append(topic_name)
        topic_list.append(topic)
        # print(topic_name)
        frq = t_model.get_topic_freq(topic)
        freq_list.append(frq)
        wordset = t_model.get_topic(topic)[:15]
        # print("====Get item from get_topic Results====")
        topic_word = []
        for item in wordset:
            # print()
            # topic_word += '' + str(item[0])
            topic_word.append(item[0])

        words_list.append(topic_word)
    # words_list.append(join(topic_word))
    topics_df = pd.DataFrame(list(zip(topic_list, freq_list, words_list)), columns=['Topic', 'Freq', 'Allwords'])
    return topics_df


# Find related tooics with certain keywords
def Keyword_Search(keyword_list, topicmodel, valid_topic_list):
    similar_topic_list = []
    for keyWord in keyword_list:
        # find similar topics
        similar_topics, similarity = topicmodel.find_topics(keyWord, top_n=3)
        print("-Using keyword:", keyWord, "related", similar_topics)
        print(similarity)
        # append all topic from each set of similar topics
        for item in similar_topics:
            if item in valid_topic_list:
                similar_topic_list.append(item)
            else:
                pass

    # before drop dulicates
    print("Before remove", similar_topic_list)

    # remove duplicate item in list
    final_list = list(set(similar_topic_list))
    # print("Arfter remove", final_list)

    print("Final", keyWord, "related topic", final_list)

    for topicnum in final_list:
        print("Topic", topicnum)
        print(topicmodel.get_topic(topicnum))

    return final_list


# Section 3 Word Cloud Visual
def __gen_cloud_3_color__(data, w, h):  # Generate word cloud
    '''
    :param data: freq data
    :param w: width
    :param h: height
    :return: a word cloud figure
    '''

    # Define custom colormap with orange, blue, and green
    #colors = ['#386cb0', '#fdc086', '#7fc97f']  # Orange, Blue, Green
    # colors = ['#E07F86', '#fc8d62', '##8FA2CD']  # Orange, Blue, Green
    # colors = ['#4E62AB', '#87CFA4', '#F57547']
    colors = ['#95A2C3', '#AECD54', '#F2A93B']
    font_path = "src/DM_Sans/DMSans-VariableFont_opsz,wght.ttf"

    # cmap = LinearSegmentedColormap.from_list('custom', colors)
    cmap = ListedColormap(colors)
    wordcloud = WordCloud(width=w, height=h, background_color='white', colormap=cmap, prefer_horizontal=1,
                          font_path=font_path).generate_from_frequencies(data)

    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()