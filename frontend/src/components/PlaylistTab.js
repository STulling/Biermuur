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
  }
});

class PlaylistTab extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      'playlistList': {},
      'open': false,
      'addPlaylist': '',
      'currPlaylist': '',
      'newName': '',
      'currPlaylistSongs': []
    };
  }

  componentDidMount() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/playlists', true);

    xhr.onload = function () {
      var playlistList = {}
      var songs = JSON.parse(xhr.responseText)
      songs.sort()
      var chars = songs.map(x => x[0].toUpperCase())
      var unique = [...new Set(chars)];
      for (const char of unique) {
        playlistList[char] = []
        for (const song of songs) {
          if (song[0].toUpperCase() == char) {
            playlistList[char].push(song);
          }
        }
      }
      this.setState({'playlistList': playlistList});
    }.bind(this);
    
    xhr.send(null);
  }

  render() {
    const { classes } = this.props;

    const handleClickOpen = () => {
      this.setState({'songaddOpen': true });
    };

    const play = (playlistName) => {
      var xhr = new XMLHttpRequest();
      xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/playlists/play/' + playlistName, true);
      
      xhr.send(null);
    };

    const refresh = () => {
      var xhr = new XMLHttpRequest();
      xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/playlists', true);

      xhr.onload = function () {
        var playlistList = {}
        var songs = JSON.parse(xhr.responseText)
        songs.sort()
        var chars = songs.map(x => x[0].toUpperCase())
        var unique = [...new Set(chars)];
        for (const char of unique) {
          playlistList[char] = []
          for (const song of songs) {
            if (song[0].toUpperCase() == char) {
              playlistList[char].push(song);
            }
          }
        }
        this.setState({'playlistList': playlistList});
      }.bind(this);
      
      xhr.send(null);
    }

    const handleClickSettingsOpen = (song) => {
      this.setState({'playlistsettingsOpen': true, 'currPlaylist': song });
      var xhr = new XMLHttpRequest();
      xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/playlists/get/' + song, true);

      xhr.onload = function () {
        var playlistList = {}
        var songs = JSON.parse(xhr.responseText)
        songs.sort()
        this.setState({'currPlaylistSongs': songs});
      }.bind(this);
      
      xhr.send(null);
    };

    const handleClose = () => {
      this.setState({'songaddOpen': false });
      this.setState({'playlistsettingsOpen': false });
    };

    const changeAddPlaylist = (e) => {
      this.setState({'addPlaylist': e.target.value });
    };

    const changecurrPlaylistName = (e) => {
      this.setState({'newName': e.target.value });
    };

    const addPlaylist = () => {
      var xhr = new XMLHttpRequest();
      xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/playlists/new/' + this.state.addPlaylist, true);
      
      xhr.send(null);
      handleClose();
      refresh()
    };

    const editPlaylist = () => {
      var xhr = new XMLHttpRequest();
      xhr.open("PUT", 'http://' + process.env.REACT_APP_IP + ':5000/api/playlists/rename/' + this.state.currPlaylist, true);
      xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      
      xhr.send('data=' + encodeURIComponent(this.state.newName));
      handleClose();
      refresh()
    };

    const removePlaylist = () => {
      var xhr = new XMLHttpRequest();
      xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/playlists/destroy/' + this.state.currPlaylist, true);
      
      xhr.send(null);
      handleClose();
      refresh()
    };

    return (
      <div className={classes.root}>
        <List>
          {Object.keys(this.state.playlistList).map((sectionId) => (
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
                {this.state.playlistList[sectionId].map((item) => {
                  if (this.state.playlistList[sectionId].indexOf(item) == 0) {
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
          <DialogTitle id="simple-dialog-title">Add playlist</DialogTitle>
          <DialogContent>
            <TextField id="song-title" label="Playlist Title" variant="outlined" onChange={changeAddPlaylist}/>
          </DialogContent>
          <DialogActions>
            <Button variant="contained" color="primary" onClick={addPlaylist}>
              Add
            </Button>
          </DialogActions>
        </Dialog>
        <Dialog aria-labelledby="simple-dialog-title" open={this.state.playlistsettingsOpen} onClose={handleClose}>
          <DialogContent>
            <TextField id="song-title" label="New Song Title" variant="outlined" onChange={changecurrPlaylistName}/>
          </DialogContent>
          <DialogActions>
            <Button variant="contained" color="primary" onClick={editPlaylist}>
              Edit
            </Button>
            <Button variant="contained" color="secondary" onClick={removePlaylist}>
              Delete
            </Button>
          </DialogActions>
          <DialogContent>
            <List>
              {Object.values(this.state.currPlaylistSongs).map((name) => (
              <ListItem>
                <Paper>
                  {name}
                </Paper>
              </ListItem>
              ))}
            </List>
          </DialogContent>
        </Dialog>
      </div>
    );
  }
}
export default withStyles(styles)(PlaylistTab);