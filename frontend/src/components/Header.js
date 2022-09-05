import React, { Component } from 'react';
// import logo from '../logo.svg';
import '../stylesheets/Header.css';

class Header extends Component {

  navTo(uri){
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      // <div className="App-header">
      //   <h1 onClick={() => {this.navTo('')}}>Udacity Trivia</h1>
      //   <h2 onClick={() => {this.navTo('')}}>List</h2>
      //   <h2 onClick={() => {this.navTo('/add')}}>Add</h2>
      //   <h2 onClick={() => {this.navTo('/play')}}>Play</h2>

      <section class="navigation">
        <div class="nav-container">
          <div class="brand">
            <a href="/">Udacity Trivia</a>
          </div>
          <nav>
            <div class="nav-mobile"><a id="nav-toggle" href="#!"><span></span></a></div>
            <ul class="nav-list">
              <li>
                <a href="#!" onClick={() => {this.navTo('')}}>List</a>
              </li>
              <li>
                <a href="#!" onClick={() => {this.navTo('/add')}}>Add</a>
              </li>
              <li>
                <a href="#!" onClick={() => {this.navTo('/play')}}>Play</a>
              </li>
            </ul>
          </nav>
        </div>
      </section>
      // </div>
    );
  }
}

export default Header;
