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
import './App.css'
import {useSelector} from "react-redux";

const App = () => {
    LogRocket.init('bc26dt/ml-starter-frontend');

    const configuration = useSelector(state => state.configuration)
    const {applicationName} = configuration


    return (
        <Router>
        <div className="App" >
            <Header/>
        </div>
        <div className="AppBody">
        <h1 className="ApplicationName">{applicationName}</h1>
        <Switch>
            <Route path="/prediction">
                <PredictionView />
            </Route>
            <Route path="/">
                <InputDataView />
            </Route>
        </Switch>
        </div>
        </Router>);
}

export default App;
