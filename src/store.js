import {createStore, combineReducers, applyMiddleware, compose} from 'redux'
import thunk from 'redux-thunk'
import {composeWithDevTools} from 'redux-devtools-extension'
import {configurationReducer} from './reducers/configurationReducers'
import {predictionReducer} from "./reducers/predictionReducers";

const reducer = combineReducers({
    configuration: configurationReducer,
    prediction: predictionReducer
})

const initialState = {}

const middleware = [thunk]

const store = createStore(reducer,
    initialState,
    composeWithDevTools(applyMiddleware(...middleware)))

export default store
