import React from 'react';
import Paper from '@material-ui/core/Paper';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import { makeStyles } from '@material-ui/core/styles';
import EmojiObjectsIcon from '@material-ui/icons/EmojiObjects';
import SettingsIcon from '@material-ui/icons/Settings';
import MusicNoteIcon from '@material-ui/icons/MusicNote';
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';
import MainTab from './components/MainTab';
import SettingsTab from './components/SettingsTab';
import MusicTab from './components/MusicTab';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

function App() {
  const classes = useStyles();
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const clear = () => {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", 'http://localhost:5000/api/common/clear', true);
    xhr.send(null);
  };

  return (
  <div className={classes.root}>
    <AppBar position="sticky">
      <Toolbar>
        <Typography variant="h6" className={classes.title}>
          Biermuur
        </Typography>
        <IconButton color="inherit">
          <DeleteForeverIcon onClick={clear}/>
        </IconButton>
      </Toolbar>
    </AppBar>
    {value === 0 && <MainTab />}
    {value === 1 && <MusicTab />}
    {value === 2 && <SettingsTab />}
    <Paper square style={{ position: 'fixed', bottom: '0px', width: '100%'}}>
      <Tabs
        value={value}
        onChange={handleChange}
        variant="fullWidth"
        indicatorColor="primary"
        textColor="primary"
        aria-label="icon tabs example"
      >
        <Tab icon={<EmojiObjectsIcon />} label="MODES" />
        <Tab icon={<MusicNoteIcon />} label="MUSIC" />
        <Tab icon={<SettingsIcon />} label="SETTINGS" />
      </Tabs>
    </Paper>
  </div>);
}

export default App;
