import React, {useState} from "react";
import {useDispatch} from "react-redux";
import {addData} from "../actions/predictionActions";
import '../styles/InputFields.css'


export const InputField = ({inputField}) => {

    const [fileName, setFileName] = useState('No file chosen')


    const toBase64 = file => new Promise((resolve, reject) => {
        console.log(file)
        if (file === undefined){
            resolve('')
        }
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result.split(',')[1]);

        reader.onerror = error => reject(error);

    });


    const {id, type, label} = inputField
    const dispatch = useDispatch();

    let htmlTag = (<p>InputField not recognized</p>)
    switch (type){

        case 'file':
            htmlTag = (
                <div style={{textAlign:'center'}}>
                    <label className="InputLabel">{label}</label>
                    <input onChange={ async (event) => {
                        dispatch(addData(id, await toBase64(event.target.files[0])))
                        setFileName(event.target.files[0] !== undefined ? event.target.files[0].name.substring(0,30) : 'No file chosen')
                    }} type="file" id="actual-btn" hidden/>
                    <br/>
                    <label  className="FileLabel" htmlFor="actual-btn">Choose File</label>
                    <br/>
                    <br/>

                    <span id="file-chosen" >{fileName}</span>
                </div>)
            break
        case 'float':
            htmlTag = (
                <div style={{marginBottom:'1.5rem'}}>
                <label className="InputLabel">{label}</label>
                <input className="InputField" type="number" step="any"  onChange={(event) => dispatch(addData(id, event.target.value))}/>
                </div>
            )
            break
        case 'str':
            htmlTag = (
                <div style={{marginBottom:'1.5rem'}}>
                <label className="InputLabel">{label}</label>
                <input className="InputField" type="text" onChange={(event) => dispatch(addData(id, event.target.value))}/>
                </div>
            )
            break
        default:
            return ''
    }



    return (<>{htmlTag}</>)



}