import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/styles';
import IconButton from '@material-ui/core/IconButton';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';
import MenuIcon from '@material-ui/icons/Menu';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';

import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import Divider from '@material-ui/core/Divider';

const styles = theme => ({
  root: {
    width: '100%',
    paddingBottom: '100px',
  },
  ul: {
    padding: 0,
  },
  icon: {
    position: 'sticky',
    top: '60px',
    //marginBottom: '-45px',
  },
  label: {
    minWidth: '0px',
    width: '30px',
    height: '30px',
    borderRadius: "5em",
  },
  labelText: {
    textAlign: 'center',
  },
  songName: {
    textAlign: 'left',
    whiteSpace: "nowrap",
    overflow: 'hidden',
  },
  firstItem: {
    marginTop: '-45px',
  },
  fab: {
    position: 'fixed',
    right: '10px',
    bottom: '80px',
  },
  diaActions: {
    alignSelf: 'center',
  },
  select: {
    width: '200px',
  }
});

class MusicTab extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      'songList': {},
      'open': false,
      'addSong': '',
      'currSong': '',
      'newName': '',
      'chosenPlaylist': '',
      'playlistList': []
    };
  }

  componentDidMount() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/songs', true);

    xhr.onload = function () {
      var songList = {}
      var songs = JSON.parse(xhr.responseText)
      songs.sort()
      var chars = songs.map(x => x[0].toUpperCase())
      var unique = [...new Set(chars)];
      for (const char of unique) {
        songList[char] = []
        for (const song of songs) {
          if (song[0].toUpperCase() == char) {
            songList[char].push(song);
          }
        }
      }
      this.setState({'songList': songList});
    }.bind(this);
    
    xhr.send(null);

    var xhr2 = new XMLHttpRequest();
    xhr2.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/playlists', true);

    xhr2.onload = function () {
      var playlistList = {}
      var songs = JSON.parse(xhr2.responseText)
      songs.sort()
      this.setState({'playlistList': songs});
    }.bind(this);
    
    xhr2.send(null);
  }

  render() {
    const { classes } = this.props;

    const handleChange = (event) => {
      this.setState({'chosenPlaylist': event.target.value});
    };

    const handleClickOpen = () => {
      this.setState({'songaddOpen': true });
    };

    const play = (songName) => {
      var xhr = new XMLHttpRequest();
      xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/songs/play/' + songName, true);
      
      xhr.send(null);
    };

    const handleClickSettingsOpen = (song) => {
      this.setState({'songsettingsOpen': true, 'currSong': song });
    };

    const handleClose = () => {
      this.setState({'songaddOpen': false });
      this.setState({'songsettingsOpen': false });
    };

    const changeAddSong = (e) => {
      this.setState({'addSong': e.target.value });
    };

    const changeCurrSongName = (e) => {
      this.setState({'newName': e.target.value });
    };

    const addSong = () => {
      var xhr = new XMLHttpRequest();
      xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/songs/add/' + this.state.addSong, true);
      
      xhr.send(null);
      handleClose();
    };

    const addSongToPlaylist = () => {
      var xhr = new XMLHttpRequest();
      xhr.open("PUT", 'http://' + process.env.REACT_APP_IP + ':5000/api/playlists/add/' + this.state.chosenPlaylist, true);
      xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      
      xhr.send('data=' + encodeURIComponent(this.state.currSong));
      handleClose();
    };

    const removeSongFromPlaylist = () => {
      var xhr = new XMLHttpRequest();
      xhr.open("PUT", 'http://' + process.env.REACT_APP_IP + ':5000/api/playlists/remove/' + this.state.chosenPlaylist, true);
      xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      
      xhr.send('data=' + encodeURIComponent(this.state.currSong));
      handleClose();
    };

    const editSong = () => {
      var xhr = new XMLHttpRequest();
      xhr.open("PUT", 'http://' + process.env.REACT_APP_IP + ':5000/api/songs/' + this.state.currSong, true);
      xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      
      xhr.send('data=' + encodeURIComponent(this.state.newName));
      handleClose();
    };

    const removeSong = () => {
      var xhr = new XMLHttpRequest();
      xhr.open("DELETE", 'http://' + process.env.REACT_APP_IP + ':5000/api/songs/' + this.state.currSong, true);
      
      xhr.send(null);
      handleClose();
    };

    return (
      <div className={classes.root}>
        <List>
          {Object.keys(this.state.songList).map((sectionId) => (
            <li key={`section-${sectionId}`} className={classes.listSection}>
              <ul className={classes.ul}>
                <ListItem className={classes.icon}>
                  <ListItemIcon>
                    <Paper className={classes.label}>
                      <Typography variant="h6" className={classes.labelText}>
                        {sectionId}
                      </Typography>
                    </Paper>
                  </ListItemIcon>
                </ListItem>
                {this.state.songList[sectionId].map((item) => {
                  if (this.state.songList[sectionId].indexOf(item) == 0) {
                  return (
                    <ListItem className={classes.firstItem} button key={`item-${sectionId}-${item}`} onClick={() => play(item)}>
                      <ListItemText className={classes.songName} inset primary={`${item}`}/>
                      <ListItemSecondaryAction>
                        <IconButton edge="end" aria-label="comments" onClick={() => handleClickSettingsOpen(item)}>
                          <MenuIcon />
                        </IconButton>
                      </ListItemSecondaryAction>
                    </ListItem>
                  )} else { return (
                    <ListItem button key={`item-${sectionId}-${item}`} onClick={() => play(item)}>
                      <ListItemText className={classes.songName} inset primary={`${item}`} />
                      <ListItemSecondaryAction>
                        <IconButton edge="end" aria-label="comments" onClick={() => handleClickSettingsOpen(item)}>
                          <MenuIcon />
                        </IconButton>
                      </ListItemSecondaryAction>
                    </ListItem>
                  )}})
                }
              </ul>
            </li>
          ))}
        </List>
        <Fab color="primary" aria-label="add" className={classes.fab} onClick={handleClickOpen}>
          <AddIcon />
        </Fab>
        <Dialog aria-labelledby="simple-dialog-title" open={this.state.songaddOpen} onClose={handleClose}>
          <DialogTitle id="simple-dialog-title">Add song</DialogTitle>
          <DialogContent>
            <TextField id="song-title" label="Song Title" variant="outlined" onChange={changeAddSong}/>
          </DialogContent>
          <DialogActions>
            <Button variant="contained" color="primary" onClick={addSong}>
              Add
            </Button>
          </DialogActions>
        </Dialog>
        <Dialog aria-labelledby="simple-dialog-title" open={this.state.songsettingsOpen} onClose={handleClose}>
          <DialogContent>
            <TextField id="song-title" label="New Song Title" variant="outlined" onChange={changeCurrSongName}/>
          </DialogContent>
          <DialogActions className={classes.diaActions}>
            <Button variant="contained" color="primary" onClick={editSong}>
              Edit
            </Button>
            <Button variant="contained" color="secondary" onClick={removeSong}>
              Delete
            </Button>
          </DialogActions>
          <DialogActions className={classes.diaActions}>
            <Select
              className={classes.select}
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              onChange={handleChange}
            >
              {Object.values(this.state.playlistList).map((name) => (
                <MenuItem value={name}>{name}</MenuItem>
              ))}
            </Select>
          </DialogActions>
          <DialogActions className={classes.diaActions}>
          <Button variant="contained" color="primary" onClick={addSongToPlaylist}>
              Add
            </Button>
            <Button variant="contained" color="secondary" onClick={removeSongFromPlaylist}>
              Remove
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}
export default withStyles(styles)(MusicTab);