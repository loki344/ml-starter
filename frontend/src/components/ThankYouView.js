import React from "react";
import {useHistory} from "react-router-dom";


export const ThankYouView = () => {

    let history = useHistory()

    const handleNewPrediction = () => {
        history.push('/')
    }

    const handleKnowMore = () => {
        history.push('/about')
    }

    return(

        <div>
            <h3 className='PredictionTitle'>Thank you for your feedback!</h3>
            <br/>
            <br/>
            <button onClick={handleNewPrediction} className="button">
                Make another prediction
                <div className="button__horizontal"/>
                <div className="button__vertical"/>
            </button>
            <br/>
            <br/>

            <button onClick={handleKnowMore} className="button"  >
                I want to know more about this project
                <div className="button__horizontal"/>
                <div className="button__vertical"/>
            </button>


        </div>
    )


}