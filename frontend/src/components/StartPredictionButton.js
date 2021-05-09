import React from "react";
import {postPrediction} from "../actions/predictionActions";
import {useDispatch, useSelector} from "react-redux";

export const StartPredictionButton = () => {


    const {inputData} = useSelector(state => state.prediction)
    const dispatch = useDispatch();

    const configuration = useSelector(state => state.configuration)
    const {inputFields, requestObject} = configuration

    const clickHandler = async (e) => {
        e.preventDefault()

        for (let inputField of inputFields) {
            if (inputData[inputField.id] === undefined || inputData === undefined) {
                alert('Please fill out all fields')
                return
            }
        }

        let requestData = JSON.stringify(requestObject.inputData)

        for (let inputField of inputFields) {
            let inputFieldToReplace = inputField.id
            requestData = requestData.replace(inputFieldToReplace, inputData[inputField.id])
        }

        let requestBody = '{"inputData":' + requestData + '}'
        requestBody = JSON.parse(requestBody)

        await dispatch(postPrediction(requestBody))
    }

    return (


        <button className="button" onClick={clickHandler} type="submit">
            Start prediction
            <div className="button__horizontal"/>
            <div className="button__vertical"/>
        </button>
    )

}