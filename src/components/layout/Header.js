import React, { Component } from 'react'
import {Link} from "react-router-dom"
import {useSelector} from "react-redux";

export const Header = () => {

    const configuration = useSelector(state => state.configuration)
     const {applicationName} = configuration


        return (
            <nav className="navbar navbar-expand navbar-dark bg-dark">
                <a className="navbar-brand" href="#">{applicationName}</a>
                <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                    <div className="navbar-nav">
                        <a className="nav-item nav-link active" href="#">Home <span className="sr-only">(current)</span></a>
                    </div>
                </div>
            </nav>

        )

}

export default Header;