import React, { Component } from 'react'
import {Link} from "react-router-dom"
import {useSelector} from "react-redux";

export const Header = () => {

    const configuration = useSelector(state => state.configuration)
     const {applicationName} = configuration


        return (
            <nav className="navbar navbar-expand navbar-dark bg-dark">
                <Link className="navbar-brand" to="/">{applicationName}</Link>
                <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                    <div className="navbar-nav">
                <Link className="nav-item nav-link active" to="/about">About</Link>
                    </div>
                </div>
            </nav>

        )

}

export default Header;