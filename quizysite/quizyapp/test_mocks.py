import responses, json
raw_question_list = [
    {
        "category": "General Knowledge",
        "type": "boolean",
        "difficulty": "easy",
        "question": "The Great Wall of China is visible from the moon.",
        "correct_answer": "False",
        "incorrect_answers": [
            "True"
        ]
    },
    {
        "category": "General Knowledge",
        "type": "boolean",
        "difficulty": "easy",
        "question": "A scientific study on peanuts in bars found traces of over 100 unique specimens of urine.",
        "correct_answer": "False",
        "incorrect_answers": [
            "True"
        ]
    },
    {
        "category": "General Knowledge",
        "type": "multiple",
        "difficulty": "easy",
        "question": "Which country, not including Japan, has the most people of japanese decent?",
        "correct_answer": "Brazil",
        "incorrect_answers": [
            "China",
            "South Korea",
            "United States of America"
        ]
    }
]


mock_amount_2={
'method'         : responses.GET,
'url'            : 'https://opentdb.com/api.php?amount=2&category=9&difficulty=easy',
'body'           : json.dumps({"response_code":0,"results":raw_question_list[:1]}),
'status'         : 200,
'content_type'   : 'application/json',
}

mock_default={
'method'         : responses.GET,
'url'            : 'https://opentdb.com/api.php?amount=3&category=9&difficulty=easy',
'body'           : json.dumps({"response_code":0,"results":raw_question_list}),
'status'         : 200,
'content_type'   : 'application/json',
}