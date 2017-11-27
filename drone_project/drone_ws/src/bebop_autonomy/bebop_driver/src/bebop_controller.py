#!/usr/bin/env python
import rospy
import os 
from std_msgs.msg import String
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from ftplib import FTP

def camera_control():
	files=[]
	msg = Twist()
	pub = rospy.Publisher('camera_control', Twist, queue_size=10)
	rospy.init_node('controller', anonymous=True)
	rate = rospy.Rate(.2) # 10hz

	i = 0
	while not rospy.is_shutdown():
		i = i+1
		if(i%2==0):
			msg.angular.y = -25
        		msg.angular.z = 0
		else:
			msg.angular.y = 25
        		msg.angular.z = 0
		pub.publish(msg)

		ftp = FTP('192.168.42.1')
		ftp.login()
		ftp.cwd('internal_000/Bebop_2/media')
		ftp.dir('-t',files.append)
		fileForCVInfo=files[len(files)-1].split()
		fileForCV=fileForCVInfo[len(fileForCVInfo) - 1]
		ftp.retrbinary('RETR %s' % fileForCV, open('%s/%s' % (os.path.dirname(os.path.realpath(__file__)), fileForCV), 'wb').write)
		rospy.logwarn(str(fileForCV))
		
 		rate.sleep()
	ftp.quit()

if __name__ == '__main__':
	try:
		camera_control()
	except rospy.ROSInterruptException:
		pass
