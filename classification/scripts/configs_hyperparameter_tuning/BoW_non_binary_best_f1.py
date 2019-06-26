class Configurations:

    configs = [
        #
        # Configurations for Machine-Learning Pipeline
        #
        {# bow non binary best f1
            # basic preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": True,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            # advanced preprocessing
            "textPriceTagger": True,
            "textStemText": True,
            "textRemoveStopWords": True,
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
            "use_BoW": True,
            "binary": False,
            "maxFeatures": None,

            # tf-idf
            "use_tfidf": False,
            "ngram_range": (1, 2),
            "min_df": 2,
            "max_df": .95,
            "maxFeaturesTFIDF": None,

            # dimension reduction (truncated svd)
            "use_dimension_reduction": True,
            "n_components": 100,
            "n_iter": 10,

            # hyperparameter
            "params": {
                "n_estimators" : [10, 20, 50, 70, 100, 150, 300, 500, 1000, 1200, 1500, 2000],
                "learning_rate" : [0.01, 0.02, 0.05, 0.07, 0.1, 0.2, 0.5, 0.7, 1., 1.2, 1.3, 1.5, 2.],
                "random_state" : [3]
            }
        }
    ]