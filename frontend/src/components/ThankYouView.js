import React from "react";
import {useHistory} from "react-router-dom";
import {NextPredictionButton} from "./NextPredictionButton";


export const ThankYouView = () => {

    let history = useHistory()

    const handleKnowMore = () => {
        history.push('/about')
    }

    return(

        <div>
            <h3 className='PredictionTitle'>Thank you for your feedback!</h3>
            <NextPredictionButton/>

            <button onClick={handleKnowMore} className="button"  >
                I want to know more about this project
                <div className="button__horizontal"/>
                <div className="button__vertical"/>
            </button>


        </div>
    )


}