import {InputField} from "./InputField";
import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {getConfiguration} from "../actions/configurationActions";
import { useHistory } from "react-router-dom";
import {postPrediction, resetInputData} from "../actions/predictionActions";
import '../CustomButton.css'
import {RESET_INPUT_DATA} from "../constants/predictionConstants";

export const InputDataView = () => {


    const dispatch = useDispatch();
    const configuration = useSelector(state => state.configuration)
    const {inputFields, requestObject, description} = configuration

    const {inputData} = useSelector(state => state.prediction)




    let history = useHistory();

    useEffect(() => {
        dispatch(resetInputData())
    }, [dispatch])


    const clickHandler = async (e) => {
        e.preventDefault()

        console.log(inputData)

        for (let inputField of inputFields){
            if (inputData[inputField.id] === undefined || inputData === undefined){
                alert('Please fill out all fields')
                return
            }
        }

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

        <h3 className="PredictionTitle">{description}</h3>

            <br/>
            <br/>

        <form className="InputDataForm" >
            {inputFields.map((inputField) => (
                <InputField key={inputField.label} inputField={inputField}>
                </InputField>
            ))}
        <br/>
            <button className="button" onClick={clickHandler} type="submit">
                Start prediction
                <div className="button__horizontal"/>
                <div className="button__vertical"/>
            </button>

    </form>
        </div>
    )

}
