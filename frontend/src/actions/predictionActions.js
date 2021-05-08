import {ADD_DATA, POST_PREDICTION, RATE_PREDICTION, RESET_INPUT_DATA} from "../constants/predictionConstants";
import axios from "axios";

export const addData = (id, value) => async (dispatch) =>{
    dispatch({type: ADD_DATA, payload: {"id": id, "value": value} })
}

export const resetInputData = () => async (dispatch) =>{
    dispatch({type: RESET_INPUT_DATA, payload: {}})
}

export const postPrediction = (requestBody) => async (dispatch) => {

    const {data} = await axios.post('/api/predictions', requestBody)
    let payload =  {"id": data.id, "prediction": typeof data.prediction === 'object' ? data.prediction : [data.prediction]}
    console.log(payload)
    dispatch({type: POST_PREDICTION, payload:payload})

}

export const patchRating = (id, rating) => async (dispatch) =>{

    let requestBody = {"rating": rating}

    await axios.patch('/api/predictions/'+ id, requestBody)

    dispatch({type: RATE_PREDICTION})

    // TODO patch something to trigger next run?
}