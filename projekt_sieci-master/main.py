from util import read_tweets, get_location_and_save, merge_jsons, list_nonassigned_locations, fix_nonassigned_locations, \
    categorization, json_to_csv, categorize_hashtags, create_graph, analyze_tweets, create_graph_optimized, \
    create_graph_for_province

# Tutaj trzeba zmienić
# START = 1
# END = 700159

if __name__ == "__main__":
    # merge_jsons()
    # fix_nonassigned_locations("tweets_woj_merged_onlyloc.json")
    # categorization("tweets_woj_merged_onlyloc_currentfix.json")
    # json_to_csv("tweets_categorized.json", "tweets_categorized.csv")
    # categorize_hashtags()
    # categorization()
    # create_graph(gexf_out="graph.gexf")
    create_graph_optimized(gexf_out="graph_optimized.gexf")
    # create_graph_for_province(province='dolnośląskie')
    # create_graph_for_province(province='kujawsko-pomorskie')
    # create_graph_for_province(province='lubelskie')
    # create_graph_for_province(province='lubuskie')
    # create_graph_for_province(province='łódzkie')
    # create_graph_for_province(province='małopolskie')
    # create_graph_for_province(province='mazowieckie')
    # create_graph_for_province(province='opolskie')
    # create_graph_for_province(province='podkarpackie')
    # create_graph_for_province(province='podlaskie')
    # create_graph_for_province(province='pomorskie')
    # create_graph_for_province(province='śląskie')
    # create_graph_for_province(province='świętokrzyskie')
    # create_graph_for_province(province='warmińsko-mazurskie')
    # create_graph_for_province(province='wielkopolskie')
    # create_graph_for_province(province='zachodniopomorskie')
    # analyze_tweets()

