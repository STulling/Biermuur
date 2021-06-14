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
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
  },
  ul: {
    padding: 0,
  },
  icon: {
    position: 'sticky',
    top: '60px',
    marginBottom: '-45px',
  },
  label: {
    minWidth: '0px',
    width: '30px',
    height: '30px',
    borderRadius: "5em",
  },
}));

function MainTab() {
  const classes = useStyles();

  const handleToggle = (value) => () => {
    console.log(value)
  };

  return (
    <div className={classes.root}>
      <List>
        {['A', 'B', 'C', 'D', 'E', 'F', 'G'].map((sectionId) => (
          <li key={`section-${sectionId}`} className={classes.listSection}>
            <ul className={classes.ul}>
              <ListItem className={classes.icon}>
                <ListItemIcon>
                  <Button className={classes.label} variant="contained" disabled>
                    {sectionId}
                  </Button>
                </ListItemIcon>
              </ListItem>
              {[0, 1, 2].map((item) => (
                <ListItem button key={`item-${sectionId}-${item}`}>
                  <ListItemText inset primary={`Item ${item}`} />
                </ListItem>
              ))}
            </ul>
          </li>
        ))}
      </List>
    </div>
  );
}

export default MainTab;