class Configurations:

    configs = [
        #
        # Configurations for Machine-Learning Pipeline
        #
        {# tfidf best precision
            # basic preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": True,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            # advanced preprocessing
            "textPriceTagger": False,
            "textStemText": False,
            "textRemoveStopWords": False,
            "textBeverageTagger": False,

            # Parameters for Data-Visualization
            "n_most_freq_words": 20,
            "n_most_freq_words_per_class": 15,
            "n_most_freq_bigrams_per_class": 15,

            # train test split
            "test_size": .3,
            "shuffle": True,
            #"stratify": y,
            "random_state": 3,

            # bag of words
            "use_BoW": False,
            "binary": False,
            "maxFeatures": None,

            # tf-idf
            "use_tfidf": True,
            "ngram_range": (1, 2),
            "min_df": 2,
            "max_df": .95,
            "maxFeaturesTFIDF": None,

            # dimension reduction (truncated svd)
            "use_dimension_reduction": True,
            "n_components": 325,
            "n_iter": 10,

            # hyperparameter
            "params": {
                "max_depth" : [10, 50, 100, None],
                "min_samples_split" : [2, 5, 10],
                "min_samples_leaf" : [1, 2, 5],
                "bootstrap" : [True, False],
                "max_features" : ['auto', 'log2', None],
                "random_state" : [3]
            }
        }
    ]