# Configuration-File Class
# Class consisting of list for different configs

class Configurations:

    configs = [
        #
        # Configurations for Machine-Learning Pipeline
        #
        {#
            # text preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": True,
            "textPriceTagger": True,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            "textStemText": True,
            "textRemoveStopWords": True,

            # title preprocessing
            "titleToLowerCase": True,
            "titleReplaceUmlaut": True,
            "titlePriceTagger": True,
            "titleRemoveSpecialCharacters": True,
            "titleRemoveSingleCharacters": True,
            "titleRemoveMultiSpaces": True,
            "titleStemText": True,
            "titleRemoveStopWords": True,

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
            #"maxFeatures": 50,
            "maxFeatures": 200,

            # tf-idf
            "use_tfidf": True,
            "ngram_range": (1, 2),
            "min_df": 2,
            "max_df": .95,

            # dimension reduction (truncated svd)
            "use_dimension_reduction": True,
            "n_components": 100,
            "n_iter": 10
        },
        {#
                   # text preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": True,
            "textPriceTagger": True,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            "textStemText": True,
            "textRemoveStopWords": True,

            # title preprocessing
            "titleToLowerCase": True,
            "titleReplaceUmlaut": True,
            "titlePriceTagger": True,
            "titleRemoveSpecialCharacters": True,
            "titleRemoveSingleCharacters": True,
            "titleRemoveMultiSpaces": True,
            "titleStemText": True,
            "titleRemoveStopWords": True,

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
            #"maxFeatures": 50,
            "maxFeatures": 200,

            # tf-idf
            "use_tfidf": False,
            "ngram_range": (1, 2),
            "min_df": 2,
            "max_df": .95,

            # dimension reduction (truncated svd)
            "use_dimension_reduction": False,
            "n_components": 100,
            "n_iter": 10
        },
        {#
            # text preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": True,
            "textPriceTagger": True,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            "textStemText": True,
            "textRemoveStopWords": True,

            # title preprocessing
            "titleToLowerCase": True,
            "titleReplaceUmlaut": True,
            "titlePriceTagger": True,
            "titleRemoveSpecialCharacters": True,
            "titleRemoveSingleCharacters": True,
            "titleRemoveMultiSpaces": True,
            "titleStemText": True,
            "titleRemoveStopWords": True,

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
            #"maxFeatures": 50,
            "maxFeatures": 200,

            # tf-idf
            "use_tfidf": False,
            "ngram_range": (1, 2),
            "min_df": 2,
            "max_df": .95,

            # dimension reduction (truncated svd)
            "use_dimension_reduction": True,
            "n_components": 100,
            "n_iter": 10
        },
        {#
            # text preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": True,
            "textPriceTagger": True,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            "textStemText": True,
            "textRemoveStopWords": True,

            # title preprocessing
            "titleToLowerCase": True,
            "titleReplaceUmlaut": True,
            "titlePriceTagger": True,
            "titleRemoveSpecialCharacters": True,
            "titleRemoveSingleCharacters": True,
            "titleRemoveMultiSpaces": True,
            "titleStemText": True,
            "titleRemoveStopWords": True,

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
            #"maxFeatures": 50,
            "maxFeatures": 200,

            # tf-idf
            "use_tfidf": True,
            "ngram_range": (1, 2),
            "min_df": 2,
            "max_df": .95,

            # dimension reduction (truncated svd)
            "use_dimension_reduction": False,
            "n_components": 100,
            "n_iter": 10
        }
    ]