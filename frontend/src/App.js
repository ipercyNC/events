import axios from "axios";
import React, { useEffect, useState, useReducer, createContext } from "react";
import Header from "./components/Header"
import Events from "./components/Events"
import Cookies from 'js-cookie';

function App() {
  const [user, setUser] = useState(null);

  function handleLogin() {
    axios.post("/users/login", 
      {"username": "guest", 
       "password": "test"})
       .then(response => {
        console.log("logged in", response)
        setUser(response.data)
       })
  }
  function handleLogout() {
    
    axios.post("/users/logout")
     .then(response => {
      console.log("logged out", response)
      setUser(null)
     })
  }

  return (
    <div>
      <Header user={user} handleLogin={handleLogin} setUser={setUser} handleLogout={handleLogout}/>
      {user ? <Events />: <div>Please Log In!</div>}
    </div>
  );
}

export default App;
