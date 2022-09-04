# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter) and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

> Once you're ready, you can submit your project on the last page.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [./backend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. _./backend/flaskr/`__init__.py`_
2. _./backend/test_flaskr.py_

### Frontend

The [./frontend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. _./frontend/src/components/QuestionView.js_
2. _./frontend/src/components/FormView.js_
3. _./frontend/src/components/QuizView.js_

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [README within ./frontend for more details.](./frontend/README.md)

## Trivia Application API Documentation

`GET '/categories'`

- Fetches a dictionary of categories type in string
- Request Arguments: None
- Returns: An object of an array of categories type, a success boolean value, and total number of categories.

```json
{
  "categories": [
    "Art",
    "Entertainment",
    "Geography",
    "History",
    "Science",
    "Sports"
  ],
  "success": true,
  "total_categories": 6
}
```

---

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, array of categories type, total number of questions, and a success boolean value.

```json
{
  "categories": [
    "Art",
    "Entertainment",
    "Geography",
    "History",
    "Science",
    "Sports"
  ],
  "questions": [
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 23
}
```

---

`GET '/categories/${id}/questions'`

- Fetches questions for a category specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total number of questions, and current category string, and a success boolean value.

```json
{
  "current_category": "History",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled \"I Know Why the Caged Bird Sings?\""
    }
  ],
  "success": true,
  "total_questions": 4
}
```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: An object of the deleted id and a success boolean value.
```json
{
  "deleted": 23,
  "success": true
}

```
---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
  "previous_questions": [],
  "quiz_category": {
    "type": "Science",
    "id": "4"
  }
}
```

- Returns: An object of a random question of the selected quiz category and a success boolean value.

```json
{
  "question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled \"I Know Why the Caged Bird Sings?\""
  },
  "success": true
}
```

---

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: Does not return any new data

---

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "Heaviest"
}
```

- Returns: Any matching array of questions, total number of questions that met the search term and a success boolean value.

```json
{
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

## Examples of CURL Requests

```bash
curl http://127.0.0.1:5000/questions
```

```bash
curl -X DELETE http://127.0.0.1:5000/questions/3
```

```bash
curl -X POST -H "Content-Type: application/json" -d '{"question":"what is the largest organ in the body?", "answer":"Skin", "category":"5", "difficulty":"3"}' http://127.0.0.1:5000/questions
```
