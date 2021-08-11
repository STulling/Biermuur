import React from 'react';
import { withStyles } from '@material-ui/styles';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import StarIcon from '@material-ui/icons/Star';
import HorizontalSplitIcon from '@material-ui/icons/HorizontalSplit';
import FiberManualRecordIcon from '@material-ui/icons/FiberManualRecord';
import GraphicEqIcon from '@material-ui/icons/GraphicEq';
import ShowChartIcon from '@material-ui/icons/ShowChart';
import MoodIcon from '@material-ui/icons/Mood';
import StopIcon from '@material-ui/icons/Stop';

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
        "mond": <MoodIcon className={classes.largeIcon}/>,
        "fill": <StopIcon className={classes.largeIcon}/>,
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