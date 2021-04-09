import React, {useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {patchRating} from "../actions/predictionActions";
import {useHistory} from "react-router-dom";
import '../CustomRadioButton.css'


export const PredictionView = () => {

    let history = useHistory();

    const predictionObject = useSelector(state => state.prediction)
    const {prediction, previousInputData, id} =  predictionObject

    const configuration = useSelector(state => state.configuration)
    const {inputFields} =  configuration
    
    const [rating, setRating] = useState('')

    const dispatch = useDispatch();
    
    const handleSubmit = (event) =>{
        event.preventDefault()

        if (rating === ''){
            alert('Please choose a radiobutton')
            return
        }

        dispatch(patchRating(id,rating ))

        history.push('/thanks')
    }

    return(

        <div className="PredictionView">
            <h2 className="PredictionTitle">Prediction:</h2>
            <br/>
            {
                prediction.map((pred) => (

                        typeof pred === 'object' && pred !== null ?
                            Object.keys(pred).map(key =>

                                    <div className="PredictionItem">{key}: {pred[key]}</div>
                                )
                            :
                        <div className="PredictionItem">{pred}</div>

                    )
                )
            }
            <br/>
            <br/>
            <h2 className="PredictionTitle">Your input:</h2>
            <br/>
            {inputFields.map((inputField) => (

                inputField.type === 'file' ?

                <img src={`data:image/png;base64,${previousInputData[inputField.id]}`} style={{maxWidth: '50%', height: 'auto'}}  alt=""/>
                :
                <div>
                    <p className="PredictionItem">{inputField.label}: {previousInputData[inputField.id]}</p>
                </div>

            ))}

            <br/>
            <br/>
            <br/>

            <form className="RatingForm" onSubmit={handleSubmit}>
                <h3 className="PredictionTitle">Please rate the prediction</h3>
                <br/>
                <div className="radio-toolbar">

                    <input onChange={(event) => setRating(event.target.value)} type="radio" id="poor" name="radioFruit" value="poor"/>
                    <label htmlFor="poor">Poor</label>

                    <input onChange={(event) => setRating(event.target.value)} type="radio" id="acceptable" name="radioFruit" value="acceptable"/>
                    <label htmlFor="acceptable">Acceptable</label>

                    <input onChange={(event) => setRating(event.target.value)} type="radio" id="good" name="radioFruit" value="good"/>
                    <label htmlFor="good">Good</label>

                    <input onChange={(event) => setRating(event.target.value)} type="radio" id="verygood" name="radioFruit" value="verygood"/>
                    <label htmlFor="verygood">Very good</label>

                    <input onChange={(event) => setRating(event.target.value)} type="radio" id="excellent" name="radioFruit" value="excellent"/>
                    <label htmlFor="excellent">Excellent</label>

                </div>

                <br/>
                <br/>
                <br/>
                <button className="button" type="submit">
                    Submit
                    <div className="button__horizontal"/>
                    <div className="button__vertical"/>
                </button>

            </form>
        </div>
    )

}