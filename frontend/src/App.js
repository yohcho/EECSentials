import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/home";
import Chat from "./pages/chat";

import "./App.css"

function App() {   
    return(
      <BrowserRouter>
        <Routes>
          <Route index element={<Home/>}/>
          <Route path="chat" element={<Chat/>}/>
        </Routes>
      </BrowserRouter>
    )
  }

export default App;
