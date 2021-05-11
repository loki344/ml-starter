import React, {useEffect, useState} from "react";
import {useDispatch} from "react-redux";
import {addData} from "../actions/predictionActions";
import '../styles/InputFields.css'
import Notiflix from "notiflix-react";


export const InputField = ({inputField}) => {

    const [fileName, setFileName] = useState('No file chosen')
    const [textColor, setTextColor] = useState('black')
    const [fileData, setFileData] = useState ('')

    useEffect(() => {
        Notiflix.Notify.Init({position: "right-bottom",timeout: 5000});
    }, [Notiflix])

    const toBase64 = file => new Promise((resolve, reject) => {
        if (file === undefined){
            resolve('')
        }
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function(event) {
            let result = reader.result
            setFileData(result)
            resolve(result.split(',')[1])
        };
        reader.onerror = error => reject(error);

    });

    const validateFile = file => {
        if (file === undefined){
            return false
        }
        let extensionRegex = new RegExp('(\.jpg|\.jpeg|\.png)$')
        let validation = extensionRegex.exec(file.name)
        return validation !== null
    }


    const {id, type, label} = inputField
    const dispatch = useDispatch();

    let htmlTag = (<p>InputField not recognized</p>)
    switch (type){

        case 'image':
            htmlTag = (
                <div style={{textAlign:'center'}}>
                    <label className="InputLabel">{label}</label>
                    <input onChange={ async (event) => {
                        if (!validateFile(event.target.files[0])){
                            Notiflix.Notify.Failure("File format not allowed")
                            setFileName('Allowed formats: jpg, jpeg, png')
                            setTextColor('red')
                            event.target.value = null
                            return
                        }
                        setTextColor('black')
                        dispatch(addData(id, await toBase64(event.target.files[0])))
                        setFileName(event.target.files[0] !== undefined ? event.target.files[0].name.substring(0,30) : 'No file chosen')
                    }} type="file" accept="image/*" id="actual-btn" hidden/>
                    <br/>
                    <label className="FileLabel" htmlFor="actual-btn">Choose File</label>
                    <br/>
                    <br/>

                    <div id="file-chosen" style={{color: textColor}} >{fileName}</div>

                        <img style={{marginTop: "2rem", width: "auto", maxHeight: "30rem"}} src={fileData}/>

                </div>)
            break
        case 'number':
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