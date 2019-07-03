# Configuration-File Class
# Class consisting of list for different configs

class Configurations:

    configs = [
        {#0
            # text preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": True,
            "textPriceTagger": True,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            "textStemText": True,
            "textBeverageTagger": True,
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

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 2,

            # Classify with MenuInTitle
            "classifyMenuInTitle": True,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 20,
            "negLimit": 20, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "dynamic": False,
            "testSizeSplit": 0.3,
            "numberOfFeatures": 200,
            "decisionLimit": -5
        },
        {#0
            # text preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": True,
            "textPriceTagger": True,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            "textStemText": True,
            "textBeverageTagger": True,
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

            # Classify with Pricedetector
            "classifyPricedetector": True,
            "priceLimit": 2,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 20,
            "negLimit": 20, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "dynamic": False,
            "testSizeSplit": 0.3,
            "numberOfFeatures": 200,
            "decisionLimit": -5
        },
        {#0
            # text preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": True,
            "textPriceTagger": True,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            "textStemText": True,
            "textBeverageTagger": True,
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

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 2,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": True,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 20,
            "negLimit": 20, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "dynamic": False,
            "testSizeSplit": 0.3,
            "numberOfFeatures": 200,
            "decisionLimit": -5
        },
        {#0
            # text preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": True,
            "textPriceTagger": True,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            "textStemText": True,
            "textBeverageTagger": True,
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

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 2,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": True,
            "posLimit": 7,
            "negLimit": 20, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "dynamic": False,
            "testSizeSplit": 0.3,
            "numberOfFeatures": 200,
            "decisionLimit": -5
        },
        {#0
            # text preprocessing
            "textToLowerCase": True,
            "textReplaceUmlaut": True,
            "textPriceTagger": True,
            "textRemoveSpecialCharacters": True,
            "textRemoveSingleCharacters": True,
            "textRemoveMultiSpaces": True,
            "textStemText": True,
            "textBeverageTagger": True,
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

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 2,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 20,
            "negLimit": 20, 

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,     # If False, use Title
            "dynamic": False,
            "testSizeSplit": 0.3,
            "numberOfFeatures": 400,
            "decisionLimit": -5
        }
    ]
