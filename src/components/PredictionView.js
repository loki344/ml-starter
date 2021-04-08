import React, {useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {patchRating} from "../actions/predictionActions";


export const PredictionView = () => {

    const predictionObject = useSelector(state => state.prediction)
    const {prediction, inputData, id} =  predictionObject

    const configuration = useSelector(state => state.configuration)
    const {inputFields} =  configuration
    
    const [rating, setRating] = useState('')

    const dispatch = useDispatch();
    
    const handleSubmit = (event) =>{
        event.preventDefault()

        dispatch(patchRating(id,rating ))

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

                <p className="PredictionItem">{inputField.label}: {inputData[inputField.id]}</p>
            ))}

            <br/>
            <br/>

            <form className="RatingForm" onSubmit={handleSubmit}>
                <h3 className="PredictionTitle">Please rate the prediction</h3>

                <div className="RadioGroup">
                    <span className="RadioItemWrapper">
                        <input name="rating" type="radio" value="1" onInput={(event) => setRating(event.target.value)} className="RadioButton"/>
                        <label>1 - Poor</label>
                    </span>

                    <span className="RadioItemWrapper">
                        <input name="rating"  type="radio" value="2" onInput={(event) => setRating(event.target.value)}  className="RadioButton"/>
                        <label>2 - Acceptable</label>
                    </span>

                    <span className="RadioItemWrapper">
                        <input name="rating"  type="radio" value="3" onInput={(event) => setRating(event.target.value)}  className="RadioButton"/>
                        <label>3 - Good</label>
                    </span>

                    <span className="RadioItemWrapper">
                        <input name="rating"  type="radio" value="4" onInput={(event) => setRating(event.target.value)}  className="RadioButton"/>
                        <label>4 - Very Good</label>
                    </span>

                    <span className="RadioItemWrapper">
                        <input name="rating"  type="radio" value="5" onInput={(event) => setRating(event.target.value)}  className="RadioButton"/>
                        <label>5 - Excellent</label>
                    </span>

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