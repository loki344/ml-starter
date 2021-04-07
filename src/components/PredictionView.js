import React from "react";
import {useDispatch, useSelector} from "react-redux";


export const PredictionView = () => {

    const predictionObject = useSelector(state => state.prediction)
    const {prediction, inputData, id} =  predictionObject

    const configuration = useSelector(state => state.configuration)
    const {inputFields} =  configuration

    const dispatch = useDispatch();

    const handleInput = (event) =>{

        dispatch()

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

            <form className="RatingForm">
                <h3 className="PredictionTitle">Please rate the prediction</h3>

                <div className="RadioGroup">
                    <span className="RadioItemWrapper">
                        <input name="rating" type="radio" value="1" onInput={handleInput} className="RadioButton"/>
                        <label>1 - Poor</label>
                    </span>

                    <span className="RadioItemWrapper">
                        <input name="rating"  type="radio" value="2" onInput={handleInput} className="RadioButton"/>
                        <label>2 - Acceptable</label>
                    </span>

                    <span className="RadioItemWrapper">
                        <input name="rating"  type="radio" value="3" onInput={handleInput} className="RadioButton"/>
                        <label>3 - Good</label>
                    </span>

                    <span className="RadioItemWrapper">
                        <input name="rating"  type="radio" value="4" onInput={handleInput} className="RadioButton"/>
                        <label>4 - Very Good</label>
                    </span>

                    <span className="RadioItemWrapper">
                        <input name="rating"  type="radio" value="5" onInput={handleInput} className="RadioButton"/>
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