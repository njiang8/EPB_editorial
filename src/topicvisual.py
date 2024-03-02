# All Visualization Functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# from chord import Chord # for visualization; "
#from plotapi import Chord


# import plotapi
# Chord.set_license("naj060@icloud.com", "PLOTAPI-P-6b5adba4-66f9-4086-8ce5-390c93b43a4a")
# from plotapi import Chord
# Chord.api_key("4ebe2263-fc0a-4093-9d1a-7a4a419266c0")

###################
# Part 1 Chord
###################

# V1; check n
def CreateKeywordsMatrix(keywordlist):
    print("Creating Topic Intersection Matrix...")

    # Get intersection number
    def IntersectAmout(list1, list2):
        # print("Get Intersection...")
        # get intersections
        temp = list(set(list1).intersection(list2))
        if temp == list1 or temp == list2:
            # return len(temp)
            return 0
        else:
            # print
            return len(temp)

    topicintersectmatrix = []  # new list
    # loop through the kewordlist
    for item in range(0, len(keywordlist)):
        # print('xxx')
        # print(item)
        # print(keywordlist[item])
        intersect_list = []
        for eachlist in keywordlist:
            # print(eachlist)
            intersect_list.append(IntersectAmout(keywordlist[item], eachlist))
        topicintersectmatrix.append(intersect_list)
        # print(intersect_list)
    # print(topicintersectmatrix)
    return topicintersectmatrix


def CreateTopicMatrix(keywordlist, topicintersectmatrix, narrtive_topics, keywords):
    print("Creating Topic Matrix...")
    # list hold all intersection amount
    matrix = []
    for item in range(0, len(keywordlist)):
        # print(item)
        # print(keywordlist[item])
        # if item <= 5:

        # intersect_list = topicintersectmatrix[item]
        intersect_list = [0] * 6
        # print(intersect_list)
        for topic in narrtive_topics:
            # print("For Topic", topic)
            if topic in keywordlist[item]:
                intersect_list.append(1)
            else:
                intersect_list.append(0)
            # intersect_list.append(IntersectAmout(keywordlist[item], eachlist))
        # intersect_list.extend([0] * 6)
        # print(len(intersect_list))
        matrix.append(intersect_list)
        # print(intersect_list)
    # print(matrix)
    # transpose the matrix
    transmatrix = np.array(matrix).T.tolist()

    # adding other elements for the final transmatrix
    for i in range(0, len(transmatrix)):
        # print(i)
        if i <= 5:
            transmatrix[i].extend(matrix[i][6:])
        else:
            transmatrix[i].extend([0] * len(narrtive_topics))

    final_keywords = keywords
    for t in narrtive_topics:
        final_keywords.append("Topic" + str(t))

    return transmatrix, final_keywords


# function generate chord diagram
def VisualizeChord(resultsmatrix, resultsmatrixnames):
    # from plotapi import Chord
    # Chord.api_key("4ebe2263-fc0a-4093-9d1a-7a4a419266c0")

    print("Creating Chord Diagram")
    colorlist = [
        "#00fa68", "#ff575c", "#ff914d", "#ffca38", "#f2fa00", "#C3F500", "#94f000",
        "#7f5e38", "#432818", "#6e4021", "#99582a", "#cc9f69", "#755939", "#BAA070",
        "#00C1A2", "#0087db", "#0054f0", "#5d00e0", "#2F06EB",
        "#6f1d1b", "#955939", "#A87748", "#bb9457"]

    Chord(resultsmatrix, resultsmatrixnames, color=colorlist, width=700,
          outer_radius_scale=1.2,
          padding=0.2,
          font_size="14px",
          font_size_large="14px",
          arc_numbers=True,
          animated_intro=True, animated_duration=10000
          ).show()
###############################END OF PART ONE#############################################


