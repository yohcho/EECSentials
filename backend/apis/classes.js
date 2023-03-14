const express = require('express')
const router  = express.Router()

router.get('/getResponse', (req,res)=>{
    const message = req.query.message
    res.status(200).json({message:"Dummy response"})
})

module.exports = router