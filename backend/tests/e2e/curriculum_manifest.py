"""
Authoritative Curriculum Manifest for the 12-Module Robotics Textbook.

Defines the exact 110-chapter structure (+ 1 intro) spanning all 12 modules,
used for automated structural validation, link integrity checks, and progressive
milestone verification.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class ChapterSpec:
    module_id: str
    module_dir: str
    filename: str
    chapter_num: str
    expected_title_fragment: str
    milestone: str
    is_existing_initially: bool

    @property
    def relative_path(self) -> Path:
        if self.module_dir:
            return Path("ai-book-docs") / self.module_dir / self.filename
        return Path("ai-book-docs") / self.filename


@dataclass(frozen=True)
class ModuleSpec:
    module_id: str
    module_dir: str
    title: str
    expected_chapter_count: int
    position: int


MODULES: List[ModuleSpec] = [
    ModuleSpec("module1", "module1-ros2", "The Robotic Nervous System (ROS 2)", 14, 1),
    ModuleSpec("module2", "module2-digital-twin", "The Digital Twin (Gazebo & Unity)", 10, 2),
    ModuleSpec("module3", "module3-ai-robot-brain", "The AI-Robot Brain (NVIDIA Isaac)", 10, 3),
    ModuleSpec("module4", "module4-vla", "Vision-Language-Action (VLA) Systems", 10, 4),
    ModuleSpec("module5", "module5-kinematics-dynamics", "Humanoid Kinematics & Dynamics", 10, 5),
    ModuleSpec("module6", "module6-bipedal-locomotion", "Bipedal Locomotion & Whole-Body Control", 10, 6),
    ModuleSpec("module7", "module7-dexterous-manipulation", "Dexterous Manipulation & Hand Design", 8, 7),
    ModuleSpec("module8", "module8-robot-learning", "Robot Learning & Reinforcement Learning", 10, 8),
    ModuleSpec("module9", "module9-sim-to-real", "Sim-to-Real Transfer & Domain Randomization", 8, 9),
    ModuleSpec("module10", "module10-hardware-architecture", "Hardware Architecture & Embedded Systems", 8, 10),
    ModuleSpec("module11", "module11-safety-ethics", "Safety, Ethics & Deployment", 6, 11),
    ModuleSpec("module12", "module12-capstone-frontiers", "Capstone Projects & Research Frontiers", 6, 12),
]


CHAPTERS: List[ChapterSpec] = [
    # Intro
    ChapterSpec("intro", "", "intro.mdx", "intro", "Foundations", "M1", True),

    # Module 1: ROS 2 (14 chapters)
    ChapterSpec("module1", "module1-ros2", "1-1-introduction.mdx", "1-1", "Robotic Nervous System", "M1", True),
    ChapterSpec("module1", "module1-ros2", "1-2-ros2-core-concepts.mdx", "1-2", "Core Concepts", "M1", True),
    ChapterSpec("module1", "module1-ros2", "1-3-ros2-workspace.mdx", "1-3", "Workspace", "M1", True),
    ChapterSpec("module1", "module1-ros2", "1-4-nodes.mdx", "1-4", "Nodes", "M1", True),
    ChapterSpec("module1", "module1-ros2", "1-5-topics.mdx", "1-5", "Topics", "M1", True),
    ChapterSpec("module1", "module1-ros2", "1-6-services.mdx", "1-6", "Services", "M1", True),
    ChapterSpec("module1", "module1-ros2", "1-7-actions.mdx", "1-7", "Actions", "M1", True),
    ChapterSpec("module1", "module1-ros2", "1-8-parameters.mdx", "1-8", "Parameters", "M1", True),
    ChapterSpec("module1", "module1-ros2", "1-9-rclpy-rclcpp.mdx", "1-9", "rclpy", "M1", True),
    ChapterSpec("module1", "module1-ros2", "1-10-best-practices.mdx", "1-10", "Best Practices", "M1", True),
    # M1 Phase 1 Expansion (4 chapters)
    ChapterSpec("module1", "module1-ros2", "1-11-ros2-control.mdx", "1-11", "ros2_control", "M2", False),
    ChapterSpec("module1", "module1-ros2", "1-12-dds-internals.mdx", "1-12", "DDS", "M2", False),
    ChapterSpec("module1", "module1-ros2", "1-13-real-time-linux.mdx", "1-13", "Real-Time Linux", "M2", False),
    ChapterSpec("module1", "module1-ros2", "1-14-ros2-diagnostics-and-monitoring.mdx", "1-14", "Diagnostics", "M2", False),

    # Module 2: Gazebo & Unity (10 chapters)
    ChapterSpec("module2", "module2-digital-twin", "2-1-introduction-to-digital-twins.mdx", "2-1", "Digital Twins", "M1", True),
    ChapterSpec("module2", "module2-digital-twin", "2-2-gazebo-simulation-engine.mdx", "2-2", "Gazebo", "M1", True),
    ChapterSpec("module2", "module2-digital-twin", "2-3-sensor-simulation.mdx", "2-3", "Sensor Simulation", "M1", True),
    ChapterSpec("module2", "module2-digital-twin", "2-4-unity-for-high-fidelity-visuals.mdx", "2-4", "Unity", "M1", True),
    ChapterSpec("module2", "module2-digital-twin", "2-5-hands-on-exercises.mdx", "2-5", "Hands-On", "M1", True),
    # M2 Phase 1 Expansion (5 chapters)
    ChapterSpec("module2", "module2-digital-twin", "2-6-urdf-and-sdf-mastery.mdx", "2-6", "URDF", "M2", False),
    ChapterSpec("module2", "module2-digital-twin", "2-7-physics-engine-deep-dive.mdx", "2-7", "Physics Engine", "M2", False),
    ChapterSpec("module2", "module2-digital-twin", "2-8-synthetic-data-generation.mdx", "2-8", "Synthetic Data", "M2", False),
    ChapterSpec("module2", "module2-digital-twin", "2-9-drake-and-mujoco.mdx", "2-9", "Drake", "M2", False),
    ChapterSpec("module2", "module2-digital-twin", "2-10-digital-twin-data-loop.mdx", "2-10", "Digital Twin", "M2", False),

    # Module 3: NVIDIA Isaac (10 chapters)
    ChapterSpec("module3", "module3-ai-robot-brain", "3-1-introduction-to-isaac-platform.mdx", "3-1", "Isaac Platform", "M1", True),
    ChapterSpec("module3", "module3-ai-robot-brain", "3-2-isaac-sim-for-humanoids.mdx", "3-2", "Isaac Sim", "M1", True),
    ChapterSpec("module3", "module3-ai-robot-brain", "3-3-isaac-ros-perception-pipeline.mdx", "3-3", "Perception Pipeline", "M1", True),
    ChapterSpec("module3", "module3-ai-robot-brain", "3-4-nav2-for-bipedal-movement.mdx", "3-4", "Nav2", "M1", True),
    ChapterSpec("module3", "module3-ai-robot-brain", "3-5-hands-on-exercises.mdx", "3-5", "Hands-On", "M1", True),
    # M3 Phase 1 Expansion (5 chapters)
    ChapterSpec("module3", "module3-ai-robot-brain", "3-6-cuvslam-and-state-estimation.mdx", "3-6", "cuVSLAM", "M2", False),
    ChapterSpec("module3", "module3-ai-robot-brain", "3-7-semantic-perception.mdx", "3-7", "Semantic Perception", "M2", False),
    ChapterSpec("module3", "module3-ai-robot-brain", "3-8-force-torque-sensing.mdx", "3-8", "Force-Torque", "M2", False),
    ChapterSpec("module3", "module3-ai-robot-brain", "3-9-multi-sensor-fusion.mdx", "3-9", "Sensor Fusion", "M2", False),
    ChapterSpec("module3", "module3-ai-robot-brain", "3-10-edge-inference-optimization.mdx", "3-10", "Edge Inference", "M2", False),

    # Module 4: VLA Systems (10 chapters)
    ChapterSpec("module4", "module4-vla", "4-1-introduction-to-vla-systems.mdx", "4-1", "VLA", "M1", True),
    ChapterSpec("module4", "module4-vla", "4-2-voice-to-action-pipeline.mdx", "4-2", "Voice-to-Action", "M1", True),
    ChapterSpec("module4", "module4-vla", "4-3-cognitive-planning-with-llms.mdx", "4-3", "Cognitive Planning", "M1", True),
    ChapterSpec("module4", "module4-vla", "4-4-multimodal-interaction.mdx", "4-4", "Multimodal", "M1", True),
    ChapterSpec("module4", "module4-vla", "4-5-hands-on-exercises.mdx", "4-5", "Hands-On", "M1", True),
    # M4 Phase 1 Expansion (5 chapters)
    ChapterSpec("module4", "module4-vla", "4-6-foundation-model-architectures.mdx", "4-6", "Foundation Model", "M2", False),
    ChapterSpec("module4", "module4-vla", "4-7-diffusion-policies.mdx", "4-7", "Diffusion", "M2", False),
    ChapterSpec("module4", "module4-vla", "4-8-imitation-learning.mdx", "4-8", "Imitation Learning", "M2", False),
    ChapterSpec("module4", "module4-vla", "4-9-reward-shaping-and-rlaif.mdx", "4-9", "Reward Shaping", "M2", False),
    ChapterSpec("module4", "module4-vla", "4-10-deployment-and-safety.mdx", "4-10", "Deployment", "M2", False),

    # Module 5: Kinematics & Dynamics (10 chapters, pre-authored)
    ChapterSpec("module5", "module5-kinematics-dynamics", "5-1-introduction-to-robot-kinematics.mdx", "5-1", "Kinematics", "M1", True),
    ChapterSpec("module5", "module5-kinematics-dynamics", "5-2-forward-kinematics.mdx", "5-2", "Forward Kinematics", "M1", True),
    ChapterSpec("module5", "module5-kinematics-dynamics", "5-3-inverse-kinematics.mdx", "5-3", "Inverse Kinematics", "M1", True),
    ChapterSpec("module5", "module5-kinematics-dynamics", "5-4-rigid-body-dynamics.mdx", "5-4", "Rigid Body Dynamics", "M1", True),
    ChapterSpec("module5", "module5-kinematics-dynamics", "5-5-spatial-algebra.mdx", "5-5", "Spatial Algebra", "M1", True),
    ChapterSpec("module5", "module5-kinematics-dynamics", "5-6-humanoid-skeleton-modeling.mdx", "5-6", "Humanoid Skeleton", "M1", True),
    ChapterSpec("module5", "module5-kinematics-dynamics", "5-7-trajectory-planning.mdx", "5-7", "Trajectory Planning", "M1", True),
    ChapterSpec("module5", "module5-kinematics-dynamics", "5-8-differential-kinematics.mdx", "5-8", "Differential Kinematics", "M1", True),
    ChapterSpec("module5", "module5-kinematics-dynamics", "5-9-contact-mechanics.mdx", "5-9", "Contact Mechanics", "M1", True),
    ChapterSpec("module5", "module5-kinematics-dynamics", "5-10-computational-tools.mdx", "5-10", "Computational Tools", "M1", True),

    # Module 6: Bipedal Locomotion (10 chapters)
    ChapterSpec("module6", "module6-bipedal-locomotion", "6-1-introduction-to-bipedal-locomotion.mdx", "6-1", "Bipedal Locomotion", "M3", False),
    ChapterSpec("module6", "module6-bipedal-locomotion", "6-2-zero-moment-point.mdx", "6-2", "Zero-Moment Point", "M3", False),
    ChapterSpec("module6", "module6-bipedal-locomotion", "6-3-capture-point-and-dcm.mdx", "6-3", "Capture Point", "M3", False),
    ChapterSpec("module6", "module6-bipedal-locomotion", "6-4-model-predictive-control.mdx", "6-4", "Model Predictive Control", "M3", False),
    ChapterSpec("module6", "module6-bipedal-locomotion", "6-5-whole-body-control.mdx", "6-5", "Whole-Body Control", "M3", False),
    ChapterSpec("module6", "module6-bipedal-locomotion", "6-6-reinforcement-learning-locomotion.mdx", "6-6", "Reinforcement Learning", "M3", False),
    ChapterSpec("module6", "module6-bipedal-locomotion", "6-7-sim-to-real-locomotion.mdx", "6-7", "Sim-to-Real", "M3", False),
    ChapterSpec("module6", "module6-bipedal-locomotion", "6-8-advanced-locomotion-skills.mdx", "6-8", "Locomotion Skills", "M3", False),
    ChapterSpec("module6", "module6-bipedal-locomotion", "6-9-gait-analysis-and-biomechanics.mdx", "6-9", "Gait Analysis", "M3", False),
    ChapterSpec("module6", "module6-bipedal-locomotion", "6-10-motion-capture-and-reference.mdx", "6-10", "Motion Capture", "M3", False),

    # Module 7: Dexterous Manipulation (8 chapters)
    ChapterSpec("module7", "module7-dexterous-manipulation", "7-1-introduction-to-dexterous-manipulation.mdx", "7-1", "Dexterous Manipulation", "M3", False),
    ChapterSpec("module7", "module7-dexterous-manipulation", "7-2-grasp-theory.mdx", "7-2", "Grasp Theory", "M3", False),
    ChapterSpec("module7", "module7-dexterous-manipulation", "7-3-robotic-hand-design.mdx", "7-3", "Robotic Hand Design", "M3", False),
    ChapterSpec("module7", "module7-dexterous-manipulation", "7-4-tactile-sensing.mdx", "7-4", "Tactile Sensing", "M3", False),
    ChapterSpec("module7", "module7-dexterous-manipulation", "7-5-motion-planning-for-manipulation.mdx", "7-5", "Motion Planning", "M3", False),
    ChapterSpec("module7", "module7-dexterous-manipulation", "7-6-learning-based-manipulation.mdx", "7-6", "Learning-Based Manipulation", "M3", False),
    ChapterSpec("module7", "module7-dexterous-manipulation", "7-7-assembly-and-contact-rich-tasks.mdx", "7-7", "Assembly", "M3", False),
    ChapterSpec("module7", "module7-dexterous-manipulation", "7-8-manipulation-benchmarks.mdx", "7-8", "Benchmarks", "M3", False),

    # Module 8: Robot Learning & RL (10 chapters)
    ChapterSpec("module8", "module8-robot-learning", "8-1-foundations-of-reinforcement-learning.mdx", "8-1", "Reinforcement Learning", "M3", False),
    ChapterSpec("module8", "module8-robot-learning", "8-2-deep-rl-algorithms.mdx", "8-2", "Deep RL", "M3", False),
    ChapterSpec("module8", "module8-robot-learning", "8-3-rl-for-continuous-control.mdx", "8-3", "Continuous Control", "M3", False),
    ChapterSpec("module8", "module8-robot-learning", "8-4-massively-parallel-training.mdx", "8-4", "Massively Parallel", "M3", False),
    ChapterSpec("module8", "module8-robot-learning", "8-5-curriculum-learning.mdx", "8-5", "Curriculum Learning", "M3", False),
    ChapterSpec("module8", "module8-robot-learning", "8-6-offline-rl-and-imitation.mdx", "8-6", "Offline RL", "M3", False),
    ChapterSpec("module8", "module8-robot-learning", "8-7-model-based-rl.mdx", "8-7", "Model-Based RL", "M3", False),
    ChapterSpec("module8", "module8-robot-learning", "8-8-multi-task-and-meta-learning.mdx", "8-8", "Meta-Learning", "M3", False),
    ChapterSpec("module8", "module8-robot-learning", "8-9-safe-reinforcement-learning.mdx", "8-9", "Safe Reinforcement Learning", "M3", False),
    ChapterSpec("module8", "module8-robot-learning", "8-10-evaluation-and-benchmarking.mdx", "8-10", "Benchmarking", "M3", False),

    # Module 9: Sim-to-Real Transfer (8 chapters)
    ChapterSpec("module9", "module9-sim-to-real", "9-1-the-reality-gap.mdx", "9-1", "Reality Gap", "M3", False),
    ChapterSpec("module9", "module9-sim-to-real", "9-2-domain-randomization.mdx", "9-2", "Domain Randomization", "M3", False),
    ChapterSpec("module9", "module9-sim-to-real", "9-3-system-identification.mdx", "9-3", "System Identification", "M3", False),
    ChapterSpec("module9", "module9-sim-to-real", "9-4-privileged-learning.mdx", "9-4", "Privileged Learning", "M3", False),
    ChapterSpec("module9", "module9-sim-to-real", "9-5-adaptation-modules.mdx", "9-5", "Adaptation Modules", "M3", False),
    ChapterSpec("module9", "module9-sim-to-real", "9-6-real-world-fine-tuning.mdx", "9-6", "Fine-Tuning", "M3", False),
    ChapterSpec("module9", "module9-sim-to-real", "9-7-transfer-benchmarks.mdx", "9-7", "Transfer Benchmarks", "M3", False),
    ChapterSpec("module9", "module9-sim-to-real", "9-8-digital-twin-feedback-loop.mdx", "9-8", "Feedback Loop", "M3", False),

    # Module 10: Hardware Architecture (8 chapters)
    ChapterSpec("module10", "module10-hardware-architecture", "10-1-humanoid-mechanical-design.mdx", "10-1", "Mechanical Design", "M4", False),
    ChapterSpec("module10", "module10-hardware-architecture", "10-2-actuator-technologies.mdx", "10-2", "Actuator", "M4", False),
    ChapterSpec("module10", "module10-hardware-architecture", "10-3-power-electronics-and-motor-control.mdx", "10-3", "Power Electronics", "M4", False),
    ChapterSpec("module10", "module10-hardware-architecture", "10-4-communication-buses.mdx", "10-4", "Communication Buses", "M4", False),
    ChapterSpec("module10", "module10-hardware-architecture", "10-5-compute-platforms.mdx", "10-5", "Compute Platforms", "M4", False),
    ChapterSpec("module10", "module10-hardware-architecture", "10-6-sensor-hardware.mdx", "10-6", "Sensor Hardware", "M4", False),
    ChapterSpec("module10", "module10-hardware-architecture", "10-7-real-time-embedded-software.mdx", "10-7", "Embedded Software", "M4", False),
    ChapterSpec("module10", "module10-hardware-architecture", "10-8-system-integration-and-testing.mdx", "10-8", "System Integration", "M4", False),

    # Module 11: Safety, Ethics & Deployment (6 chapters)
    ChapterSpec("module11", "module11-safety-ethics", "11-1-robot-safety-standards.mdx", "11-1", "Safety Standards", "M4", False),
    ChapterSpec("module11", "module11-safety-ethics", "11-2-functional-safety-architecture.mdx", "11-2", "Functional Safety", "M4", False),
    ChapterSpec("module11", "module11-safety-ethics", "11-3-human-robot-interaction-safety.mdx", "11-3", "HRI Safety", "M4", False),
    ChapterSpec("module11", "module11-safety-ethics", "11-4-ethics-of-autonomous-humanoids.mdx", "11-4", "Ethics", "M4", False),
    ChapterSpec("module11", "module11-safety-ethics", "11-5-privacy-and-data-governance.mdx", "11-5", "Privacy", "M4", False),
    ChapterSpec("module11", "module11-safety-ethics", "11-6-deployment-operations.mdx", "11-6", "Deployment Operations", "M4", False),

    # Module 12: Capstone Projects & Frontiers (6 chapters)
    ChapterSpec("module12", "module12-capstone-frontiers", "12-1-capstone-project-guide.mdx", "12-1", "Capstone Project", "M4", False),
    ChapterSpec("module12", "module12-capstone-frontiers", "12-2-research-frontiers-locomotion.mdx", "12-2", "Research Frontiers", "M4", False),
    ChapterSpec("module12", "module12-capstone-frontiers", "12-3-research-frontiers-ai.mdx", "12-3", "Frontiers in AI", "M4", False),
    ChapterSpec("module12", "module12-capstone-frontiers", "12-4-the-future-of-humanoid-robotics.mdx", "12-4", "Future of Humanoids", "M4", False),
    ChapterSpec("module12", "module12-capstone-frontiers", "12-5-contributing-to-open-source.mdx", "12-5", "Open-Source", "M4", False),
    ChapterSpec("module12", "module12-capstone-frontiers", "12-6-reference-and-bibliography.mdx", "12-6", "Bibliography", "M4", False),
]


def get_all_chapters() -> List[ChapterSpec]:
    return CHAPTERS


def get_chapters_by_module(module_id: str) -> List[ChapterSpec]:
    return [ch for ch in CHAPTERS if ch.module_id == module_id]


def get_all_modules() -> List[ModuleSpec]:
    return MODULES


def get_module_by_id(module_id: str) -> Optional[ModuleSpec]:
    for m in MODULES:
        if m.module_id == module_id:
            return m
    return None
