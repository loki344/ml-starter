import {Form, FormLabel} from "react-bootstrap";
import React, {useEffect, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {addData} from "../actions/predictionActions";

export const InputField = ({inputField}) => {

    const toBase64 = file => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve('"'+reader.result.split(',')[1]+'"');
        reader.onerror = error => reject(error);
    });


    const {id, type, label} = inputField
    const dispatch = useDispatch();
    const prediction =  useSelector(state => state.prediction);
    const {inputData} = prediction

    let htmlTag = (<p>InputField not recognized</p>)

    switch (type){

        case 'file':
            htmlTag = (<input type="file" onChange={ async (event) =>  dispatch(addData(id, await toBase64(event.target.files[0])))} ></input>)
            break
        case 'float':
            htmlTag = (<input type="number" step="any" onChange={(event) => dispatch(addData(id, event.target.value))}></input>)
            break
        default:
            return ''
    }



    return (<Form.Label>
        {label}
        {htmlTag}
    </Form.Label>)



}