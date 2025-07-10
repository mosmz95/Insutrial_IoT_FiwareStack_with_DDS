import rclpy
from rclpy.node import Node
import requests
from communication_interfaces.msg import PcbInfoMsg, PcbMetaMsg
from cv_bridge import CvBridge
import cv2
import numpy as np
import sys
import argparse
class DefectivePCBListener(Node):
    def __init__(self, server_url):
        super().__init__('defective_pcb_listener')
        self.subscription = self.create_subscription(PcbInfoMsg, '/defective_pcb_info', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(PcbMetaMsg, '/pcb_metadata', 1)
        self.bridge = CvBridge()
        self.server_url = server_url.rstrip('/')  
        self.get_logger().info(f"Listening on /defective_pcb_info, uploading to: {self.server_url}/upload")

    def listener_callback(self, msg):
        self.get_logger().info(f"""
        Received PCB Info:
        ID: {msg.id}
        Departured: {msg.departured}
        Width: {msg.width}
        Height: {msg.height}
        Defected: {msg.defected}
        Material: {msg.material_info}
        Heatsinks: {msg.heatsink_number}
        Defect Location: ({msg.defect_loc_x}, {msg.defect_loc_y})
        """)

        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg.pcb_img, desired_encoding='bgr8')
            success, encoded_image = cv2.imencode('.png', cv_image)
            if not success:
                self.get_logger().error("Failed to encode image")
                return

            files = {'file': ('pcb_image.png', encoded_image.tobytes(), 'image/png')}
            response = requests.post(f"{self.server_url}/upload", files=files)

            if response.status_code == 200:
                image_url = response.json().get("image_url", "unknown")
                self.get_logger().info(f"Image uploaded successfully.")
                if 'localhost' in image_url:
                    server_ip = self.server_url.split('//')[-1].split(':')[0]
                    image_url = image_url.replace('localhost', server_ip)

                metadata_pcb  =PcbMetaMsg()
                metadata_pcb.url = image_url
                metadata_pcb.id = msg.id
                metadata_pcb.departured = msg.departured
                metadata_pcb.width = msg.width
                metadata_pcb.height = msg.height
                metadata_pcb.defected = msg.defected
                metadata_pcb.material_info = msg.material_info
                metadata_pcb.heatsink_number = msg.heatsink_number
                metadata_pcb.defect_loc_x = msg.defect_loc_x
                metadata_pcb.defect_loc_y = msg.defect_loc_y
                self.publisher_.publish(metadata_pcb)
                self.get_logger().info(f"""
                Augmented PCB Info with URL:
                ID: {msg.id}
                Image URL: {image_url}
                is published.
                """)
                
                

            else:
                self.get_logger().warn(f"Upload failed: {response.status_code} {response.text}")

        except Exception as e:
            self.get_logger().error(f"Error in image processing/upload: {e}")


def main(args=None):
    rclpy.init(args=args)

    parser = argparse.ArgumentParser(description='Defective PCB Listener Node')
    parser.add_argument('server_url', help='Server URL where PCB imges will be sent http://0.0.0.0:5000')

    # parse_known_args ensures ROS 2 internal args like --ros-args don't break parsing
    known_args, _ = parser.parse_known_args()

    server_url = known_args.server_url
    print(f"✅ Parsed server_url: {server_url}")
    node = DefectivePCBListener(server_url)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
