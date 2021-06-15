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
import { withStyles } from '@material-ui/styles';
import Button from '@material-ui/core/Button';
import UpdateIcon from '@material-ui/icons/Update';

const styles = theme => ({
  root: {
    width: '100%',
  },
});

class SettingsTab extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      'primary': '',
      'secondary': '',
    };
  }

  render() {
    const { classes } = this.props;

    const handleToggle = (value) => () => {
      var xhr = new XMLHttpRequest();
      xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/common/' + value, true);
      xhr.send(null);
    };

    const changeColor = (type) => (e) => {
      var out = {}
      out[type] = e.css.backgroundColor
      this.setState(out)
      var xhr = new XMLHttpRequest();
      xhr.open("PUT", 'http://' + process.env.REACT_APP_IP + ':5000/api/settings/' + type, true);
      xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      
      xhr.send('data=' + encodeURIComponent(e.css.backgroundColor));
    };

    return (
      <div className={classes.root}>
        <List subheader={<ListSubheader>Colors</ListSubheader>}>
          <ListItem>
            <ListItemIcon>
              <PaletteIcon />
            </ListItemIcon>
            <ColorPicker
              defaultValue='#FF0000' disablePlainColor onChange={changeColor("primary")} value={this.state.primary}
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <PaletteIcon />
            </ListItemIcon>
            <ColorPicker
              defaultValue='#00FF00' disablePlainColor onChange={changeColor("secondary")} value={this.state.secondary}
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
              <PaletteIcon />
            </ListItemIcon>
            <TextField id="show-text" label="Buffer size" />
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
        <List subheader={<ListSubheader>Advanced</ListSubheader>}>
          <ListItem>
            <ListItemIcon>
              <UpdateIcon />
            </ListItemIcon>
            <ListItemText primary="Update" />
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
        <List subheader={<ListSubheader>Info</ListSubheader>}>
          <ListItem>
            <ListItemText primary={"Debug button"} />
          </ListItem>
          <ListItemSecondaryAction>
              <Button
                  color="primary"
                  variant="contained"
                  onClick={() => console.log(process.env)}
                >
                <SendIcon />
              </Button>
            </ListItemSecondaryAction>
        </List>
      </div>
    );
  }
}

export default withStyles(styles)(SettingsTab);