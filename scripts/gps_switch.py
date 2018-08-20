#!/usr/bin/env python
import rospy
from nav_msgs.msg   import Odometry

class gps_switch:
  switch_on = True

  def __init__(self):
    self.params()
    self.subs()
    self.pubs()

  def params(self):
    cutoff_time = rospy.get_param('~cutoff_time', -1);
    if cutoff_time >= 0:
      self.timer = rospy.Timer(rospy.Duration(cutoff_time), self.switchOff, oneshot=True)

  def subs(self):
    rospy.Subscriber("gps_in", Odometry, self.gpsCallback)

  def pubs(self):
    self.pub = rospy.Publisher('gps_out', Odometry, queue_size=10)

  def switchOff(self, event):
    print("Turning off GPS")
    self.switch_on = False

  def gpsCallback(self, gps_msg):
    if self.switch_on:
      self.pub.publish(gps_msg)

if __name__ == '__main__':
  rospy.init_node('gps_switch', anonymous=True)
  obj = gps_switch()
  rospy.spin()
