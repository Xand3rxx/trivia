import React, { Component } from 'react'
import "../stylesheets/Search.css";

class Search extends Component {
  state = {
    query: '',
  }

  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch(this.state.query)
  }

  handleInputChange = () => {
    this.setState({
      query: this.search.value
    })
  }

  render() {
    return (
      <form onSubmit={this.getInfo}>
        <input
        className="card-input__input-2"
          placeholder="Search questions..."
          ref={input => this.search = input}
          onChange={this.handleInputChange}
        />
        <input type="submit" value="Submit" className="card-form__button-2"/>
      </form>
    )
  }
}

export default Search
