import {ADD_DATA} from "../constants/predictionConstants";



const initialState = {"inputData":{}}


export const predictionReducer = (state = initialState, action) => {


    switch (action.type){
        case ADD_DATA:
            state.inputData[action.payload.id] = action.payload.value
            return {...state, "inputData":{...state.inputData, [action.payload.id]:action.payload.value}}

        default:
            return state
}


}
