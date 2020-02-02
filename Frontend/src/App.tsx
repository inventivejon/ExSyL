import 'typeface-roboto';
import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Widget, addResponseMessage, toggleMsgLoader, setQuickButtons, addUserMessage, toggleWidget } from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
import AppBar from '@material-ui/core/AppBar';
import CssBaseline from '@material-ui/core/CssBaseline';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid'
import Button from '@material-ui/core/Button'

interface IProps {
}

interface IState {
  fSM?: boolean;
  autofocus: boolean;
  displayMode: String;
}

class App extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);
    this.state = {fSM: false, autofocus: true, displayMode: 'chat'};
  }

  componentDidMount() {
    toggleWidget();
    setQuickButtons([ { label: 'Begrüßen', value: 'Hallo ExSyNL!' } ]);
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
      <React.Fragment>
      <CssBaseline />
      <AppBar position="relative">
        <Toolbar>
        <Grid
          container
          direction="row"
          justify="space-between"
          alignItems="center"
        >
          <Typography variant="h6" color="inherit" noWrap>Du chattest mit ExSyNL
          </Typography>
            <Grid
            container
            direction="row"
            justify="flex-end"
            alignItems="center"
            >
            {this.state.displayMode!=='chat' && (
              <Button variant="contained" color="primary" disableElevation onClick={() => { this.setState({displayMode: 'chat'})}}>
              Zurück zum Chat
              </Button>
            )}
            <Button variant="contained" color="primary" disableElevation onClick={() => { this.setState({displayMode: 'GitHub'})}}>
            GitHub
            </Button>
            <Button variant="contained" color="primary" disableElevation onClick={() => { this.setState({displayMode: 'Datenschutz'})}}>
            Datenschutz
            </Button>
            <Button variant="contained" color="primary" disableElevation onClick={() => { this.setState({displayMode: 'Impressum'})}}>
            Impressum
            </Button>
            </Grid>
          </Grid>
        </Toolbar>
      </AppBar>
      {this.state.displayMode==='chat' && (
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
      )}
      {this.state.displayMode==='Impressum' && (
        <div className="rcw-widget-container rcw-full-screen rcw-opened">
        <Grid className="rcw-widget-container rcw-full-screen rcw-opened"
        container
        direction="column"
        justify="center"
        alignItems="center"
        >
          <Typography variant="h6" color="inherit" noWrap>
            Impressum
          </Typography>
          <Typography variant="h6" color="inherit" noWrap>
            Hier sollte Dein Impressum stehen
          </Typography>
        </Grid>
      </div>
      )}
      {this.state.displayMode==='Datenschutz' && (
        <div className="rcw-widget-container rcw-full-screen rcw-opened">
        <Grid className="rcw-widget-container rcw-full-screen rcw-opened"
        container
        direction="column"
        justify="center"
        alignItems="center"
        >
          <Typography variant="h6" color="inherit" noWrap>
            Datenschutz
          </Typography>
          <Typography variant="h6" color="inherit" noWrap>
            Hier sollte Dein Datenschutz stehen
          </Typography>
        </Grid>
      </div>
      )}
      {this.state.displayMode==='GitHub' && (
        <div className="rcw-widget-container rcw-full-screen rcw-opened">
          <Grid className="rcw-widget-container rcw-full-screen rcw-opened"
          container
          direction="column"
          justify="center"
          alignItems="center"
          >
            <Typography variant="h6" color="inherit" noWrap>
              Besuche uns auf GitHub:
            </Typography>
            <Button variant="outlined" color="primary" href="https://github.com/inventivejon/ExSyNL">
            ExSyNL on GitHub
            </Button>
          </Grid>
        </div>
      )}
      </React.Fragment>
    );
  }
}

export default App;
