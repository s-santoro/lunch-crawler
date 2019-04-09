# Configuration-File Class
# Class consisting of list for different configs

class Configurations:

    configs = [
        {
            # text preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": False,
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

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": False,     # If False, use Title
            "testSizeSplit": 0.7,
            "numberOfFeatures": 3,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": False
        },
        {
            # text preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": False,
            "textPriceTagger": False,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            "textStemText": True,
            "textRemoveStopWords": True,

            # title preprocessing
            "titleToLowerCase": True,
            "titleReplaceUmlaut": True,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": True,
            "titleRemoveSingleCharacters": True,
            "titleRemoveMultiSpaces": True,
            "titleStemText": True,
            "titleRemoveStopWords": True,

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.5,
            "numberOfFeatures": 50,
            "decisionLimit": 0,


            # Classify with combined Rules
            "classifyCombinedRules": True
        }
    ]
