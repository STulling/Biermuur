export REACT_APP_IP=$1
cd frontend
npm start &
cd ../backend
python main.py $2
