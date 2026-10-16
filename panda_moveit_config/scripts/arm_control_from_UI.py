#!/usr/bin/env python3

import time
import threading

import rclpy
from rclpy.node import Node
from rclpy.logging import get_logger
from rclpy.action import ActionClient

from geometry_msgs.msg import PoseStamped, Point
from control_msgs.action import GripperCommand

from moveit.planning import MoveItPy


def plan_and_execute(
    robot,
    planning_component,
    logger,
    sleep_time=0.0,
):

    logger.info("Planning trajectory")

    plan_result = planning_component.plan()

    if plan_result:

        logger.info("Executing plan")

        robot.execute(
            plan_result.trajectory,
            controllers=[]
        )

    else:

        logger.error("Planning failed")

    time.sleep(sleep_time)



class Controller(Node):

    def __init__(self):

        super().__init__("bolt_arm_controller")


        self.subscription = self.create_subscription(
            Point,
            "/bolt_target_pixel",
            self.listener_callback,
            10
        )


        self.pose_goal = PoseStamped()
        self.pose_goal.header.frame_id = "panda_link0"


        self.panda = MoveItPy(
            node_name="moveit_controller"
        )


        self.panda_arm = self.panda.get_planning_component(
            "panda_arm"
        )


        self.logger = get_logger(
            "moveit_py.pose_goal"
        )


        self.gripper_client = ActionClient(
            self,
            GripperCommand,
            "/panda_hand_controller/gripper_cmd"
        )


        self.height = 0.18
        self.pick_height = 0.126
        self.carrying_height = 0.30

        self.init_angle = -0.3825



    def pixel_to_robot(self, px, py):

        # Image reference center
        center_px = 320
        center_py = 215


        # Robot position of table center
        center_x = 0.45
        center_y = 0.0


        table_width = 0.8
        table_height = 1.5


        left = 29
        right = 612

        top = 70
        bottom = 380



        dx = (
            (py - center_py)
            /
            (bottom - top)
            *
            table_height
        )


        dy = (
            (px - center_px)
            /
            (right - left)
            *
            table_width
        )


        robot_x = center_x + dx
        robot_y = center_y - dy


        self.get_logger().info(
            f"BEFORE CLAMP robot_x={robot_x}, robot_y={robot_y}"
        )


        # Restore workspace limits
        robot_x = max(0.25, min(0.75, robot_x))
        robot_y = max(-0.35, min(0.35, robot_y))


        self.get_logger().info(
            f"Converted pixel ({px},{py}) -> robot ({robot_x},{robot_y})"
        )


        return robot_x, robot_y




    def move_to(
        self,
        x,
        y,
        z,
        xo,
        yo,
        zo,
        wo
    ):


        self.get_logger().info(
            f"GOING TO POSE x={x} y={y} z={z}"
        )


        self.pose_goal.header.stamp = (
            self.get_clock()
            .now()
            .to_msg()
        )


        self.pose_goal.pose.position.x = x
        self.pose_goal.pose.position.y = y
        self.pose_goal.pose.position.z = z


        self.pose_goal.pose.orientation.x = xo
        self.pose_goal.pose.orientation.y = yo
        self.pose_goal.pose.orientation.z = zo
        self.pose_goal.pose.orientation.w = wo



        self.panda_arm.set_start_state_to_current_state()


        self.panda_arm.set_goal_state(
            pose_stamped_msg=self.pose_goal,
            pose_link="panda_link8"
        )


        plan_and_execute(
            self.panda,
            self.panda_arm,
            self.logger,
            sleep_time=2.0
        )





    def gripper_action(self, action):


        if not self.gripper_client.wait_for_server(
            timeout_sec=3.0
        ):

            self.get_logger().error(
                "Gripper action server not available"
            )

            return



        goal = GripperCommand.Goal()


        if action == "open":

            goal.command.position = 0.035
            goal.command.max_effort = 20.0


        elif action == "close":

            goal.command.position = 0.0
            goal.command.max_effort = 20.0


        else:

            return



        self.get_logger().info(
            f"GRIPPER {action}"
        )


        self.gripper_client.send_goal_async(
            goal
        )


        time.sleep(2.0)





    def listener_callback(self,msg):


        self.get_logger().info(
            "******** CALLBACK RECEIVED ********"
        )


        self.get_logger().info(
            f"PIXEL x={msg.x} y={msg.y}"
        )



        bolt_x, bolt_y = self.pixel_to_robot(
            msg.x,
            msg.y
        )



        # Move above bolt
        self.move_to(
            bolt_x,
            bolt_y,
            self.height,
            1.0,
            self.init_angle,
            0.0,
            0.0
        )



        self.gripper_action("open")



        # Pick
        self.move_to(
            bolt_x,
            bolt_y,
            self.pick_height,
            1.0,
            self.init_angle,
            0.0,
            0.0
        )



        self.gripper_action("close")



        # Lift
        self.move_to(
            bolt_x,
            bolt_y,
            self.carrying_height,
            1.0,
            self.init_angle,
            0.0,
            0.0
        )



        # Drop position
        self.move_to(
            0.3,
            -0.3,
            self.carrying_height,
            1.0,
            self.init_angle,
            0.0,
            0.0
        )



        self.gripper_action("open")





def main():

    rclpy.init()

    controller = Controller()


    executor = rclpy.executors.MultiThreadedExecutor()

    executor.add_node(controller)


    thread = threading.Thread(
        target=executor.spin,
        daemon=True
    )

    thread.start()


    try:

        while rclpy.ok():

            time.sleep(0.5)


    except KeyboardInterrupt:

        pass


    rclpy.shutdown()

    thread.join()




if __name__ == "__main__":

    main()