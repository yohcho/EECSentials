import axios from "axios"

const newRequest= async(message,updateLog,updateWaiting)=>{
    const config = {
        method: 'get',
        url: 'https://wpr4bkssk4td4csrd5yxm667iq0pcbmj.lambda-url.us-east-2.on.aws/',
        params: {
            message:message
        }
    }
    const response = await axios(config)
    updateLog(prevLog=>{
        const newLog = [...prevLog]
        newLog.pop()
        newLog.push({
            message: response.data,
            sender: "ai",
            loading: false
        })
        return newLog
    })
    updateWaiting(false)
}

export default newRequest