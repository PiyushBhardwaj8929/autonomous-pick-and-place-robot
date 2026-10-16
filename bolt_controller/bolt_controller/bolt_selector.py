#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from std_msgs.msg import Float64MultiArray
from yolov8_msgs.msg import Yolov8Inference


class BoltSelector(Node):

    def __init__(self):
        super().__init__("bolt_selector")


def main():

    rclpy.init()

    node = BoltSelector()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()