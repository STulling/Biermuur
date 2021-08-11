sudo pkill -f node
export REACT_APP_IP=192.168.1.5
export FLASK_MEDIA_DIR=/media/usb/music
cd frontend
npm start &
cd ../backend
python3 main.py