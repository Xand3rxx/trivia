import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv

dotenv_path = os.path.abspath(os.path.dirname(__file__))

# Get environment variables from .env.
load_dotenv(dotenv_path+'/.env')

DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.environ.get('DATABASE_HOST')  # eg localhost:5433
TEST_DATABASE_NAME = os.getenv('TEST_DATABASE_NAME')
if not DATABASE_PASSWORD:
    raise ValueError("No DATABASE_PASSWORD set for Flask application")



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, TEST_DATABASE_NAME
        )

        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "What is the largest organ in the human body?",
            "answer": "Skin", 
            "category": 1,
            "difficulty": 3
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_if_questions_endpoint_exists(self):
        """Test _____________ """
        res = self.client().get('/questions')

        self.assertEqual(res.status_code, 200)

    # A test to get paginated questions
    def test_get_paginated_questions(self):
        """Test _____________ """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_to_return_404_for_invalid_page_range_questions(self):
        """Test _____________ """
        res = self.client().get('/questions/page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")
    
    def test_return_404_if_question_does_not_exist_before_deleting(self):
        """Test _____________ """
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_can_create_a_new_question(self):
        """Test _____________ """
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question was successfully created.')

    def test_return_405_if_question_creation_method_is_not_allowed(self):
        """Test _____________ """
        res = self.client().post('/questions/100', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "method not allowed")
    
    def test_get_question_search_with_results(self):
        """Test _____________ """
        res = self.client().get('/questions', json={"searchTerm": "Heaviest"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_get_question_search_without_results(self):
        """Test _____________ """
        res = self.client().get('/questions', json={"search": "Gibberish"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_if_categories_endpoint_exists(self):
        """Test _____________ """
        res = self.client().get('/categories')

        self.assertEqual(res.status_code, 200)

    def test_get_categories(self):
        """Test _____________ """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_category_questions(self):
        """Test _____________ """
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 'Science')

    def test_to_return_404_for_invalid_question_range(self):
        """Test _____________ """
        res = self.client().get('/categories/13/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
