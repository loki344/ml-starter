import React, {useEffect, useState} from 'react';
import axios from 'axios'

function App() {
    // Declare a new state variable, which we'll call "count"
    const [inputData, setInputData] = useState({
        firstInput:[5, 2.9, 1, 0.2],
        secondInput:[5, 2.9, 1, 0.2]
    })

    const [imageData, setImageData] = useState()

    const [prediction, setPrediction] = useState([])
    const [prediction2, setPrediction2] = useState([])

    function handleFirstInput(value) {
        inputData.firstInput.push(value)
    }

    function handleSecondInput(value){
        inputData.secondInput.push(value)
    }

    function handleClick() {
        let object = {
            inputData:[inputData.firstInput,inputData.secondInput]
        }
        console.log(object)
        axios.post('http://localhost:8000/predict',object).then(res => {
            console.log(res.data)
            setPrediction([...prediction,res.data])

        })

        console.log({prediction})
    }

    function handleSecondClick() {
        let object = {
            inputData:imageData
        }
        console.log(object)
        axios.post('http://localhost:8000/predict',object).then(res => {
            console.log(res.data)
            setPrediction2([...prediction2,res.data])

        })

        console.log({prediction2})
    }

    return (
        <div>

                <h1>IRIS FLOWER</h1>
                <h3>Flower 1</h3>
                <input
                    type="number"
                    value={inputData.firstInput[0]}
                    onChange={e => handleFirstInput(e.target.value)}
                />
                <input
                    type="number"
                    value={inputData.firstInput[1]}
                    onChange={e => handleFirstInput(e.target.value)}
                />
                <input
                    type="number"
                    value={inputData.firstInput[2]}
                    onChange={e => handleFirstInput(e.target.value)}
                />
                <input
                    type="number"
                    value={inputData.firstInput[3]}
                    onChange={e => handleFirstInput(e.target.value)}
                />
                <h3>Flower 2</h3>
                <input
                    type="number"
                    value={inputData.secondInput[0]}
                    onChange={e => handleSecondInput(e.target.value)}
                />
                <input
                    type="number"
                    value={inputData.secondInput[1]}
                    onChange={e => handleSecondInput(e.target.value)}
                />
                <input
                    type="number"
                    value={inputData.secondInput[2]}
                    onChange={e => handleSecondInput(e.target.value)}
                />
                <input
                    type="number"
                    value={inputData.secondInput[3]}
                    onChange={e => handleSecondInput(e.target.value)}
                />
                <br/>
                <br/>

                <button onClick={handleClick}>Send Data</button>
            <br/>
            <br/>
            {JSON.stringify(prediction)}


            <h1>EFFICIENTNET</h1>
            <p>Place your base64 encoded String here, later, this will be an image upload</p>
            <textarea value={imageData}
             onChange={e => setImageData(e.target.value)} ></textarea>
            <br/>
            <button onClick={handleSecondClick}>Send Data</button>
            <br/>
            {JSON.stringify(prediction2)}



        </div>
    );
}

export default App;
