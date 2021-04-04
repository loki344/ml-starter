import {GET_CONFIGURATION} from "../constants/configurationConstants";
import axios from 'axios'

export const getConfiguration = () => async (dispatch) =>{
    const {data} = await axios.get('http://localhost:8000/configs')
    dispatch({type: GET_CONFIGURATION, payload: data })

}