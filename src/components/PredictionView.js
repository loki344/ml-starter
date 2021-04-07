import React from "react";
import {useSelector} from "react-redux";


export const PredictionView = () => {

    const predictionObject = useSelector(state => state.prediction)
    const {prediction, inputData} =  predictionObject

    const configuration = useSelector(state => state.configuration)
    const {inputFields} =  configuration
    inputFields.map(inputField => console.log(inputField))

    return(

        <div>
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

            

        </div>
    )

}