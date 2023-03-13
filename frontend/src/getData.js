import axios from "axios"

const getData = async()=>{
    const config = {
        method: 'get',
        url: 'http://localhost:5000/api/getData'
    }
    const res = await axios(config)
    const data = new Map(res.data.data.map(item=> [item.name, {
        availability:item.availability,
        _id:item._id
    }]))
    return data
}

export default getData