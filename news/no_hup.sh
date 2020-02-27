#nohup python bobae.py 1>/dev/null/ 2>&1 &
service mysql start
nohup python crawling.py 1>/dev/null/ 2>&1 &
echo "service mysql start"
echo "nohup python crawling.py &"
