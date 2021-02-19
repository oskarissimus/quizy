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

raw_question_list_art=[
    {
        "category": "Art",
        "type": "multiple",
        "difficulty": "easy",
        "question": "Who painted the Sistine Chapel?",
        "correct_answer": "Michelangelo",
        "incorrect_answers": [
            "Leonardo da Vinci",
            "Pablo Picasso",
            "Raphael"
        ]
    },
    {
        "category": "Art",
        "type": "multiple",
        "difficulty": "easy",
        "question": "Who painted The Starry Night?",
        "correct_answer": "Vincent van Gogh",
        "incorrect_answers": [
            "Pablo Picasso",
            "Leonardo da Vinci",
            "Michelangelo"
        ]
    },
    {
        "category": "Art",
        "type": "multiple",
        "difficulty": "easy",
        "question": "Which painting was not made by Vincent Van Gogh?",
        "correct_answer": "The Ninth Wave",
        "incorrect_answers": [
            "Caf&eacute; Terrace at Night",
            "Bedroom In Arles",
            "Starry Night"
        ]
    }
]

category_list={
    "trivia_categories": [
        {
            "id": 9,
            "name": "General Knowledge"
        },
        {
            "id": 10,
            "name": "Entertainment: Books"
        },
        {
            "id": 11,
            "name": "Entertainment: Film"
        },
        {
            "id": 12,
            "name": "Entertainment: Music"
        },
        {
            "id": 13,
            "name": "Entertainment: Musicals & Theatres"
        },
        {
            "id": 14,
            "name": "Entertainment: Television"
        },
        {
            "id": 15,
            "name": "Entertainment: Video Games"
        },
        {
            "id": 16,
            "name": "Entertainment: Board Games"
        },
        {
            "id": 17,
            "name": "Science & Nature"
        },
        {
            "id": 18,
            "name": "Science: Computers"
        },
        {
            "id": 19,
            "name": "Science: Mathematics"
        },
        {
            "id": 20,
            "name": "Mythology"
        },
        {
            "id": 21,
            "name": "Sports"
        },
        {
            "id": 22,
            "name": "Geography"
        },
        {
            "id": 23,
            "name": "History"
        },
        {
            "id": 24,
            "name": "Politics"
        },
        {
            "id": 25,
            "name": "Art"
        },
        {
            "id": 26,
            "name": "Celebrities"
        },
        {
            "id": 27,
            "name": "Animals"
        },
        {
            "id": 28,
            "name": "Vehicles"
        },
        {
            "id": 29,
            "name": "Entertainment: Comics"
        },
        {
            "id": 30,
            "name": "Science: Gadgets"
        },
        {
            "id": 31,
            "name": "Entertainment: Japanese Anime & Manga"
        },
        {
            "id": 32,
            "name": "Entertainment: Cartoon & Animations"
        }
    ]
}

mock_amount_2={
'method'         : responses.GET,
'url'            : 'https://opentdb.com/api.php?amount=2&category=9&difficulty=easy',
'body'           : json.dumps({"response_code":0,"results":raw_question_list[:2]}),
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

mock_category={
'method'         : responses.GET,
'url'            : 'https://opentdb.com/api_category.php',
'body'           : json.dumps(category_list),
'status'         : 200,
'content_type'   : 'application/json',
}

mock_art_category={
'method'         : responses.GET,
'url'            : 'https://opentdb.com/api.php?amount=3&category=25&difficulty=easy',
'body'           : json.dumps({"response_code":0,"results":raw_question_list_art}),
'status'         : 200,
'content_type'   : 'application/json',
}
