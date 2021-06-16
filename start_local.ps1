taskkill /IM "node.exe" /F
$env:REACT_APP_IP = "localhost"
$env:FLASK_MEDIA_DIR = "."
cd frontend
Start-Process npm start
cd ../backend
python main.py .