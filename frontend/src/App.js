import React, {useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {
    BrowserRouter as Router,
    Switch,
    Route,
} from "react-router-dom";
import Header from "./components/layout/Header";
import {MainView} from "./views/MainView";
import {AboutView} from "./views/AboutView"
import './styles/App.css'
import {useDispatch} from "react-redux";
import {getConfiguration} from "./actions/configurationActions";

const App = () => {

    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(getConfiguration())
    }, [dispatch])

    return (
        <Router>
            <div className="App">
                <Header/>
            </div>
            <div className="AppBody">
                <Switch>
                    <Route path="/about">
                        <AboutView/>
                    </Route>
                    <Route path="/">
                        <MainView/>
                    </Route>
                </Switch>
            </div>
        </Router>);
}

export default App;
