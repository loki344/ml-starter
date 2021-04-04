import React, {useEffect, useState} from 'react';
import LogRocket from 'logrocket';
import {useDispatch, useSelector} from 'react-redux'
import {getConfiguration} from "./actions/configurationActions";
import {mapFieldType} from "./mappers/typeMapper";
import {Form, FormLabel, Button} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from "axios";

const App = () => {
    LogRocket.init('bc26dt/ml-starter-frontend');

    const dispatch = useDispatch();

    const configuration = useSelector(state => state.configuration)
    const {applicationName, inputFields} = configuration

    useEffect(() => {
        dispatch(getConfiguration())
    }, [dispatch])

    const [inputData, setInputData] = useState('')
    const [prediction, setPrediction] = useState([])


    const submitHandler = async (e) => {
        e.preventDefault()
        let requestBody = {'inputData': inputData}
        const {data} = await axios.post('http://localhost:8000/predictions', requestBody)
        console.log(data)
        setPrediction(data.prediction)
    }


    return (
        <div className="App">
            <h1>{applicationName}</h1>
            <Form onSubmit={submitHandler}>
            {inputFields.map((inputField) => (
                <FormLabel key={inputField.name}>
                    <p>{inputField.label}</p>
                    <Form.Control as={mapFieldType(inputField.type)} value={inputData} onChange={(e) => setInputData(e.target.value)}/>
                </FormLabel>
            ))}
            <br/>
            <br/>
            <Button type="submit">Start prediction</Button>
            </Form>
            <div>
                <h3>Your prediction:</h3>
                {
                    prediction.map((pred) => (
                        <div>
                        <p>{pred.className}: {pred.probability}</p>
                        </div>
                    ))
                }
            </div>
            </div>);
}

export default App;
