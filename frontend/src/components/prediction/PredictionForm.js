import React, {useEffect, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {patchRating} from "../../actions/predictionActions";
import '../../styles/CustomRadioButton.css'
import {PredictionItem} from "./PredictionItem";
import {SET_RATING} from "../../constants/predictionConstants";
import Notiflix from "notiflix-react";

export const PredictionForm = () => {

    const predictionObject = useSelector(state => state.prediction)
    const {prediction, id, showSpinner, rating} = predictionObject

    const dispatch = useDispatch();

    const [notificationCount, setNotificationCount] = useState(0)

    useEffect(() => {
        Notiflix.Notify.Init({position: "right-bottom", timeout: 5000});
    })

    const INTERVAL_MS = 20000;

    useEffect(() => {
        const interval = setInterval(() => {
            let notification = "Edit the data and make another prediction :)"

            if (rating === "") {
                notification = "Please rate the prediction and improve the algorithm"
            }

            if (prediction.length > 0 && !showSpinner && notificationCount < 2) {
                Notiflix.Notify.Info(notification)
                setNotificationCount(notificationCount + 1)
            }
        }, INTERVAL_MS);

        return () => clearInterval(interval);
    }, [prediction, showSpinner, notificationCount, rating])

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
            <div>
                {
                    prediction.map((pred) => (
                        <>
                            <PredictionItem predictionObject={pred}/>
                        </>
                    ))
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
