import React from "react";
import {useHistory} from "react-router-dom";

export const NextPredictionButton = () => {


    let history = useHistory()
    const handleNewPrediction = () => {
        history.push('/')
    }


    return(
        <button onClick={handleNewPrediction} className="button">
            Make another prediction
            <div className="button__horizontal"/>
            <div className="button__vertical"/>
        </button>

        )






}