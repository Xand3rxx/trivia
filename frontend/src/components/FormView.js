import React, { Component } from "react";
import $ from "jquery";

import "../stylesheets/FormView.css";

class FormView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {},
    };
  }

  componentDidMount() {
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories });
      },
      error: (error) => {
        alert("Unable to load categories. Please try your request again");
      },
    });
  }

  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: "/questions", //TODO: update request URL
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        alert(result.message);
        document.getElementById("add-question-form").reset();
      },
      error: (error) => {
        alert("Unable to add question. Please try your request again");
      },
    });
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    return (
      <div class="form-wrapper">
        <div id="add-form">
          <h2>Add a New Trivia Question</h2>
          <form
            className="form-view"
            id="add-question-form"
            onSubmit={this.submitQuestion}
          >
            <div class="card-input">
              <label class="card-input__label">Question</label>
              <input
                class="card-input__input"
                type="text"
                name="question"
                onChange={this.handleChange}
              />
            </div>

            <div class="card-input">
              <label class="card-input__label">Answer</label>
              <input
                class="card-input__input"
                type="text"
                name="answer"
                onChange={this.handleChange}
              />
            </div>

            <div class="card-input">
              <label class="card-input__label">Difficulty</label>
              <select
                class="card-input__input"
                name="difficulty"
                onChange={this.handleChange}
              >
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
              </select>
            </div>

            <div class="card-input">

            <label class="card-input__label">
              Category
              </label>
              <select class="card-input__input" name="category" onChange={this.handleChange}>
                {Object.keys(this.state.categories).map((id) => {
                  return (
                    <option key={id} value={id}>
                      {this.state.categories[id]}
                    </option>
                  );
                })}
              </select>
            </div>
            
            <input type="submit" className="card-form__button" value="Submit" />
          </form>
        </div>
      </div>
    );
  }
}

export default FormView;
