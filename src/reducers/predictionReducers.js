import {ADD_DATA, CHECK_DATA, POST_PREDICTION} from "../constants/predictionConstants";



const initialState = {"inputData":{}, "prediction":[], "predictButtonState": 'notReady'}


export const predictionReducer = (state = initialState, action) => {

    switch (action.type){
        case ADD_DATA:
            state.inputData[action.payload.id] = action.payload.value
            return {...state, "inputData":{...state.inputData, [action.payload.id]:action.payload.value}}
        case POST_PREDICTION:
            state.prediction = action.payload
            return state
        default:
            return state
}


}
