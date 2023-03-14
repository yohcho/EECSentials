import axios from "axios"

const newRequest= async(message)=>{
    const config = {
        method: 'get',
        url: 'http://localhost:5000/api/getResponse',
        params: {
            message:message
        }
    }
    const response = await axios(config)
    return response.data.message
}

export default newRequest