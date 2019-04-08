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
            "titlePriceTagger": False,
            "titleRemoveSpecialCharacters": True,
            "titleRemoveSingleCharacters": True,
            "titleRemoveMultiSpaces": True,
            "titleStemText": True,
            "titleRemoveStopWords": True,

            #
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
        }
    ]


'''
TP: 296 FP: 0
FN: 161 TN: 566
              precision    recall  f1-score   support

           0       0.78      1.00      0.88       566
           1       1.00      0.65      0.79       457

   micro avg       0.84      0.84      0.84      1023
   macro avg       0.89      0.82      0.83      1023
weighted avg       0.88      0.84      0.84      1023

'''
