import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import TextFieldsIcon from '@material-ui/icons/TextFields';
import Button from '@material-ui/core/Button';
import SendIcon from '@material-ui/icons/Send';
import CasinoIcon from '@material-ui/icons/Casino';
import TextField from '@material-ui/core/TextField';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
  },
}));

function MainTab() {
  const classes = useStyles();

  const handleToggle = (value) => () => {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/common/' + value, true);
    
    xhr.send(null);
    handleClose();
  };

  return (
    <div className={classes.root}>
      <List subheader={<ListSubheader>Text</ListSubheader>}>
        <ListItem>
          <ListItemIcon>
            <TextFieldsIcon />
          </ListItemIcon>
          <TextField id="show-text" label="Set Text" />
          <ListItemSecondaryAction>
            <Button
              color="primary"
              variant="contained"
              onClick={handleToggle('wifi')}
            >
              <SendIcon />
            </Button>
          </ListItemSecondaryAction>
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <CasinoIcon />
          </ListItemIcon>
          <ListItemText primary="Random Text" />
          <ListItemSecondaryAction>
            <Button
                color="primary"
                variant="contained"
                onClick={handleToggle('wifi')}
              >
              <SendIcon />
            </Button>
          </ListItemSecondaryAction>
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <CasinoIcon />
          </ListItemIcon>
          <ListItemText primary="Dobbelsteen" />
          <ListItemSecondaryAction>
            <Button
                color="primary"
                variant="contained"
                onClick={handleToggle('dobbelsteen')}
              >
              <SendIcon />
            </Button>
          </ListItemSecondaryAction>
        </ListItem>
      </List>
    </div>
  );
}

export default MainTab;