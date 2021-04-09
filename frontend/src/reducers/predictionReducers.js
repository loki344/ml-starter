import {ADD_DATA, POST_PREDICTION, RATE_PREDICTION, RESET_INPUT_DATA} from "../constants/predictionConstants";



const initialState = {"inputData":{}, "prediction":[], "id":''}


export const predictionReducer = (state = initialState, action) => {

    switch (action.type){
        case ADD_DATA:
            state.inputData[action.payload.id] = action.payload.value
            return {...state, "inputData":{...state.inputData, [action.payload.id]:action.payload.value}}
        case POST_PREDICTION:

            return {...state, prediction: action.payload.prediction, id: action.payload.id}
        case RATE_PREDICTION:

            return state
        case RESET_INPUT_DATA:

            return {...state, inputData: action.payload}

        default:
            return state
}


}
