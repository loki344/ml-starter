import {GET_CONFIGURATION} from "../constants/configurationConstants";

const initialState = {'applicationName': '', 'description': '', 'inputFields': [], 'requestObject': {}}

export const configurationReducer = (state = initialState, action) => {

    switch (action.type){
        case GET_CONFIGURATION:
        return {...state, applicationName: action.payload.applicationName, inputFields: action.payload.inputFields, requestObject: action.payload.requestObject, description: action.payload.description}

        default:
            return state
    }


}

