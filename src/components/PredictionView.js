import React from "react";
import {useSelector} from "react-redux";


export const PredictionView = () => {

    const predictionObject = useSelector(state => state.prediction)
    const {prediction} =  predictionObject

    return(

        <div>
            <h3>Your prediction:</h3>
            {
                prediction.map((pred) => (
                        typeof pred === 'object' && pred !== null ?
                            Object.keys(pred).map(key =>
                                <div>
                                    <p>{key}: {pred[key]}</p>
                                </div>)
                            :
                            <p>{pred}</p>
                    )
                )
            }
        </div>
    )

}