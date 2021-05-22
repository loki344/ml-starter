import {ADD_DATA, POST_PREDICTION, RESET_INPUT_DATA, SET_RATING, SHOW_SPINNER} from "../constants/predictionConstants";


const initialState = {"inputData": {}, "prediction": [], "id": '', "showSpinner": false, "rating": ""}

export const predictionReducer = (state = initialState, action) => {

    switch (action.type) {
        case ADD_DATA:
            state.inputData[action.payload.id] = action.payload.value
            return {...state, "inputData": {...state.inputData, [action.payload.id]: action.payload.value}}
        case POST_PREDICTION:

            return {...state, prediction: action.payload.prediction, id: action.payload.id}

        case RESET_INPUT_DATA:

            return {...state, inputData: action.payload}

        case SHOW_SPINNER:

            return {...state, showSpinner: action.payload}

        case SET_RATING:

            return {...state, rating: action.payload}

        default:
            return state
    }


}
