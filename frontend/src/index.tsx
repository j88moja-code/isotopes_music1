import React from 'react';
import ReactDOM from 'react-dom/client';
import CssBaseline from '@mui/material/CssBaseline';
import App from './App';
import reportWebVitals from './reportWebVitals';
import axios from "axios";
import configureStore from "./redux/configureStore";
import {Provider} from "react-redux";
import {positions, Provider as AlertProvider} from 'react-alert';

axios.defaults.baseURL = 'http://localhost:8001/api';
// axios.defaults.headers.Authorization = `Bearer ${localStorage.getItem('token')}`;
axios.defaults.withCredentials = true;

const store = configureStore();

// const AlertTemplate = ({ style, options, message, close }) => (
//     <div style={style}>
//         {options.type === 'info' && '!'}
//         {options.type === 'success' && ':)'}
//         {options.type === 'error' && ':('}
//         {message}
//         <button onClick={close}>X</button>
//     </div>
// )
//
// //Alert option
// const alertOptions = {
//     timeout: 3000,
//     position: positions.TOP_CENTER
// }

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
      <Provider store={store}>
          <CssBaseline />
          <App />
      </Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
