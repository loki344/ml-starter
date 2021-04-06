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
        console.log(inputData)
        for (let inputField of inputFields){
            console.log(inputField.id)
            console.log(inputData[inputField.id])
            requestData = requestData.replace(inputField.id, inputData[inputField.id])
        }
        let requestBody = '{"inputData": '+requestData+'}'
        requestBody = JSON.parse(requestBody)

        const {data} = await axios.post('http://localhost:8000/predictions', requestBody)
        console.log(data);
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
                        <div>
                        <p>{pred}</p>
                        </div>
                    ))
                }
            </div>
            </div>);
}

export default App;
