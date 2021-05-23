import {ADD_DATA, POST_PREDICTION, RESET_INPUT_DATA, SET_RATING, SHOW_SPINNER} from "../constants/predictionConstants";
import axios from "axios";

export const addData = (id, value) => async (dispatch) => {
    dispatch({type: ADD_DATA, payload: {"id": id, "value": value}})
}

export const resetInputData = () => async (dispatch) => {
    dispatch({type: RESET_INPUT_DATA, payload: {}})
}


export const postPrediction = (requestBody) => async (dispatch) => {
    dispatch({type: SET_RATING, payload: ""})
    dispatch({type: SHOW_SPINNER, payload: true})
    const {data} = await axios.post('/api/predictions', requestBody)
    let payload = {
        "id": data.id,
        "prediction": typeof data.prediction === 'object' || data.prediction instanceof Array ? data.prediction : [data.prediction]
    }

    setTimeout(() => {
        dispatch({type: SHOW_SPINNER, payload: false})
    }, 3000)
    setTimeout(() => {
        dispatch({type: POST_PREDICTION, payload: payload})
    }, 3000)

}

export const patchRating = (id, rating) => async (dispatch) => {

    let requestBody = {"rating": rating}
    await axios.patch('/api/predictions/' + id, requestBody)
}
