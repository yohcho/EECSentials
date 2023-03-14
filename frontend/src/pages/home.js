import React from "react";
import { Link, useNavigate } from "react-router-dom"

import logo from "../assets/logo.png"
import fblogo from "../assets/home/fblogo.png"
import iglogo from "../assets/home/iglogo.png"
import twlogo from "../assets/home/twlogo.png"

import "./home.css"

const Home = ()=>{
    const navigate  = useNavigate()

    const TopBar = ()=>{
        return (
            <div className="home-topbar">
                <img alt="uofmlogo" src={logo}/>
                <div className="home-topbar-navigation">
                    <Link className="home-topbar-navigation-indiv" to="/">HOME</Link>
                    <Link className="home-topbar-navigation-indiv" to="/">ABOUT</Link>
                    <Link className="home-topbar-navigation-indiv" to="/chat">PRODUCT</Link>
                    <Link className="home-topbar-navigation-indiv" to="/">CONTACT</Link>
                </div>
            </div>
        )
    }

    const Content = ()=>{
        return(
            <div className="home-content">
                <div className="home-content-header">
                    <h1>EECSentials</h1>
                    <h3>by EECS, for EECS</h3>
                </div>
                <div className="home-content-getStarted" onClick={()=>navigate("/chat")}>Get Started</div>
                <div className="home-content-social">
                    <img alt="social media logo" src={twlogo}/>
                    <img alt="social media logo" src={iglogo}/>
                    <img alt="social media logo" src={fblogo}/>                    
                </div>
            </div>
        )
    }

    return(
        <div className="home-root">
            {TopBar()}
            {Content()}
        </div>
    )
}

export default Home;