###################
# Part 2 Stack Bars
###################
# * Step1: Get the dataframe for the visualization
def GetTopicCountByYear(topiclist, evo_table, yearlycount):
    # extract the key info from eveolution table
    temp_df = evo_table.loc[:, ['Topic', 'Frequency', 'Timestamp']]
    # print(temp_df)

    # Loop through the keywords list to draw lins on Cavas
    topiclist.sort()
    # print("TopicList", topiclist)
    legend_list = []

    # Create a dataframe to hold the all topics, freq, year amount
    stack_df = pd.DataFrame()

    for item in range(0, len(topiclist)):
        topic = topiclist[item]
        topic_label = "Topic " + str(topic)
        # print("Topic", topic)
        legend_list.append("Topic" + str(topic))

        # Extract visulize dataframe
        visual_df = temp_df[temp_df.Topic == topic].reset_index(drop=True)
        visual_df = visual_df.rename(columns={'Timestamp': 'year'})  # rename timstamp to year fro merge
        # Merge on year
        final_visual_df = pd.merge(visual_df, yearlycount, on="year")
        # print(final_visual_df.head())
        #stack_df = stack_df.append(final_visual_df)
        stack_df = pd.concat([stack_df, final_visual_df])

    # group the df based on year and topics
    grouped_stack = stack_df.groupby(["year", "Topic"])["Frequency"].sum().reset_index()

    # pivot the dataframe into the correct format
    grouped_stack_df = grouped_stack.pivot(index='year', columns='Topic', values='Frequency').fillna(0).reset_index()
    # print(grouped_stack_df.head())

    return grouped_stack_df


# * Step2: Satcked bar visualization
# Get the topic evo for each topic
def GetTopicEvo(topiclist, overtime):  # topics list, topic_model, topic over time dataframe
    finaldataframe = pd.DataFrame()
    for topic in topiclist:
        # print(topic)
        tempdf = overtime[overtime.Topic == topic].reset_index(drop=True)
        # print(tempdf.head())
        # finaldataframe = finaldataframe.append(tempdf)
        finaldataframe = pd.concat([finaldataframe, tempdf])
    return finaldataframe


def VisualizeStackByYearColor(data, year_range, PlotTitle):  # 3String
    plt.style.use('default')

    # create the figure
    fig, ax = plt.subplots(figsize=(25, 10))
    # plt.figure(figsize=(25,10))
    plt.xlabel('Year', fontsize=30, fontname="Arial")
    plt.ylabel('Frequency', fontsize=30, fontname="Arial")

    print(len(data.columns[1:]))
    if len(data.columns[1:]) == 2:
        color_list = ['#4E62AB', '#FDB96A']

    if len(data.columns[1:]) == 3:
        color_list = ['#4E62AB', '#FDB96A', '#D6404E']

    if len(data.columns[1:]) == 4:
        color_list = ['#4E62AB', '#87CFA4', '#FDB96A', '#D6404E']

    if len(data.columns[1:]) == 5:
        color_list = ['#4E62AB', '#87CFA4', '#F5FBB1', '#FDB96A', '#D6404E']

    if len(data.columns[1:]) == 6:
        color_list = ['#4E62AB', '#87CFA4', '#CBE99D', '#FEE89A', '#F57547', '#9E0142']

    if len(data.columns[1:]) == 7:
        color_list = ['#4E62AB', '#469EB4', '#87CFA4', '#FEE89A', '#FDB96A', '#F57547', '#9E0142']

    if len(data.columns[1:]) == 8:
        color_list = ['#4E62AB', '#469EB4', '#87CFA4', '#F5FBB1', '#FEE89A', '#FDB96A', '#F57547', '#9E0142']

    if len(data.columns[1:]) == 9:
        color_list = ['#4E62AB', '#469EB4', '#87CFA4', '#F5FBB1', '#FEE89A', '#FDB96A', '#F57547', '#D6404E', '#9E0142']

    # Legend of the stacked bars
    bottom = 0
    colorid = 0
    legend_list = []
    for topic in data.columns[1:]:
        # legend
        topic_label = "Topic " + str(topic)
        # print("Topic", topic)
        legend_list.append("Topic" + str(topic))
        # bar plot
        # plt.bar(data.loc[:, 'year'], data[topic], bottom = bottom, width=0.95)
        plt.bar(data.index, data[topic], bottom=bottom, width=0.95, color=color_list[colorid])
        bottom = bottom + data[topic]
        colorid = colorid + 1

    # ax.set_title(PlotTitlem)
    plt.legend((legend_list), prop={'family': 'Arial', "size": 20}, loc='upper left', ncol=1)

    # set x ticks: dont' show the year without any topics
    #x_label = list(np.arange(data.year.min(), 2021, 5))
    #x_label.append(2021)
    #x_label = list(data.year)
    x_label = list(data["Publication Year"])
    print(x_label)

    x_ticks = []
    for year_index in range(0, len(x_label)):
        #print(year)
        year = x_label[year_index]
        try:
            temp = data[data['year'] == year].index[0]
            #print(temp)
        except:
            temp = data[data['year'] == year + 1].index[0]
        #if temp%5 == 0:
        x_ticks.append(temp)
    print(x_ticks)

    # x_ticks = data.index.to_list()
    # x_label = data.loc[:, 'year'].to_list()
    # x_label = np.arange(1975, 2021, 5)
    # Plot x and y axticks
    plt.gcf().autofmt_xdate()  # italics of x label
    plt.xticks(ticks=x_ticks, labels=x_label, fontsize=15)
    # plt.xticks(np.arange(1975, 2021, 5))
    plt.yticks(fontsize=25)
    plt.margins(x=0.01)
    plt.show()

