import React from "react";

export const PredictionItem = (props) => {

    const prediction = props.predictionObject

return(
    typeof prediction === 'object' && prediction !== null ?
        Object.keys(prediction).map(key =>
            <>
                <div className="PredictionItem" style={{
                    textAlign: "left",
                    justifyContent: 'center',
                    display: 'flex',
                    alignItems: 'center'}}>{key}:
                </div>
                <div className="PredictionItem" style={{
                    textAlign: "left",
                    justifyContent: 'left',
                    display: 'flex',
                    alignItems: 'center',
                    marginLeft:'2rem'}}>{prediction[key]}</div>
            </>
        )
        :
        <div className="PredictionItem"
             style={{gridColumnStart: '1', gridColumnEnd: -1}}>{prediction}</div>

)

}