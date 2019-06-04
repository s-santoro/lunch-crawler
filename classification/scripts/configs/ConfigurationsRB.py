# Configuration-File Class
# Class consisting of list for different configs

class Configurations:

    configs = [
        #
        # Configurations for Rulebased Pipeline
        #
        #### Classifier = Bag of Words Method ####
        {#0
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

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": False,
            "menuInTitle": False,
            "priceEntity": True,
            "whiteList": True,
            "keyAmount": 1,
            "keyValTreshold": 1,   
        },
        {#1
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

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,  # If False, use Title
            "testSizeSplit": 0.5,
            "numberOfFeatures": 50,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": False,
            "menuInTitle": False,
            "priceEntity": True,
            "whiteList": True,
            "keyAmount": 1,
            "keyValTreshold": 1,  
        },
        {#2
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

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,  # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 100,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": False,
            "menuInTitle": False,
            "priceEntity": True,
            "whiteList": True,
            "keyAmount": 1,
            "keyValTreshold": 1, 
        },
        {#3
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

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,  # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 185,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": False,
            "menuInTitle": False,
            "priceEntity": True,
            "whiteList": True,
            "keyAmount": 1,
            "keyValTreshold": 1,
        },
        {#4
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

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,  # If False, use Title
            "testSizeSplit": 0.5,
            "numberOfFeatures": 200,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": False,
            "menuInTitle": False,
            "priceEntity": True,
            "whiteList": True,
            "keyAmount": 1,
            "keyValTreshold": 1,  
        },
        {#5
            #No Preprocessing
            # text preprocessing
            "textToLowerCase": False,
            "textReplaceUmlaut": False,
            "textPriceTagger": False,
            "textRemoveSpecialCharacters": False,
            "textRemoveSingleCharacters": False,
            "textRemoveMultiSpaces": False,
            "textStemText": False,
            "textRemoveStopWords": False,

            # title preprocessing
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,  # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 185,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": False,
            "menuInTitle": False,
            "priceEntity": True,
            "whiteList": True,
            "keyAmount": 1,
            "keyValTreshold": 1,
        },
        #### Classifier = Combined Rules Method ####
        {#6
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

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.5,
            "numberOfFeatures": 50,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": True,
            "menuInTitle": True,
            "priceEntity": False,
            "whiteList": False,
            "keyAmount": 1,
            "keyValTreshold": 1,
        },
		{#7
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

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.5,
            "numberOfFeatures": 50,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": True,
            "menuInTitle": False,
            "priceEntity": True,
            "whiteList": False,
            "keyAmount": 1,
            "keyValTreshold": 1,
        },
		{#8
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

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.5,
            "numberOfFeatures": 50,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": True,
            "menuInTitle": False,
            "priceEntity": False,
            "whiteList": True,
            "keyAmount": 1,
            "keyValTreshold": 1,
        },
		{#9
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

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.5,
            "numberOfFeatures": 50,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": True,
            "menuInTitle": True,
            "priceEntity": True,
            "whiteList": False,
            "keyAmount": 1,
            "keyValTreshold": 1,
        },
		{#10
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

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.5,
            "numberOfFeatures": 50,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": True,
            "menuInTitle": True,
            "priceEntity": False,
            "whiteList": True,
            "keyAmount": 1,
            "keyValTreshold": 1, 
        },
		{#11
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

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.5,
            "numberOfFeatures": 50,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": True,
            "menuInTitle": False,
            "priceEntity": True,
            "whiteList": True,
            "keyAmount": 1,
            "keyValTreshold": 1,
        },
		{#12
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

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.5,
            "numberOfFeatures": 50,
            "decisionLimit": 0,

            # Classify with combined Rules
            "classifyCombinedRules": True,
            "menuInTitle": True,
            "priceEntity": True,
            "whiteList": True,
            "keyAmount": 1,
            "keyValTreshold": 1,
        }
    ]
