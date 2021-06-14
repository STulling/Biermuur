import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/styles';
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
    marginBottom: '-45px',
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
  fab: {
    position: 'fixed',
    right: '10px',
    bottom: '80px',
  }
});

class MainTab extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      'songList': {},
      'open': false
    };
  }

  componentDidMount() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", 'http://localhost:5000/api/songs', true);

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
  }

  render() {
    const { classes } = this.props;

    const handleClickOpen = () => {
      this.setState({'open': true });
    };

    const handleClose = () => {
      this.setState({'open': false });
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
                {this.state.songList[sectionId].map((item) => (
                  <ListItem button key={`item-${sectionId}-${item}`}>
                    <ListItemText className={classes.songName} inset primary={`${item}`} />
                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="comments">
                        <MenuIcon />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </ul>
            </li>
          ))}
        </List>
        <Fab color="primary" aria-label="add" className={classes.fab} onClick={handleClickOpen}>
          <AddIcon />
        </Fab>
        <Dialog aria-labelledby="simple-dialog-title" open={this.state.open} onClose={handleClose}>
          <DialogTitle id="simple-dialog-title">Add song</DialogTitle>
          <DialogContent>
            <TextField id="song-title" label="Song Title" variant="outlined" />
          </DialogContent>
          <DialogActions>
            <Button variant="contained" color="primary">
              Add
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}
export default withStyles(styles)(MainTab);