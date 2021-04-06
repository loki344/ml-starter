import React, {useEffect, useState} from 'react';
import LogRocket from 'logrocket';
import {useDispatch, useSelector} from 'react-redux'
import {getConfiguration} from "./actions/configurationActions";
import {InputField} from "./components/InputField";
import {Form, FormLabel, Button} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from "axios";

const App = () => {
    LogRocket.init('bc26dt/ml-starter-frontend');


    const dispatch = useDispatch();

    const configuration = useSelector(state => state.configuration)
    const {applicationName, inputFields, requestObject} = configuration

    const {inputData} = useSelector(state => state.prediction)


    useEffect(() => {
        dispatch(getConfiguration())
    }, [dispatch])


    const [prediction, setPrediction] = useState([])


    const clickHandler = async (e) => {
        e.preventDefault()

        let requestData = String(requestObject.inputData)
        for (let inputField of inputFields){
            requestData = requestData.replace(inputField.id, inputData[inputField.id])
        }

        let requestBody = '{"inputData":'+requestData+'}'
        requestBody = requestBody.replace('/','\/')

        console.log(requestBody)
        requestBody = JSON.parse(requestBody)
        console.log(requestBody)
        const {data} = await axios.post('http://localhost:8000/predictions', requestBody)
        setPrediction(data.prediction)
    }


    return (
        <div className="App">
            <h1>{applicationName}</h1>
            <Form>
            {inputFields.map((inputField) => (
                <InputField key={inputField.label} inputField={inputField}>
                </InputField>
            ))}
            <br/>
            <br/>
            <Button onClick={clickHandler} type="submit">Start prediction</Button>
            </Form>
            <div>
                <h3>Your prediction:</h3>
                {
                    prediction.map((pred) => (
                        typeof pred === 'object' && pred !== null ?
                    Object.keys(pred).map(key =>
                            <div>
                                <p>{key}: {pred[key]}</p>
                            </div>)
                            :
                                    <p>{pred}</p>
                            )
                    )
                }
            </div>
            </div>);
}

export default App;
