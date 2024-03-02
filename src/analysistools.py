import bertopic
import pandas as pd


# create a data frame with topic number along with its freq and all words
def _get_topic_allwords_(all_topics, t_model):
    topic_list = []
    freq_list = []
    words_list = []

    for topic in all_topics:
        topic_name = "Topic" + str(topic)
        topic_list.append(topic_name)
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
    topics_df = pd.DataFrame(list(zip(topic_list, freq_list, words_list)), columns=['Topic', 'Freq', 'Words'])
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
