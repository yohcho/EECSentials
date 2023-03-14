const express = require('express')
const dotenv = require('dotenv')
const cors = require('cors')

const routes = require('./apis/classes')

const app = express()
app.use(express.json())
dotenv.config()

app.use(cors({origin:'*'}));
app.use('/api', routes)

app.listen(5000, () => {});