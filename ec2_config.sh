# to ssh into instance, ssh -i "sruti-uw.pem" ec2-user@ec2-13-59-74-208.us-east-2.compute.amazonaws.com
# to configure aws credentials, aws configure
sudo yum install git
git clone -b dev https://github.com/SrutiG/uw_database.git
cd uw_database
pip install --user -r requirements.txt
nohup python run.py --host 0.0.0.0 > uw_database.out 2>&1 &
# to kill process, get process id using command
# ps -ef | grep nohup
# then kill process
# kill <pid>