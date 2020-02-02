import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Widget, addResponseMessage, toggleMsgLoader, setQuickButtons, addUserMessage, toggleWidget } from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';

interface IProps {
}

interface IState {
  fSM?: boolean;
  autofocus: boolean;
}

class App extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);
    this.state = {fSM: false, autofocus: true};
  }

  componentDidMount() {
    toggleWidget();
    setQuickButtons([ { label: 'Begrüßen', value: 'Hallo ExSyNL!' }, { label: 'Orange', value: 'orange' }, { label: 'Pear', value: 'pear' }, { label: 'Banana', value: 'banana' } ]);
    this.setState({fSM: true}, () => {this.setState({autofocus: false})});
  }

  handleNewUserMessage = (newMessage: String) => {
    toggleMsgLoader();
    const data = { newInput: newMessage };
    window.fetch('/talk/0', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then((response) => response.json())
    .then((data) => {
      addResponseMessage(data['answer']);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
    // Now send the message throught the backend API
    toggleMsgLoader();
  }

  handleQuickButtonClicked = (e: any) => {
    addUserMessage(e);
    toggleMsgLoader();
    const data = { newInput: e };
    window.fetch('/talk/0', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then((response) => response.json())
    .then((data) => {
      addResponseMessage(data['answer']);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
    // Now send the message throught the backend API
    toggleMsgLoader();
    setQuickButtons([]);
  }

  render() {
    return (
      <div className="App">
        <Widget
          handleNewUserMessage={this.handleNewUserMessage}
          handleQuickButtonClicked={this.handleQuickButtonClicked}
          title="ExSyNL"
          subtitle=""
          senderPlaceHolder="Tippe etwas ein"
          fullScreenMode={this.state.fSM}
          showCloseButton={false}
          autofocus={this.state.autofocus}
         />
      </div>
    );
  }
}

export default App;
