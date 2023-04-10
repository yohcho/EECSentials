import { React, useRef, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"

import logo from "../assets/logo.png"
import submitButton from "../assets/chat/submit.png"
import homelogo from "../assets/chat/home-logo.png"
import newRequest from "../apiCall"

import "./chat.css"

const Chat = ()=>{
    const [awaiting, setAwaiting] = useState(false)
    const [messageLog, setMessageLog] = useState([{
        message: "Hi! What can I help with you today?",
        sender: "ai",
        loading: true
    }])

    useEffect(()=>{
        setTimeout(()=>{
            setMessageLog([{
                message: "Hi! What can I help with you today?",
                sender: "ai",
                loading: false
            }])
        },1500)
    },[])

    const inputText = useRef("")
    const navigate = useNavigate()

    const handleSubmit = async ()=>{
        if(awaiting) return
        if(inputText.current.value==="") return
        const newMessage = {
            message: inputText.current.value,
            sender: "human"
        }
        setAwaiting(true)
        inputText.current.value=""
        setMessageLog(prevMessageLog=>[...prevMessageLog,newMessage,{message:"loading",loading:true,sender:"ai"}])
        await newRequest(newMessage.message,setMessageLog,setAwaiting)
    }

    const ContentLeft = ()=>{
        return(
            <div className="chat-content-left">
                <img className="chat-content-left-homelogo" alt="home logo" src={homelogo} onClick={()=>navigate("/")}/>
                <h1>EECSentials</h1>
                <h3>by EECS, for EECS</h3>
                <img className="chat-content-left-uofmlogo" alt="uofmlogo" src={logo}/>
            </div>
        )
    }

    const handleScrolling = (ref)=>{
        if(ref){
            ref.scrollTop = ref.scrollHeight-ref.getBoundingClientRect().height
        }
    }

    const ContentRight = ()=>{
        return(
            <div className="chat-content-right">
                <div className="chat-content-right-log" ref={handleScrolling}>
                    {messageLogDisplay()}
                    <div className="chat-content-right-log-padding"></div>
                </div>                
                <div className="chat-content-right-input">
                    <textarea 
                        ref={inputText} 
                        placeholder="What class should I take next semester?" 
                        onSubmit={handleSubmit}
                        onKeyDown={(e)=> e.keyCode===13 &&  (e.preventDefault()|| handleSubmit())}
                    />
                    <img alt="submit button" src={submitButton} onClick={handleSubmit}/>
                </div>
            </div>
        )
    }

    const messageLogDisplay = ()=>{
        return messageLog.map(el=>{
            const classname = `chat-content-right-log-indiv ${el.sender[0]==='a' ? "ai-message" : "human-message"}`
            if(el.loading){
                return(
                    <div className={`${classname} loading`} key={el.message}>
                        <div></div>
                        <div></div>
                        <div></div>
                    </div>
                )
            }
            return(
                <div className={classname} key={`${el.message}-${el.sender}`}>
                    {el.message}
                </div>
            )
        })
    }

    return(
        <div className="chat-root">
            {ContentLeft()}
            {ContentRight()}
        </div>
    )
}

export default Chat;