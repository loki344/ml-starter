import React, {useEffect} from 'react';
import LogRocket from 'logrocket';
import {useDispatch, useSelector} from 'react-redux'
import {getConfiguration} from "./actions/configurationActions";
import {mapFieldType} from "./mappers/typeMapper";

const App = () => {
    LogRocket.init('bc26dt/ml-starter-frontend');

    const dispatch = useDispatch();

    const configuration = useSelector(state => state.configuration)
    const {applicationName, inputFields} = configuration

    useEffect(() => {
        dispatch(getConfiguration())
    }, [dispatch])


    return (
        <div className="App">
            <h1>{applicationName}</h1>
            <form>
            {inputFields.map((inputField) => (
                <label>
                    <p>{inputField.description}</p>
                    <input type={mapFieldType(inputField.type)}/>
                </label>
            ))}
            </form>
        </div>);
}

export default App;
