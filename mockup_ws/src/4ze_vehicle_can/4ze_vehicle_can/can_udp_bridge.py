import socket
import struct

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, UInt8MultiArray


class CanUdpBridge(Node):
    """Encode pedal values as 11-byte CAN-like frames and send them to Windows over UDP."""

    def __init__(self):
        super().__init__('can_udp_bridge')
        self.declare_parameter('windows_host', 'host.docker.internal')
        self.declare_parameter('udp_port', 5005)
        self.host = self.get_parameter('windows_host').value
        self.port = self.get_parameter('udp_port').value
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 5006))
        self.can_pub = self.create_publisher(UInt8MultiArray, '/can/tx', 10)
        self.accel = 0
        self.brake = 0
        self.create_subscription(Float32, '/pedal/accelerator', self.accel_callback, 10)
        self.create_subscription(Float32, '/pedal/brake', self.brake_callback, 10)

    def accel_callback(self, msg):
        self.accel = self.to_u16(msg.data)
        self.send_frame(0x101, self.accel)

    def brake_callback(self, msg):
        self.brake = self.to_u16(msg.data)
        self.send_frame(0x102, self.brake)

    def to_u16(self, value):
        return max(0, min(1000, round(float(value) * 1000)))

    def send_frame(self, can_id, value):
        # Packet: uint16 CAN ID, uint8 DLC, then 8-byte CAN payload.
        payload = struct.pack('<HBB8s', can_id, 2, value & 0xFF, bytes([(value >> 8) & 0xFF]) + bytes(6))
        self.sock.sendto(payload, (self.host, self.port))
        msg = UInt8MultiArray()
        msg.data = list(payload)
        self.can_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = CanUdpBridge()
    try:
        rclpy.spin(node)
    finally:
        node.sock.close()
        node.destroy_node()
        rclpy.shutdown()
