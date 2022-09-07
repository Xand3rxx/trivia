import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import desc, asc
import sys
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # Method to return paginated question results based on users requests
    def paginate_questions(request, model):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        formatted_questions = [question.format() for question in model]
        return formatted_questions[int(start):int(start + QUESTIONS_PER_PAGE)]

    # Method to return all questions from the `questions` table
    def total_questions():
        return len(Question.query.all())

    # Method to return all categories from the `categories` table
    def get_categories():
        # return [category.format() for category in Category.query.order_by(asc(Category.type)).all()]
        return {category.id: category.type for category in Category.query.order_by(asc(Category.type)).all()}

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    def categories():
        categories = get_categories()

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories,
            'total_categories': len(categories),
        })

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions', methods=['GET'])
    def questions():
        model = Question.query.order_by(desc(Question.id)).all()
        questions = paginate_questions(request, model)

        if len(model) == 0:
            abort(404)

        for question in model:
            category = Category.query.filter(
                Category.id == question.id).first()

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': total_questions(),
            'categories': get_categories(),
            'current_category': category.type
        })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                }
            )
        except:
            abort(422)

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.

  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        question = body.get("question", None)
        answer = body.get("answer", None)
        category = body.get("category", None)
        difficulty = body.get("difficulty", None)
        search_term = body.get('searchTerm', None)

        try:
            if search_term:
                # if search term is emoty return all questions
                if search_term == '':
                    model = Question.query.all()
                else:
                    model = Question.query.filter(
                        Question.question.ilike(f'%{search_term}%')).all()

                questions = paginate_questions(request, model)

                if search_term == None:
                    abort(404)

                return jsonify({
                    "success": True,
                    "questions": questions,
                    "total_questions": len(model),
                })
            else:
                if question == '' or answer == '' or category == '' or difficulty == '':
                    abort(422)

                question = Question(question=question, answer=answer,
                                    category=category, difficulty=difficulty)
                question.insert()

                return jsonify(
                    {
                        "success": True,
                        "message": 'Question was successfully created.',
                    }
                )
        except:
            question.rollback()
            print(sys.exc_info())
            abort(422)

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):

        try:
            category = Category.query.filter(
                Category.id == category_id).one_or_none()

            if category is None:
                abort(404)

            model = Question.query.filter(
                Question.category == category_id).all()
            questions = paginate_questions(request, model)

            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": len(questions),
                "current_category": category.type
            })
        except:
            abort(404)
    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            category_id = quiz_category['id']
            previous_questions_size = len(previous_questions)
            print(category_id)

            # If ALL category was selected and previous questions array is empty
            if category_id == 0 & previous_questions_size == 0:
                questions = Question.query.order_by(desc(Question.id)).all()

            # If ALL category was selected and previous questions array is not empty
            elif category_id == 0 & previous_questions_size > 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions),
                                                  Question.category == category_id).all()

            # Initialize question variable to None
            question = None
            if (questions):
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': question.format()
            })
        except:
            abort(422)

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"success": False, "error": 405, "message": "method not allowed"}), 405

    return app
