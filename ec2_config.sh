# to ssh into instance, ssh -i "sruti-uw.pem" ec2-user@ec2-13-59-74-208.us-east-2.compute.amazonaws.com
# to configure aws credentials, aws configure
sudo yum install git
git clone -b dev https://github.com/SrutiG/uw_database.git
cd uw_database
pip install --user -r requirements.txt
nohup python run.py --host 0.0.0.0 > uw_database.out 2>&1 &
# route port 80 to port 8090 (http)
sudo iptables -A INPUT -i eth0 -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -i eth0 -p tcp --dport 8090 -j ACCEPT
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8090
# route port 443 to port 8090 (https)
sudo iptables -A INPUT -i eth0 -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -i eth0 -p tcp --dport 8090 -j ACCEPT
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 8090
# to kill process, get process id using command
# ps -ef | grep nohup
# then kill process
# kill <pid>

