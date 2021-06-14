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
import SendIcon from '@material-ui/icons/Send';
import WifiIcon from '@material-ui/icons/Wifi';
import CasinoIcon from '@material-ui/icons/Casino';
import BluetoothIcon from '@material-ui/icons/Bluetooth';
import TextField from '@material-ui/core/TextField';
import PaletteIcon from '@material-ui/icons/Palette';
import { ColorPicker } from 'material-ui-color';

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
      <List subheader={<ListSubheader>Colors</ListSubheader>}>
        <ListItem>
          <ListItemIcon>
            <PaletteIcon />
          </ListItemIcon>
          <ColorPicker
            defaultValue='#FF0000' disablePlainColor
          />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <PaletteIcon />
          </ListItemIcon>
          <ColorPicker
            defaultValue='#00FF00' disablePlainColor
          />
        </ListItem>
      </List>
      <List subheader={<ListSubheader>Audio</ListSubheader>}>
        <ListItem>
          <ListItemIcon>
            <PaletteIcon />
          </ListItemIcon>
          <TextField id="show-text" label="Block size" />
          <ListItemSecondaryAction>
            <IconButton
              color="primary"
              onClick={handleToggle('wifi')}
            >
              <SendIcon />
            </IconButton>
          </ListItemSecondaryAction>
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <PaletteIcon />
          </ListItemIcon>
          <TextField id="show-text" label="Buffer size" />
          <ListItemSecondaryAction>
            <IconButton
              color="primary"
              onClick={handleToggle('wifi')}
            >
              <SendIcon />
            </IconButton>
          </ListItemSecondaryAction>
        </ListItem>
      </List>
    </div>
  );
}

export default MainTab;