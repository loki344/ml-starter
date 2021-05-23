import React from "react";

export const PredictionItem = (props) => {

    const prediction = props.predictionObject

    return (
        typeof prediction === 'object' && prediction !== null ?
            <>
                {
                    Object.keys(prediction).map(key =>
                        <div>
                            <span className="PredictionItem">{key}: </span>
                            <span className="PredictionItem">{prediction[key]}</span>
                        </div>
                    )
                }

                <div style={{marginBottom: "1rem"}}/>
            </>
            :
            <div className="PredictionItem"
                 style={{gridColumnStart: '1', gridColumnEnd: -1}}>
                {

                    typeof prediction === 'boolean' ?
                        prediction.toString() : prediction

                }
            </div>
    )
}
