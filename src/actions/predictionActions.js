import {ADD_DATA} from "../constants/predictionConstants";

export const addData = (id, value) => async (dispatch) =>{
    dispatch({type: ADD_DATA, payload: {"id": id, "value": value} })
}