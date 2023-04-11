import axios from "axios"

const newRequest= async(message,updateLog,updateWaiting,session)=>{
    const config = {
        method: 'get',
        url: 'https://wpr4bkssk4td4csrd5yxm667iq0pcbmj.lambda-url.us-east-2.on.aws/',
        params: {
            message:message,
            session:session? session : "false"
        }
    }
    const response = await axios(config)
    updateLog(prevLog=>{
        const newLog = [...prevLog]
        newLog.pop()
        newLog.push({
            message: response.data.sessionID && !response.data.classInfo ? response.data.text : response.data,
            sender: "ai",
            loading: false,
            sessionID: response.data.sessionID
        })
        if(response.data.classInfo)
            newLog.push({
                message: "These are some relevant classes. Which classes do you want to learn more about?",
                sender: "ai",
                loading: false,
                sessionID:response.data.sessionId
            })
        return newLog
    })
    updateWaiting(false)
}

export default newRequest