import {InputField} from "./InputField";
import React from "react";
import {postPrediction} from "../actions/predictionActions";
import {useDispatch, useSelector} from "react-redux";
import {useHistory} from "react-router-dom";


export const InputDataForm = (props) => {

    const dispatch = useDispatch();

    const configuration = useSelector(state => state.configuration)
    const {inputFields, requestObject} = configuration
    console.log(inputFields)
    const {inputData} = props.inputData

    let history = useHistory();

    const clickHandler = async (e) => {
        e.preventDefault()

        for (let inputField of inputFields){
            if (inputData[inputField.id] === undefined || inputData === undefined){
                alert('Please fill out all fields')
                return
            }
        }

        let requestData = JSON.stringify(requestObject.inputData)

        for (let inputField of inputFields){
            let inputFieldToReplace = inputField.type === 'float' ? '"'+inputField.id+'"' : inputField.id
            requestData = requestData.replace(inputFieldToReplace, inputData[inputField.id])
        }

        let requestBody = '{"inputData":'+requestData+'}'
        requestBody = JSON.parse(requestBody)

        //TODO why do i need await here?
        await dispatch(postPrediction(requestBody))
        history.push('/prediction')
    }

    return (

        <form className="InputDataForm" >
            {inputFields.map((inputField) => (

                <InputField key={inputField.label} inputField={inputField}>
                </InputField>
            ))}
            <br/>
            <br/>
            <br/>
            <button className="button" onClick={clickHandler} type="submit">
                Start prediction
                <div className="button__horizontal"/>
                <div className="button__vertical"/>
            </button>

        </form>

    )


}
