import axios from "axios";
import React, { useEffect, useState, useReducer, createContext } from "react";
import Header from "./components/Header"
import Events from "./components/Events"
import Cookies from 'js-cookie';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { Theme } from "@material-ui/core/styles";
import FilledInput from '@mui/material/FilledInput';
import FormControl from '@mui/material/FormControl';
import FormHelperText from '@mui/material/FormHelperText';
import Input from '@mui/material/Input';
import InputLabel from '@mui/material/InputLabel';
import Divider from '@mui/material/Divider';

function App() {
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  useEffect(() => {
    if (sessionStorage.getItem("user") !== null) {

      setUser(JSON.parse(sessionStorage.getItem("user")))
    }
  }, [])

  function handleLogin() {
    axios.post("/users/login",
      {
        "username": username,
        "password": password
      })
      .then(response => {
        console.log("logged in", response)
        setUser(response.data.user)
        sessionStorage.setItem("user", JSON.stringify(response.data.user));
      })
  }
  function handleLogout() {

    axios.post("/users/logout")
      .then(response => {
        console.log("logged out", response)
        setUser(null)
        sessionStorage.removeItem("user");
      })
  }
  function handleRegister() {
    axios.post("/users/register",
      {
        "username": username,
        "password": password
      })
      .then(response => {
        console.log("registered", response)
        setUser(response.data.user)
        sessionStorage.setItem("user", JSON.stringify(response.data.user));
      })
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
            <Input id="password" value={password} onChange={(e) => setPassword(e.target.value)} />
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
