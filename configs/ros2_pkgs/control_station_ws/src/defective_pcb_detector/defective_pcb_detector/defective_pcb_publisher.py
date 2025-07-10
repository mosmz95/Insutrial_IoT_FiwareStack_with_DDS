import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
import os

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from communication_interfaces.msg import PcbInfoMsg  
from datetime import datetime
package_share_dir = get_package_share_directory('defective_pcb_detector')
# script_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(script_dir)
# folder_path = os.path.join(parent_dir, "configs")

class DefectivePCBPublisher(Node):
    def __init__(self):
        super().__init__('defective_pcb_publisher')

        self.publisher_ = self.create_publisher(PcbInfoMsg, '/defective_pcb_info', 1)
        timer_period = 30.0 
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.bridge = CvBridge()
        self.image_path = self.image_path = os.path.join(package_share_dir, 'configs', 'ic_detected.png')

    def timer_callback(self):

        msg = PcbInfoMsg()
        msg.id = "PCB_015"
        msg.departured = datetime.now().isoformat()

        msg.width = 120.0
        msg.height = 80.0
        msg.defected = True
        msg.material_info = "data sheet info"
        msg.heatsink_number = 4
        msg.defect_loc_x = 45.5
        msg.defect_loc_y = 60.3

        if os.path.exists(self.image_path):
            cv_image = cv2.imread(self.image_path)
            ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
            msg.pcb_img = ros_image
            self.publisher_.publish(msg)
            self.get_logger().info(f'Published Defective PCB info with ID {msg.id}')
        else:
            self.get_logger().error(f'Image not found at path: {self.image_path}')

def main(args=None):
    rclpy.init(args=args)
    node = DefectivePCBPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
