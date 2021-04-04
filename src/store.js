import {createStore, combineReducers, applyMiddleware, compose} from 'redux'
import thunk from 'redux-thunk'
import {composeWithDevTools} from 'redux-devtools-extension'
import {configurationReducer} from './reducers/configurationReducers'

const reducer = combineReducers({
    configuration: configurationReducer,
})

const initialState = {}

const middleware = [thunk]

const store = createStore(reducer,
    initialState,
    composeWithDevTools(applyMiddleware(...middleware)))

export default store
