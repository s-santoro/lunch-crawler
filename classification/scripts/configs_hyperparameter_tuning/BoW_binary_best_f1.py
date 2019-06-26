class Configurations:

    configs = [
        #
        # Configurations for Machine-Learning Pipeline
        #
        {# bow binary best f1
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
            "use_BoW": True,
            "binary": True,
            "maxFeatures": None,

            # tf-idf
            "use_tfidf": False,
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
                "penalty" : [None, 'l2','l1', 'elasticnet'],
                "alpha" : [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0],
                "max_iter" : [5, 50, 100, 300, 500, 700, 1000, 2000, 5000],
                "tol" : [None, 5e-4, 1e-3, 2e-3, 5e-3],
                "eta0" : [0.1, 0.5, 0.7, 1., 1.2, 1.5],
                "early_stopping": [False, True],

                "random_state" : [3]
            }
        }
    ]