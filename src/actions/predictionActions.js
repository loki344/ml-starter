import {ADD_DATA, CHECK_DATA, POST_PREDICTION} from "../constants/predictionConstants";
import axios from "axios";

export const addData = (id, value) => async (dispatch) =>{
    dispatch({type: ADD_DATA, payload: {"id": id, "value": value} })
}

export const postPrediction = (requestBody) => async (dispatch) => {

    const {data} = await axios.post('http://localhost:8000/predictions', requestBody)
    let payload =  typeof data.prediction === 'object' ? data.prediction : [data.prediction]

    dispatch({type: POST_PREDICTION, payload:payload})

}