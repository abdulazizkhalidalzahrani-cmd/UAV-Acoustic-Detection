import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math

# دالة لتحويل الزوايا إلى نظام Quaternions الذي يفهمه ROS 2
def quaternion_from_euler(roll, pitch, yaw):
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    return [sr * cp * cy - cr * sp * sy, cr * sp * cy + sr * cp * sy, cr * cp * sy - sr * sp * cy, cr * cp * cy + sr * sp * sy]

class DroneTrajectory(Node):
    def __init__(self):
        super().__init__('drone_trajectory')
        self.br = TransformBroadcaster(self)
        self.timer = self.create_timer(0.05, self.publish_tf) # تحديث الحركة بسرعة
        self.theta = 0.0
        self.get_logger().info("Publishing drone trajectory...")

    def publish_tf(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'       # الإطار الثابت للبيئة
        t.child_frame_id = 'base_link'  # إطار الدرون

        # إحداثيات المسار الدائري (مطابقة للمحاكاة الصوتية)
        t.transform.translation.x = 5.0 + 2.0 * math.cos(self.theta)
        t.transform.translation.y = 5.0 + 2.0 * math.sin(self.theta)
        t.transform.translation.z = 2.0

        # جعل الدرون يلتف ليوجه مقدمته نحو مسار الطيران
        yaw = self.theta + (math.pi / 2.0)
        q = quaternion_from_euler(0, 0, yaw)
        
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        self.br.sendTransform(t)
        
        self.theta += 0.02
        if self.theta >= 2 * math.pi:
            self.theta = 0.0

def main():
    rclpy.init()
    node = DroneTrajectory()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