def _visualsmall_(data, year_range):
    plt.style.use('default')

    print(len(data.columns[1:]))
    if len(data.columns[1:]) == 2:
        color_list = ['#4E62AB', '#FDB96A']

    if len(data.columns[1:]) == 3:
        color_list = ['#4E62AB', '#FDB96A', '#D6404E']

    if len(data.columns[1:]) == 4:
        color_list = ['#4E62AB', '#87CFA4', '#FDB96A', '#D6404E']

    if len(data.columns[1:]) == 5:
        color_list = ['#4E62AB', '#87CFA4', '#F5FBB1', '#FDB96A', '#D6404E']

    if len(data.columns[1:]) == 6:
        color_list = ['#4E62AB', '#87CFA4', '#CBE99D', '#FEE89A', '#F57547', '#9E0142']

    if len(data.columns[1:]) == 7:
        color_list = ['#4E62AB', '#469EB4', '#87CFA4', '#FEE89A', '#FDB96A', '#F57547', '#9E0142']

    if len(data.columns[1:]) == 8:
        color_list = ['#4E62AB', '#469EB4', '#87CFA4', '#F5FBB1', '#FEE89A', '#FDB96A', '#F57547', '#9E0142']

    if len(data.columns[1:]) == 9:
        color_list = ['#4E62AB', '#469EB4', '#87CFA4', '#F5FBB1', '#FEE89A', '#FDB96A', '#F57547', '#D6404E', '#9E0142']
    # ax = plt.axes()
    if year_range > 0:
        # figure and axis
        fig, ax = plt.subplots(1, figsize=(16, 9))
        plt.xlabel('Year', fontsize=20, fontname="Arial")

        print("Small plot is the topic before the year of ", year_range)
        year_index = data[data['year'] == year_range].index[0]
        # print(year_index.tolist())
        small_df = data.iloc[:year_index, :]  # .set_index('year')
        # print(small_df.tail())

        bottom = 0
        colorid = 0
        for topic in data.columns[1:]:
            # bar plot
            # plt.bar(small_df.loc[:, 'year'], small_df[topic], bottom = bottom, width=0.95)
            plt.bar(small_df.index, small_df[topic], bottom=bottom, width=0.95, color=color_list[colorid])
            bottom = bottom + small_df[topic]
            colorid = colorid + 1

        # remove spines
        # ax.spines['right'].set_visible(False)
        # ax.spines['left'].set_visible(False)
        # ax.spines['top'].set_visible(False)
        # ax.spines['bottom'].set_visible(False)
        x_ticks = small_df.index
        #x_label = small_df.loc[:, 'year'].to_list()
        x_label = small_df.loc[:, 'Publication Year'].to_list()

        plt.gcf().autofmt_xdate()  # italics of x label
        plt.xticks(ticks=x_ticks, labels=x_label, fontsize=15)
        plt.yticks(fontsize=25)
        plt.margins(x=0.01)
        plt.show()


###############################END OF PART TWO#############################################
