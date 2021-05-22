import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {patchRating} from "../actions/predictionActions";
import '../styles/CustomRadioButton.css'
import {PredictionItem} from "./PredictionItem";
import {SET_RATING} from "../constants/predictionConstants";
import Notiflix from "notiflix-react";

export const PredictionForm = () => {

    const predictionObject = useSelector(state => state.prediction)
    const {prediction, id, showSpinner, rating} = predictionObject

    const dispatch = useDispatch();

    useEffect(() => {
        Notiflix.Notify.Init({position: "right-bottom", timeout: 5000});
    }, [Notiflix])

    const INTERVAL_MS = 25000;

    useEffect(() => {
        const interval = setInterval(() => {
            if (prediction.length > 0 && !showSpinner) {
                Notiflix.Notify.Info("Edit the data and make another prediction :)")
            }
        }, INTERVAL_MS);

        return () => clearInterval(interval);
    }, [prediction, showSpinner])

    function updateRating(input) {

        dispatch({type: SET_RATING, payload: input})
        Notiflix.Notify.Success('Thank you for your feedback!');
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
                            <>
                                <PredictionItem predictionObject={pred}/>
                            </>
                        ))
                        :
                        <PredictionItem predictionObject={prediction}/>
                }
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
