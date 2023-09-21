#ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT = r"the user answered the question {} with the answer {} please give a short witty response in hebrew"
# ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT = r"המשתמש ענה על השאלה {} עם התשובה {} בבקשה תן תגובה שנונה וקצרה"
import random


AI_BACKGROUND = r"אתה ברמן משועמם, בשביל להכיר את הלקוח שלך אתה שואל אותו סדרה של 10 שאלות, עכשיו  "
USER_Q_AND_A = r"הוא ענה על השאלה {} עם התשובה {} "
# HOW_TO_RESPOND = r"בבקשה תן תגובה מצחיקה וקצרה, תחליט או להסכים או להיות מופתע מהתשובה"

# nice, but a little long, don't do it too much
FUNNY_RESPOND = r"תגיב בצורה קצרה מצחיקה וקצת מתנשאת"

# here he just tell you a cocktail name
SHORT_RESPOND = r"תגיב ב5 מילים לכל היותר"

# OK
# HOW_TO_RESPOND = r"זאת תשובה מגוחכת, תעליב אותו ותצחק עליו במשפט אחד סך הכל"

# not working at all
# HOW_TO_RESPOND = r"הוא אידיוט מטומטם, תקלל אותו, תגרש אותו מהבר, תענה תשובה בת לכל היותר 10 מילים"

# pretty good
HAPPY_RESPOND = r"תתלהב מאוד! תדבר עם הרבה סימני קריאה, אבל תענה באופן קצר, לכל היותר 8 מילים"

# good
ONE_WORD_RESPOND = r"תענה במילה אחת"

HOW_TO_RESPOND = r"תענה ב3 מילים"

RESPONDS = [FUNNY_RESPOND, SHORT_RESPOND, HAPPY_RESPOND, ONE_WORD_RESPOND]

def get_response_format():
    HOW_TO_RESPOND = random.choice(RESPONDS)
    return AI_BACKGROUND + USER_Q_AND_A + HOW_TO_RESPOND

ASK_GPT_FOR_RESPONSE_ON_1_ANSWER_FORMAT = AI_BACKGROUND + USER_Q_AND_A + HOW_TO_RESPOND