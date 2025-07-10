import rclpy
from rclpy.node import Node
from communication_interfaces.msg import PcbInfoMsg
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class DefectivePCBListener(Node):
    def __init__(self):
        super().__init__('defective_pcb_listener')
        self.subscription = self.create_subscription(PcbInfoMsg,'/defective_pcb_info', self.listener_callback,1)
        self.bridge = CvBridge()
        self.get_logger().info('Listening on /defective_pcb_info')

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
            cv2.imshow("Received PCB Image", cv_image)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = DefectivePCBListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
