import React, { Children } from 'react';
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
import Grid from '@material-ui/core/Grid';
import StarIcon from '@material-ui/icons/Star';
import HorizontalSplitIcon from '@material-ui/icons/HorizontalSplit';
import FiberManualRecordIcon from '@material-ui/icons/FiberManualRecord';
import GraphicEqIcon from '@material-ui/icons/GraphicEq';
import ShowChartIcon from '@material-ui/icons/ShowChart';

const styles = theme => ({
  root: {
    width: '100%',
    padding: '10px',
    overflow: 'auto',
  },
  paper: {
    padding: "5px",
    height: "100px",
    width: "100%",
    display: "inherit",
  },
  largeIcon: {
    width: 50,
    height: 50,
    marginBottom: "-20px",
  },
});

class DJTab extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      'songList': {},
      'open': false,
      'addSong': '',
      'currSong': '',
      'newName': ''
    };
  }

  render() {
    const { classes } = this.props;

    const handleClick = (value) => () => {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", 'http://' + process.env.REACT_APP_IP + ':5000/api/DJ/' + value, true);
        xhr.send(null);
    };

    var val = 4;

    var mappings = {
        "sparkle": <StarIcon className={classes.largeIcon}/>,
        "bars": <HorizontalSplitIcon className={classes.largeIcon}/>,
        "circle": <FiberManualRecordIcon className={classes.largeIcon}/>,
        "diamond": <GraphicEqIcon className={classes.largeIcon}/>,
        "wave": <ShowChartIcon className={classes.largeIcon}/>,
    };

    return (
      <div className={classes.root}>
        <Grid container spacing={2}>
            {Object.keys(mappings).map((key) => (
                <Grid item xs={val}>
                    <Button
                        variant="contained"
                        color="primary"
                        className={classes.paper}
                        onClick={handleClick(key)}
                    >
                        {mappings[key]}
                        <p />
                        {key}
                    </Button>
                </Grid>
            ))}
        </Grid>
      </div>
    );
  }
}
export default withStyles(styles)(DJTab);