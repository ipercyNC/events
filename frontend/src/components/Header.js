import { useContext } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import UserContext from '../App'

export default function Header({ user, setUser, handleLogin, handleLogout }) {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Events
          </Typography>
          {user ?
              <>
              <Typography variant="subtitle1" component="div" sx={{ align: "right", paddingRight:2}}>
                Welcome: {user.message} 
              </Typography>
              <Button onClick={() => handleLogout()} color="inherit" sx={{ align: "right"}}>LogOut</Button>
              </>
             :
            <Button onClick={() => handleLogin()} color="inherit">Login</Button>
          }

        </Toolbar>
      </AppBar>
    </Box>
  );
}