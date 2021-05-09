import React, {useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {patchRating} from "../actions/predictionActions";
import '../styles/CustomRadioButton.css'
import {PredictionItem} from "./PredictionItem";
import {SET_RATING} from "../constants/predictionConstants";

export const PredictionForm = () => {

    const predictionObject = useSelector(state => state.prediction)
    const {prediction, id, showSpinner, rating} = predictionObject

    const dispatch = useDispatch();

    function updateRating(input) {

        dispatch({type: SET_RATING, payload: input})

        if (rating === '') {
            return
        }
        dispatch(patchRating(id, rating))

    }

    const showPrediction = () => {
        return prediction.length > 0 && !showSpinner ? "" : "Hidden";
    }


    return (

        <div className={showPrediction()}>

            <h2 className="PredictionTitle">Prediction:</h2>
            <br/>

            <div style={{display: 'inline-grid', gridTemplateColumns: '20% auto', columnGap: '3rem'}}>

                {
                    Array.isArray(prediction) ?

                        prediction.map((pred) => (
                            <PredictionItem predictionObject={pred}/>
                        ))
                        :
                        <PredictionItem predictionObject={prediction}/>

                }


            </div>
            <div>
            </div>


            <form className="RatingForm">
                <h3 className="PredictionTitle">Please rate the prediction</h3>
                <br/>
                <div className="radio-toolbar">

                    <input onClick={(event) => updateRating(event.target.value)} type="radio" id="poor" name="rating"
                           value="poor" checked={rating === "poor"}/>
                    <label htmlFor="poor">Poor</label>

                    <input onClick={(event) => updateRating(event.target.value)} type="radio" id="acceptable"
                           name="rating" value="acceptable" checked={rating === "acceptable"}/>
                    <label htmlFor="acceptable">Acceptable</label>

                    <input onClick={(event) => updateRating(event.target.value)} type="radio" id="good" name="rating"
                           value="good" checked={rating === "good"}/>
                    <label htmlFor="good">Good</label>

                    <input onClick={(event) => updateRating(event.target.value)} type="radio" id="verygood"
                           name="rating" value="verygood" checked={rating === "verygood"}/>
                    <label htmlFor="verygood">Very good</label>

                    <input onClick={(event) => updateRating(event.target.value)} type="radio" id="excellent"
                           name="rating" value="excellent" checked={rating === "excellent"}/>
                    <label htmlFor="excellent">Excellent</label>

                </div>

            </form>
        </div>
    )

}