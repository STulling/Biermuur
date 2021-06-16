taskkill /IM "node.exe" /F
cd frontend
start /b cmd /c npm start
cd ../backend
python main.py .
