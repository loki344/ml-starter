import {GET_CONFIGURATION} from "../constants/configurationConstants";

const initialState = {'applicationName': '', 'inputFields': [], 'requestObject': {}}

export const configurationReducer = (state = initialState, action) => {

    switch (action.type){
        case GET_CONFIGURATION:
            return  action.payload
        default:
            return state
    }


}

