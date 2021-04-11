import React, {useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {patchRating} from "../actions/predictionActions";
import {useHistory} from "react-router-dom";
import '../styles/CustomRadioButton.css'
import {PredictionItem} from "./PredictionItem";
import {NextPredictionButton} from "./NextPredictionButton";

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
    //TODO make not objects work also
    return(

        <div>
            <h2 className="PredictionTitle">Prediction</h2>
            <br/>


                <div style={{display: 'inline-grid', gridTemplateColumns: '20% auto', columnGap:'3rem'}}>
                    {
                        prediction.map((pred) => (
                        <>
                            <PredictionItem predictionObject={pred}></PredictionItem>
                            <div style={{gridColumnStart: '1', gridColumnEnd: -1, height:'2rem', width:'100%'}}/>
                        </>
                            )
                        )
                    }

                </div>

            <br/>
            <br/>
            <br/>
            <div style={{margin:'0 auto', width:'60%'}}>
                <h2 className="PredictionTitle">Your input</h2>
                <br/>
                {inputFields.map((inputField) => (

                    inputField.type === 'image' ?

                        <img src={`data:image/png;base64,${previousInputData[inputField.id]}`} style={{maxWidth: '100%', height: 'auto', border: 'solid black 1px', padding:'10px'}}  alt=""/>
                        :
                        <div style={{display:'grid', gridTemplateColumns:'50% auto'}}>
                            <div className="PredictionItem" style={{textAlign:'left'}}>{inputField.label}:</div>
                            <div className="PredictionItem" style={{textAlign:'left', alignItems:"left"}}>{previousInputData[inputField.id]}</div>
                        </div>

                ))}

            </div>


            <NextPredictionButton/>

            <form className="RatingForm" onSubmit={handleSubmit}>
                <h3 className="PredictionTitle">Please rate the prediction</h3>
                <br/>
                <div className="radio-toolbar">

                    <input onChange={(event) => setRating(event.target.value)} type="radio" id="poor" name="rating"
                           value="poor"/>
                    <label htmlFor="poor">Poor</label>

                    <input onChange={(event) => setRating(event.target.value)} type="radio" id="acceptable" name="rating" value="acceptable"/>
                    <label htmlFor="acceptable">Acceptable</label>

                    <input onChange={(event) => setRating(event.target.value)} type="radio" id="good" name="rating" value="good"/>
                    <label htmlFor="good">Good</label>

                    <input onChange={(event) => setRating(event.target.value)} type="radio" id="verygood" name="rating" value="verygood"/>
                    <label htmlFor="verygood">Very good</label>

                    <input onChange={(event) => setRating(event.target.value)} type="radio" id="excellent" name="rating" value="excellent"/>
                    <label htmlFor="excellent">Excellent</label>

                </div>

                <button className="button" type="submit">
                    Submit
                    <div className="button__horizontal"/>
                    <div className="button__vertical"/>
                </button>

            </form>
        </div>
    )

}