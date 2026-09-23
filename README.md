UAV Passive Detection & Tracking System - Acoustic Subsystem 🚁🎙️

Project Overview

This repository contains the acoustic simulation environment for the Electrical Engineering Capstone Project at Taif University. The goal of this subsystem is to passively detect and track Unmanned Aerial Vehicles (UAVs) utilizing an Acoustic Sensor Array, working in parallel with an RF detection subsystem to guide a PTZ camera for visual verification.

Current Phase: Software Simulation

The project is currently in the software simulation phase to validate Direction of Arrival (DOA) algorithms before hardware implementation.

Key Features

Sensor Array Topology: Simulating an 8-microphone Uniform Circular Array (UCA).

DOA Algorithm: Implementing Time Difference of Arrival (TDOA) using the SRP-PHAT algorithm to estimate the azimuth angle of the sound source.

3D Visualization: ROS 2 and RViz integration for real-time 3D visualization of the drone's trajectory and the microphone array URDF models.

Real Data Testing: Designed to process real drone audio datasets (e.g., DroneAudioSet) for realistic acoustic modeling.

Tech Stack

ROS 2 (Robot Operating System) running on Ubuntu via WSL2.

Python 3

PyRoomAcoustics (for acoustic wave propagation modeling)

RViz (for 3D visualization)

Repository Structure

src/acoustic_sim/: Contains Python scripts for the acoustic simulation, TDOA algorithm, and trajectory broadcasting.

src/uav_array_description/: Contains the URDF (Unified Robot Description Format) files for the drone and the microphone array 3D models.

How to Run the Simulation

1. Acoustic DOA Estimation

To run the acoustic simulation and generate the TDOA direction graph:

cd src/acoustic_sim/scripts
python3 run_doa.py


2. RViz 3D Visualization

To view the 3D models (e.g., the microphone array) in RViz:

ros2 launch urdf_tutorial display.launch.py model:=/home/azzoz/uav_doa_ws/src/uav_array_description/urdf/microphone_array.urdf


To visualize the drone flying in the simulated circular trajectory:

Terminal 1: Run the RViz drone model:

ros2 launch urdf_tutorial display.launch.py model:=/home/azzoz/uav_doa_ws/src/uav_array_description/urdf/drone.urdf


Terminal 2: Run the trajectory broadcaster:

cd src/acoustic_sim/scripts
python3 visualize_trajectory.py
