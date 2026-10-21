import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float32


class PedalSignalNode(Node):
    """Convert interactive joint positions into normalized pedal signals."""

    def __init__(self):
        super().__init__('pedal_signal_node')
        self.accel_pub = self.create_publisher(Float32, '/pedal/accelerator', 10)
        self.brake_pub = self.create_publisher(Float32, '/pedal/brake', 10)
        self.joint_sub = self.create_subscription(JointState, '/joint_states', self.joint_callback, 10)

    def joint_callback(self, msg):
        values = dict(zip(msg.name, msg.position))
        self.publish_value(self.accel_pub, values.get('accelerator_joint', 0.0))
        self.publish_value(self.brake_pub, values.get('brake_joint', 0.0))

    def publish_value(self, publisher, position):
        msg = Float32()
        msg.data = max(0.0, min(1.0, position / 0.50))
        publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PedalSignalNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
