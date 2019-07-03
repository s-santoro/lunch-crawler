class Configurations:

    configs = [
        #
        # Configurations for production pipeline
        #
        {#
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
            "textBeverageTagger": False
        }
    ]