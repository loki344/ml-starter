import {Button, Form} from "react-bootstrap";
import {InputField} from "./InputField";
import React, {useEffect, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {getConfiguration} from "../actions/configurationActions";
import { useHistory } from "react-router-dom";
import {postPrediction} from "../actions/predictionActions";

export const InputDataView = () => {


    const dispatch = useDispatch();

    const configuration = useSelector(state => state.configuration)
    const {inputFields, requestObject} = configuration

    const {inputData} = useSelector(state => state.prediction)


    useEffect(() => {
        dispatch(getConfiguration())
    }, [dispatch])

    let history = useHistory();


    const clickHandler = async (e) => {
        e.preventDefault()

        let requestData = String(requestObject.inputData)
        for (let inputField of inputFields){
            requestData = requestData.replace(inputField.id, inputData[inputField.id])
        }

        let requestBody = '{"inputData":'+requestData+'}'
        requestBody = requestBody.replace('/','\/')
        requestBody = JSON.parse(requestBody)

        //TODO why do i need await here?
        await dispatch(postPrediction(requestBody))
        history.push('/prediction')
    }


    return (
        <div className="InputDataView">

    <Form className="InputDataForm" >
        {inputFields.map((inputField) => (
            <InputField key={inputField.label} inputField={inputField}>
            </InputField>
        ))}
        <br/>
        <br/>
        <Button onClick={clickHandler} type="submit">Start prediction</Button>
    </Form>
        </div>
    )

}
