import {ADD_DATA, POST_PREDICTION} from "../constants/predictionConstants";



const initialState = {"inputData":{}, "prediction":[], "id":''}


export const predictionReducer = (state = initialState, action) => {

    switch (action.type){
        case ADD_DATA:
            state.inputData[action.payload.id] = action.payload.value
            return {...state, "inputData":{...state.inputData, [action.payload.id]:action.payload.value}}
        case POST_PREDICTION:
            console.log(action.payload)
            state.prediction = action.payload.prediction
            state.id = action.payload.id
            return state
        default:
            return state
}


}
