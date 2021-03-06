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
import PowerSettingsNewIcon from '@material-ui/icons/PowerSettingsNew';
import SkipNextIcon from '@material-ui/icons/SkipNext';
import MainTab from './components/MainTab';
import SettingsTab from './components/SettingsTab';
import PlaylistTab from './components/PlaylistTab';
import MusicTab from './components/MusicTab';
import DJTab from './components/DJTab';
import AlbumIcon from '@material-ui/icons/Album';

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
    xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/common/stop', true);
    xhr.send(null);
  };

  const skip = () => {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/common/skip', true);
    xhr.send(null);
  };

  return (
  <div className={classes.root}>
    <AppBar position="sticky">
      <Toolbar>
        <Typography variant="h6" className={classes.title}>
          Biermuur 2.0
        </Typography>
        <IconButton color="inherit">
          <SkipNextIcon onClick={skip}/>
        </IconButton>
        <IconButton color="inherit">
          <PowerSettingsNewIcon onClick={clear}/>
        </IconButton>
      </Toolbar>
    </AppBar>
    {value === 0 && <MusicTab />}
    {value === 1 && <PlaylistTab />}
    {value === 2 && <DJTab />}
    {value === 3 && <MainTab />}
    {value === 4 && <SettingsTab />}
    <Paper square style={{ position: 'fixed', bottom: '0px', width: '100%'}}>
      <Tabs
        value={value}
        onChange={handleChange}
        variant="fullWidth"
        indicatorColor="primary"
        textColor="primary"
        aria-label="icon tabs example"
      >
        <Tab icon={<MusicNoteIcon />} label="MUSIC" />
        <Tab icon={<AlbumIcon />} label="PLAYLISTS" />
        <Tab icon={<AlbumIcon />} label="DJ" />
        <Tab icon={<EmojiObjectsIcon />} label="MODES" />
        <Tab icon={<SettingsIcon />} label="SETTINGS" />
      </Tabs>
    </Paper>
  </div>);
}

export default App;
