---
title: Curriculum Specifications & Architecture
description: Technical specifications and architecture roadmap for Physical AI & Humanoid Robotics
---

# Physical AI & Humanoid Robotics — Architecture Specifications

Welcome to the engineering specifications for the Physical AI and Humanoid Robotics curriculum. This open-access textbook provides complete mathematical modeling, code walkthroughs, and practical deployment pipelines across the four foundational layers of embodied autonomy.

---

## Technical Specifications Summary

| Layer | Domain | Primary Middleware & Tooling | Real-Time Frequency | Primary Objective |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1** | Deterministic Control | ROS 2 Humble/Iron, CycloneDDS, Iceoryx IPC | 1 kHz (1000 Hz) | Sub-millisecond motor commutation & QoS guarantees |
| **Layer 2** | Physics & Simulation | Gazebo Harmonic, DART Physics, Unity HDRP | 60 – 240 FPS | Multi-contact dynamics & sensor sim-to-real transfer |
| **Layer 3** | Edge AI & Perception | NVIDIA Isaac Sim 4.0, NITROS, cuVSLAM, Nav2 | 30 – 60 Hz | Hardware-accelerated SLAM & bipedal lattice path planning |
| **Layer 4** | Multimodal Cognition | OpenVLA, π0, Octo, Whisper, Gemini 2.5 | 5 – 20 Hz | Voice-to-action chunking & hierarchical LLM task planning |

---

## Curriculum Structure

:::tip Open Access Learning
All 26 chapters are structured with reproducible code, architectural diagrams, and hands-on exercises. You can query the embedded **RAG AI Assistant** on any page using the bottom-right floating tutor or pressing <kbd>⌘K</kbd> / <kbd>Ctrl+K</kbd>.
:::

### [Module 1: The Robotic Nervous System (ROS 2)](/ai-book/module1-ros2/1-1-introduction)
- **1-1 to 1-3:** ROS 2 architecture, DDS discovery, and colcon workspace management
- **1-4 to 1-7:** Real-time lifecycle nodes, topics, services, actions, and QoS contracts
- **1-8 to 1-10:** Dynamic parameter servers, rclpy/rclcpp interop, and production best practices

### [Module 2: The Digital Twin (Gazebo & Unity)](/ai-book/module2-digital-twin/2-1-introduction-to-digital-twins)
- **2-1 to 2-2:** Physics engines (DART, Bullet, ODE) and Gazebo Harmonic simulation
- **2-3 to 2-4:** Sensor simulation (Stereo RGB-D, IMU, Force-Torque) and Unity photorealism
- **2-5:** Hands-on bipedal humanoid balance and walking simulation exercises

### [Module 3: The AI-Robot Brain (NVIDIA Isaac)](/ai-book/module3-ai-robot-brain/3-1-introduction-to-isaac-platform)
- **3-1 to 3-2:** NVIDIA Omniverse, Isaac Sim setup, and synthetic data generation (SDG)
- **3-3 to 3-4:** NITROS zero-copy acceleration, cuVSLAM visual odometry, and Nav2 lattice planning
- **3-5:** Hands-on perception and autonomous navigation pipeline deployment

### [Module 4: Vision-Language-Action (VLA)](/ai-book/module4-vla/4-1-introduction-to-vla-systems)
- **4-1 to 4-2:** Embodied foundation models, OpenVLA policies, and Whisper voice integration
- **4-3 to 4-4:** Hierarchical task planning with LLMs, 3D spatial grounding, and action chunking
- **4-5:** End-to-end voice-directed humanoid tabletop manipulation and locomotion

---

:::note Vector Search & AI Verification
Every chapter in this book has been chunked, embedded, and indexed in Qdrant Cloud. Ask the AI Tutor questions at any time for exact citations and equations.
:::
