#!/usr/bin/env python
import rospy
import os 
from std_msgs.msg import String
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from sensor_msgs.msg import NavSatFix
from ftplib import FTP

global latit
global longit

class Controller:

	def callback(self, data):
		self.latit = data.longitude
		self.longit = data.latitude
		self.altit = data.altit

	def camera_control(self):
		files=[]
		msg = Twist()
		msg_snapshot = Empty()
		pub = rospy.Publisher('camera_control', Twist, queue_size=10)
		pub_snapshot = rospy.Publisher('snapshot', Empty, queue_size=10)

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

			pub_snapshot.publish(msg_snapshot)

			ftp = FTP('192.168.42.1')
			ftp.login()
			ftp.cwd('internal_000/Bebop_2/media')
			ftp.dir('-t',files.append)
			fileForCVInfo=files[len(files)-1].split()
			fileForCV=fileForCVInfo[len(fileForCVInfo) - 1]
			ftp.retrbinary('RETR %s' % fileForCV, open('%s/%s' % (os.path.dirname(os.path.realpath(__file__)), fileForCV), 'wb').write)
			rospy.logwarn(str(fileForCV))

			rospy.Subscriber("fix", NavSatFix, self.callback)
			rospy.logwarn("Longitude: %f, Longitude %f, Altitude %f" % (self.latit, self.longit, self.altit))

			pub.publish(msg)
		
 			rate.sleep()
		ftp.quit()
	
	def __init__(self):
		self.latit = 0
		self.longit = 0
		self.camera_control()
		

if __name__ == '__main__':
	try:
		bebop_control = Controller()
	except rospy.ROSInterruptException:
		pass
