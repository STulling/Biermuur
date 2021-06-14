import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import Divider from '@material-ui/core/Divider';
import TextFieldsIcon from '@material-ui/icons/TextFields';
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';
import SendIcon from '@material-ui/icons/Send';
import WifiIcon from '@material-ui/icons/Wifi';
import CasinoIcon from '@material-ui/icons/Casino';
import BluetoothIcon from '@material-ui/icons/Bluetooth';
import TextField from '@material-ui/core/TextField';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
  },
}));

function MainTab() {
  const classes = useStyles();

  const handleToggle = (value) => () => {
    console.log(value)
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
      </List>
    </div>
  );
}

export default MainTab;