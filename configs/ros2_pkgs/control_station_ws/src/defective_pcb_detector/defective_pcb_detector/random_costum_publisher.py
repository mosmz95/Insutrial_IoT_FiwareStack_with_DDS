import rclpy
from rclpy.node import Node
import os

from sensor_msgs.msg import Image
import cv2
from communication_interfaces.msg import PcbInfoMsg,PcbMetaMsg  
from datetime import datetime


class DefectivePCBPublisher(Node):
    def __init__(self):
        super().__init__('defective_pcb_publisher')

        self.publisher_ = self.create_publisher(PcbMetaMsg, '/random_pcb_info', 1)
        timer_period = 10 
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.counter = 0

    def timer_callback(self):

        msg = PcbMetaMsg()
        msg.id = "PCB_015"
        msg.departured = datetime.now().isoformat()

        msg.width = 120.0
        msg.height = 80.0
        msg.defected = True
        msg.material_info = "data sheet info"
        msg.heatsink_number = 4
        msg.defect_loc_x = 45.5
        msg.defect_loc_y = 60.3
        msg.url = f"my fake url {self.counter}"
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published Defective PCB info with url {msg.url}')
        self.counter +=1

def main(args=None):
    rclpy.init(args=args)
    node = DefectivePCBPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
