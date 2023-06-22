import React from 'react';
import logo from './logo.svg';
import {BrowserRouter, Route} from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/secure/Home";
import Profile from "./pages/secure/profile/Profile";
import Password from "./pages/secure/profile/Password";

function App() {
  return (
    <BrowserRouter>
        <Route path={'/'} exact component={Home} />
        <Route path={'/login'} component={Login} />
        <Route path={'/register'} component={Register} />
        <Route path={'/profile'} component={Profile} />
        <Route path={'/password'} component={Password} />
    </BrowserRouter>
  );
}

export default App;
