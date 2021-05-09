import {InputField} from "./InputField";
import React from "react";
import {useSelector} from "react-redux";
import {StartPredictionButton} from "./StartPredictionButton";

export const InputDataForm = () => {

    const configuration = useSelector(state => state.configuration)
    const prediction = useSelector(state => state.prediction)
    const {inputFields} = configuration
    const {showSpinner} = prediction


    function getClassForSpinner() {
        return showSpinner ? "" : "Hidden"
    }

    function getClassForInputForm() {
        return showSpinner ? "Hidden" : "";
    }

    return (

        <>
            <div className={getClassForSpinner()}>
                <div className={"loadingio-spinner-blocks-8ifaqit3nsg"}>
                    <div className="ldio-1t8hoj7ze7s">
                        <div style={{left: "38px", top: "38px", animationDelay: "0s"}}/>
                        <div style={{left: "80px", top: "38px", animationDelay: "0.125s"}}/>
                        <div style={{left: "122px", top: "38px", animationDelay: "0.25s"}}/>
                        <div style={{left: "38px", top: "80px", animationDelay: "0.875s"}}/>
                        <div style={{left: "122px", top: "80px", animationDelay: "0.375s"}}/>
                        <div style={{left: "38px", top: "122px", animationDelay: "0.75s"}}/>
                        <div style={{left: "80px", top: "122px", animationDelay: "0.625s"}}/>
                        <div style={{left: "122px", top: "122px", animationDelay: "0.5s"}}/>
                    </div>
                </div>
                <h3>Generate prediction, lean back..</h3>
            </div>

            <div className={"InputDataForm" + ' ' + getClassForInputForm()}>
                {inputFields.map((inputField) => (
                    <InputField key={inputField.label} inputField={inputField}>
                    </InputField>
                ))}
                <StartPredictionButton/>
            </div>


        </>


    )


}
