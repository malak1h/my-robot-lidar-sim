import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class StopBeforeObstacle(Node):
    def __init__(self):
        super().__init__('stop_before_obstacle')
        self.declare_parameter('stop_distance', 1.0)   # meters
        self.declare_parameter('speed', 0.2)           # m/s
        self.declare_parameter('cone_deg', 20.0)       # +/- degrees ahead

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_subscription(LaserScan, '/scan', self.on_scan,
                                 qos_profile_sensor_data)

    def on_scan(self, msg):
        stop_dist = self.get_parameter('stop_distance').value
        speed = self.get_parameter('speed').value
        cone = math.radians(self.get_parameter('cone_deg').value)

        # Collect distances of beams inside the front cone (angle 0 = straight ahead)
        front = []
        for i, r in enumerate(msg.ranges):
            angle = msg.angle_min + i * msg.angle_increment
            angle = math.atan2(math.sin(angle), math.cos(angle))  # wrap to -pi..pi
            if abs(angle) <= cone and math.isfinite(r) and r >= msg.range_min:
                front.append(r)

        closest = min(front) if front else float('inf')

        cmd = Twist()
        if closest < stop_dist:
            cmd.linear.x = 0.0
            self.get_logger().info(f'STOP: obstacle at {closest:.2f} m')
        else:
            cmd.linear.x = speed
            self.get_logger().info(f'Driving, closest ahead: {closest:.2f} m')
        self.pub.publish(cmd)


def main():
    rclpy.init()
    node = StopBeforeObstacle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.pub.publish(Twist())   # make sure the car stops on exit
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
