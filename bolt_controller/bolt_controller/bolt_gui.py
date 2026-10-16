import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge

import cv2


class BoltGUI(Node):

    def __init__(self):
        super().__init__("bolt_gui")

        self.bridge = CvBridge()
        self.image = None

        self.subscription = self.create_subscription(
            Image,
            "/inference_result",
            self.image_callback,
            10
        )
        self.target_publisher= self.create_publisher(
            Point,
            "/bolt_target_pixel",
            10
        )

        cv2.namedWindow("Bolt Controller")

        cv2.setMouseCallback(
            "Bolt Controller",
            self.mouse_callback
        )


    def image_callback(self, msg):

        self.image = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding = "passthrough"
        )


    def mouse_callback(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:

            print("Clicked bolt position:")
            print("x =", x, " y =", y)
            msg= Point()
            msg.x= float(x)
            msg.y= float(y)
            msg.z= 0.0
            self.target_publisher.publish(msg)

    def show_image(self):

        if self.image is not None:

            cv2.imshow(
                "Bolt Controller",
                self.image
            )

            cv2.waitKey(1)



def main():

    rclpy.init()

    node = BoltGUI()

    while rclpy.ok():

        rclpy.spin_once(
            node,
            timeout_sec=0.01
        )

        node.show_image()


    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()