import {Form, FormLabel} from "react-bootstrap";
import React, {useState} from "react";

export const InputField = (props) => {
    const {inputField} = props;

    let htmlTag = (<p>InputField not recognized</p>)
    console.log(inputField.inputField)
    switch (inputField.type){

        case 'file':
            htmlTag = (<Form.File as='file'></Form.File>)
            break
        default:
            return ''
    }

    return (<Form.Label>
        {inputField.label}
        {htmlTag}
    </Form.Label>)

}