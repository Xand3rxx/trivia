import React, { Component } from "react";
import "../stylesheets/Question.css";

class Question extends Component {
  constructor(props) {
    super(props);
    this.state = {
      visibleAnswer: false,
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  render() {
    const { id, question, answer, category, difficulty } = this.props;
    return (
      <div className="Question-holder" id={`remove-${id}`}>
        <div className="Question">{question}
        <hr />
        </div>
        <div className="Question-status">
          <img className="category" src={`${(category || 'science').toLowerCase()}.svg`} alt={`${category}`} />
          <div className="difficulty">Difficulty: {difficulty}</div>
          <img
            src="delete.png"
            alt={`delete ${category}`}
            className="delete"
            onClick={() => this.props.questionAction("DELETE")}
          />
        </div>
        <div
          className="show-answer button"
          onClick={() => this.flipVisibility()}
        >
          {this.state.visibleAnswer ? "Hide" : "Show"} Answer
        </div>
        <div className="answer-holder">
          <span
            style={{
              visibility: this.state.visibleAnswer ? "visible" : "hidden",
            }}
          >
            Answer: {answer}
          </span>
        </div>
      </div>
    );
  }
}

export default Question;
