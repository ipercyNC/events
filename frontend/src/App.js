/*
 * App.js
 * 7/19/2023
 * Ian Percy
 * 
 * 
 * Main view for the application. Entry point and renderer 
 */
import axios from "axios";
import React, { useEffect, useState } from "react";
import Header from "./components/Header"
import Events from "./components/Events"
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import Input from '@mui/material/Input';
import InputLabel from '@mui/material/InputLabel';
import Divider from '@mui/material/Divider';

function App() {
  // Set the user object, username, and password state variables
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  //On page load, check session storage for user
  useEffect(() => {
    if (sessionStorage.getItem("user") !== null) {
      setUser(JSON.parse(sessionStorage.getItem("user")))
    }
  }, [])

  /*
  * Handle login, calls backend with the saved username and password
  *
  * @param null
  * @return null
  */
  function handleLogin() {
    if (!validate()){
      window.alert("Please enter valid username and password")
      return
    }
    axios.post("/users/login",
      {
        "username": username,
        "password": password
      })
      .then(response => {
        // console.log("User logged in", response)
        setUser(response.data.data)
        sessionStorage.setItem("user", JSON.stringify(response.data.data));
      }).catch(err => {
        console.log(err.response.data);
        window.alert(err.response.data.message)
      })
  }

  /*
  * Handle logout, calls backend to unset the cookies
  *
  * @param null
  * @return null
  */
  function handleLogout() {
    axios.post("/users/logout")
      .then(response => {
        // console.log("User logged out", response)
        setUser(null)
        sessionStorage.removeItem("user");
      }).catch(err => {
        console.log(err.response.data);
        window.alert(err.response.data.message)
      })
  }

  /*
  * Handle register, calls backend with the saved username and password
  *
  * @param null
  * @return null
  */
  function handleRegister() {
    if (!validate()){
      window.alert("Please enter valid username and password")
      return
    }
    axios.post("/users/register",
      {
        "username": username,
        "password": password
      })
      .then(response => {
        // console.log("User registered", response)
        setUser(response.data.data)
        sessionStorage.setItem("user", JSON.stringify(response.data.data));
      }).catch(err => {
        console.log(err.response.data);
        window.alert(err.response.data.message)
      })
  }

  /*
  * Handle validate input for username and password
  *
  * @param null
  * @return null
  */
  function validate() {
    if (!username || username.length > 30 || !password || password.length > 30){
      return false
    }
    return true
  }
  return (
    <div>
      <Header user={user} handleLogin={handleLogin} setUser={setUser} handleLogout={handleLogout} />
      {user ?
        <Events user={user} /> :
        <Box
          component="form"
          sx={{
            '& > :not(style)': { m: 1 },
            alignItems: "center",
            justifyContent: "center",
            display: "flex",
            width: "100vw"
          }}
          noValidate
          autoComplete="off"
        >
          <Typography variant="h5" component="div" align="center" sx={{ height: 38 }}>
            Please Log In Or Register
          </Typography>
          <Divider />
          <FormControl variant="standard">
            <InputLabel htmlFor="username">Username</InputLabel>
            <Input id="username" value={username} onChange={(e) => setUsername(e.target.value)} />
          </FormControl>
          <FormControl variant="standard">
            <InputLabel htmlFor="password">Password</InputLabel>
            <Input id="password" value={password} type="password" onChange={(e) => setPassword(e.target.value)} />
          </FormControl>
          <Button onClick={handleLogin} color="inherit" variant="outlined" size="large" sx={{
            height: 38
          }}>Login</Button>
          <Button onClick={handleRegister} color="inherit" variant="outlined" sx={{
            height: 38
          }}>Register</Button>
        </Box>
      }
    </div>
  );
}

export default App;
