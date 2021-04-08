import React, {useEffect, useState} from 'react';
import LogRocket from 'logrocket';
import 'bootstrap/dist/css/bootstrap.min.css';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";
import Header from "./components/layout/Header";
import {InputDataView} from "./components/InputDataView";
import {PredictionView} from "./components/PredictionView";
import {AboutView} from "./components/AboutView"
import './App.css'

const App = () => {
    LogRocket.init('bc26dt/ml-starter-frontend');


    return (
        <Router>
        <div className="App" >
            <Header/>
        </div>
        <div className="AppBody">
        <Switch>
            <Route path="/prediction">
                <PredictionView />
            </Route>
            <Route path="/about">
                <AboutView />
            </Route>
            <Route path="/">
                <InputDataView />
            </Route>
        </Switch>
        </div>
        </Router>);
}

export default App;
