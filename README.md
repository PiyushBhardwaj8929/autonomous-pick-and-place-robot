# Autonomous Pick-and-Place Robot Simulation

**ROS 2 | Gazebo | MoveIt 2 | YOLOv8 | Computer Vision | Robotics**

## Overview

This project focuses on developing an autonomous pick-and-place robotic system in simulation. It combines computer vision for object detection with robotic motion planning and simulation to demonstrate an automated object-handling workflow.

The project was developed during my internship at **Tech Mahindra Limited**.

## Objectives

- Explore autonomous robotic manipulation in a simulated environment.
- Use YOLOv8 for visual object detection, where configured.
- Integrate ROS 2 components for robot communication and coordination.
- Use Gazebo to simulate the robot and its environment.
- Use MoveIt 2 for motion planning and manipulation, where configured.

## Technologies Used

- **ROS 2:** Robot software framework and communication.
- **Gazebo:** Robot and environment simulation.
- **MoveIt 2:** Robotic motion planning and manipulation.
- **YOLOv8:** Object detection and computer vision.
- **Python / C++:** Implementation, depending on the package.

## System Workflow

1. Initialize the simulation environment.
2. Launch the robot and required ROS 2 nodes.
3. Detect or identify the target object using the configured perception pipeline.
4. Plan the robot's movement toward the target.
5. Execute the pick-and-place sequence in simulation.

*The workflow above describes the intended system; retain only the steps implemented and tested in the repository.*

## Repository Structure

The repository contains the project source files, robot and simulation configurations, launch files, and supporting resources as applicable.

## Setup and Execution

1. Install a compatible ROS 2 distribution and the required dependencies.
2. Install Gazebo, MoveIt 2, and YOLOv8 dependencies as required by the project.
3. Clone this repository.
4. Build the ROS 2 workspace using `colcon build` if it contains a ROS 2 workspace.
5. Source the workspace and launch the relevant simulation using the actual launch commands provided in the repository.

Refer to the package configuration and launch files for the exact commands and dependencies.

## Results and Demonstration

Add screenshots or a short video demonstrating the robot simulation, object detection, motion planning, and pick-and-place execution, if these functions were implemented and tested.

## Learning Outcomes

- ROS 2 workspace and package organization.
- Robotic simulation using Gazebo.
- Motion planning concepts with MoveIt 2.
- Computer vision integration with YOLOv8.
- Coordination of perception and robotic manipulation.

## Acknowledgment

This project was developed during my internship at Tech Mahindra Limited. Any company-specific information is excluded from this public repository.

## Author

**Piyush Bhardwaj**

GitHub: https://github.com/PiyushBhardwaj8929
