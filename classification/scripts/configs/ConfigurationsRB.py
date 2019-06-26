# Configuration-File Class
# Class consisting of list for different configs

class Configurations:

    configs = [
        #
        # Configurations for Rulebased Pipeline
        #
        #### Classifier = Pricedetector ####
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
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": True,
            "priceLimit": 1,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 3,
            "negLimit": 15, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0
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
            "textBeverageTagger": True,
            "textRemoveStopWords": True,

            # title preprocessing
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": True,
            "priceLimit": 2,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 3,
            "negLimit": 15, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0
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
            "textBeverageTagger": True,
            "textRemoveStopWords": True,

            # title preprocessing
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": True,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 3,
            "negLimit": 15, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0
        },
        #### Classifier = MenuInTitle ####
        {#3
            # text preprocessing
            "textToLowerCase": False,
            "textReplaceUmlaut": False,
            "textPriceTagger": False,
            "textRemoveSpecialCharacters": False,
            "textRemoveSingleCharacters": False,
            "textRemoveMultiSpaces": False,
            "textStemText": False,
            "textBeverageTagger": False,
            "textRemoveStopWords": False,

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
            "priceLimit": 1,

            # Classify with MenuInTitle
            "classifyMenuInTitle": True,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 3,
            "negLimit": 15, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0
        },
        #### Classifier = MenuPriceCombined ####
        {#4
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
            "priceLimit": 1,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": True,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 3,
            "negLimit": 15, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0
        },
        {#5
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
            "posLimit": 3,
            "negLimit": 15, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0
        },
        {#6
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
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": True,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 3,
            "negLimit": 15, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0    
        },
        #### Classifier = Black / Whitelisting ####
        {#7
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
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": True,
            "posLimit": 1,
            "negLimit": 5, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0    
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
            "textBeverageTagger": True,
            "textRemoveStopWords": True,

            # title preprocessing
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": True,
            "posLimit": 2,
            "negLimit": 10, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0    
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
            "textBeverageTagger": True,
            "textRemoveStopWords": True,

            # title preprocessing
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": True,
            "posLimit": 3,
            "negLimit": 15, 

            # Classify with Bag of Words
            "classifyBagOfWords": False,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0    
        },
        #### Classifier = Bag of Words ####
        {#10
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
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 1,
            "negLimit": 5, 

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 0    
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
            "textBeverageTagger": True,
            "textRemoveStopWords": True,

            # title preprocessing
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 1,
            "negLimit": 5, 

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 100,
            "decisionLimit": 0    
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
            "textBeverageTagger": True,
            "textRemoveStopWords": True,

            # title preprocessing
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 1,
            "negLimit": 5, 

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 150,
            "decisionLimit": 0    
        },
        {#13
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
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 1,
            "negLimit": 5, 

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 200,
            "decisionLimit": 0    
        },
        {#14
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
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 1,
            "negLimit": 5, 

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 50,
            "decisionLimit": 5    
        },
        {#15
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
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 1,
            "negLimit": 5, 

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 100,
            "decisionLimit": 5    
        },
        {#16
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
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 1,
            "negLimit": 5, 

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 150,
            "decisionLimit": 5    
        },
        {#17
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
            "titleToLowerCase": False,
            "titleReplaceUmlaut": False,
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": False,
            "titleRemoveSingleCharacters": False,
            "titleRemoveMultiSpaces": False,
            "titleStemText": False,
            "titleRemoveStopWords": False,

            # Classify with Pricedetector
            "classifyPricedetector": False,
            "priceLimit": 3,

            # Classify with MenuInTitle
            "classifyMenuInTitle": False,

            # Classify with MenuPriceCombined
            "classifyPriceMenuCombined": False,

            # Classify with Black / Whitelisting
            "classifyListing": False,
            "posLimit": 1,
            "negLimit": 5, 

            # Classify with Bag of Words
            "classifyBagOfWords": True,
            "useText": True,     # If False, use Title
            "testSizeSplit": 0.3,
            "numberOfFeatures": 200,
            "decisionLimit": 5   
        }
    ]
