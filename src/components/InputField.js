import {Form, FormLabel} from "react-bootstrap";
import React from "react";
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

    let htmlTag = (<p>InputField not recognized</p>)

    switch (type){

        case 'file':
            htmlTag = (<Form.File type="file" onChange={ async (event) =>  dispatch(addData(id, await toBase64(event.target.files[0])))} ></Form.File>)
            break
        case 'float':
            htmlTag = (<input className="InputField" type="number" step="any"  onChange={(event) => dispatch(addData(id, event.target.value))} required></input>)
            break
        case 'str':
            htmlTag = (<input className="InputField" type="text" onChange={(event) => dispatch(addData(id, '"'+event.target.value+'"'))} required></input>)
            break
        default:
            return ''
    }



    return (<Form.Group className="InputGroup">
        <Form.Label className="InputLabel">{label}</Form.Label>
        {htmlTag}
    </Form.Group>)



}