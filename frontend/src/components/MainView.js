import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {resetInputData} from "../actions/predictionActions";
import '../styles/CustomButton.css';
import {InputDataForm} from "./InputDataForm";
import {PredictionForm} from "./PredictionForm";

export const MainView = () => {


    const dispatch = useDispatch();
    const configuration = useSelector(state => state.configuration)
    const {description} = configuration


    const {prediction, showSpinner} = useSelector(state => state.prediction)

    useEffect(() => {
        dispatch(resetInputData())
    }, [dispatch])

    const getGridClass = () => {
        return prediction.length > 0 && !showSpinner? "GridSideBySide" : "GridBigColumns"
    }

    function isSpinnerVisible() {
        return showSpinner ? "Hidden": "";
    }

    return (

        <div>

            <h3 className={'PredictionTitle '+isSpinnerVisible()}>{description}</h3>
            <div style={{marginTop: "3rem"}} className={getGridClass()}>
                <InputDataForm/>
                <PredictionForm/>
            </div>
        </div>

    )

}
