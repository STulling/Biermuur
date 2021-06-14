import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { ThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';

const theme = createMuiTheme({
  palette: {
    type: "dark",
    primary: {
      contrastText: "rgba(0, 0, 0, 0.87)",
      dark: "rgb(100, 141, 174)",
      light: "rgb(166, 212, 250)",
      main: "#90caf9",
    },
    secondary: {
      contrastText: "rgba(0, 0, 0, 0.87)",
      dark: "rgb(170, 100, 123)",
      light: "rgb(246, 165, 192)",
      main: "#f48fb1",
    },
  }
});

ReactDOM.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
