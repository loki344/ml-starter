import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {resetInputData} from "../actions/predictionActions";
import '../styles/CustomButton.css'
import {InputDataForm} from "./InputDataForm";

export const InputDataView = () => {


    const dispatch = useDispatch();
    const configuration = useSelector(state => state.configuration)
    const {description} = configuration
    const {inputData} = useSelector(state => state.prediction)


    useEffect(() => {
        dispatch(resetInputData())
    }, [dispatch])

    return (
        <div>

        <h3 className="PredictionTitle">{description}</h3>

            <br/>
            <br/>
            <InputDataForm inputData={inputData}/>
        </div>
    )

}
