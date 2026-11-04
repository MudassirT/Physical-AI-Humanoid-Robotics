# Tasks: Module 2: The Digital Twin (Gazebo & Unity)

**Input**: Design documents from `/specs/003-digital-twin-gazebo-unity/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: The feature specification for Module 2 includes functional tests and does not explicitly request a TDD approach for every component. Therefore, test tasks will focus on integration and end-to-end validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project, as defined in `specs/003-digital-twin-gazebo-unity/plan.md`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for the Digital Twin module

- [ ] T001 Create base project structure for Digital Twin module in `src/gazebo_worlds/`, `src/unity_assets/`, `src/ros2_sim_nodes/`, `src/sim_utils/`, `tests/gazebo_sim/`, `tests/unity_sim/`, `tests/ros2_sim_nodes/`
- [ ] T002 Initialize Python project with ROS 2 (`rclpy`) and other dependencies in `src/` root or shared `requirements.txt`
- [ ] T003 [P] Configure linting and formatting tools for Python and C# codebase

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Setup ROS 2 workspace and necessary environment variables for Digital Twin components
- [ ] T005 Install and configure Gazebo for robotic simulation
- [ ] T006 Install and configure Unity Engine with robotics extensions/integrations

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Setting up Simulation Environments (Priority: P1) 🎯 MVP

**Goal**: Students will learn how to set up and configure Gazebo and Unity for robotic simulation, understanding the fundamental tools for creating digital twins of humanoid robots.

**Independent Test**: Can be fully tested by successfully installing and launching both Gazebo and Unity with their respective robotics extensions/integrations, and verifying basic functionality (e.g., loading a default scene).

### Implementation for User Story 1

- [ ] T007 [US1] Create content for Introduction to Digital Twins in `specs/003-digital-twin-gazebo-unity/content.md`
- [ ] T008 [US1] Create content for Gazebo Simulation Engine (physics, SDF vs URDF, spawning models, physical properties) in `specs/003-digital-twin-gazebo-unity/content.md`
- [ ] T009 [US1] Create content for Unity for High-Fidelity Visuals (role, environment building, ROS-Unity bridge) in `specs/003-digital-twin-gazebo-unity/content.md`
- [ ] T010 [US1] Include architecture diagrams showing simulation workflow in `specs/003-digital-twin-gazebo-unity/content.md`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Simulating Humanoid Robot Sensors (Priority: P1)

**Goal**: Students will understand how to simulate various sensors (LiDAR, Depth Camera, IMU, force-torque) within Gazebo, and how these simulated sensor data can be accessed.

**Independent Test**: Can be fully tested by implementing a Gazebo simulation that includes a humanoid robot with multiple sensors, and successfully visualizing or receiving data from these simulated sensors via ROS 2 topics.

### Implementation for User Story 2

- [ ] T011 [US2] Create content for Sensor Simulation (LiDAR, Depth Camera, IMU, force-torque) in `specs/003-digital-twin-gazebo-unity/content.md`
- [ ] T012 [US2] Implement example Gazebo world with a humanoid robot and simulated LiDAR sensor in `src/gazebo_worlds/robot_with_lidar.world`
- [ ] T013 [US2] Implement example Gazebo world with a humanoid robot and simulated Depth Camera sensor in `src/gazebo_worlds/robot_with_depth_camera.world`
- [ ] T014 [US2] Implement example Gazebo world with a humanoid robot and simulated IMU sensor in `src/gazebo_worlds/robot_with_imu.world`
- [ ] T015 [US2] Create ROS 2 nodes to subscribe to and visualize sensor data in `src/ros2_sim_nodes/sensor_data_visualizer.py`
- [ ] T016 [US2] Create unit tests for sensor data processing in `tests/ros2_sim_nodes/test_sensor_processing.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Building and Interacting with Simulation Scenes (Priority: P2)

**Goal**: Students will learn to build simple simulation scenes in Gazebo and Unity, spawn humanoid robots, and explore the interaction between SDF/URDF and the simulation engine.

**Independent Test**: Can be fully tested by creating a new Gazebo world file, spawning a humanoid robot within it, and observing its physical interaction with the environment (e.g., falling due to gravity, collisions).

### Implementation for User Story 3

- [ ] T017 [US3] Implement Exercise 1: Spawn a humanoid from URDF into Gazebo in `src/gazebo_worlds/spawn_humanoid_exercise.world` and `src/gazebo_worlds/humanoid.urdf`
- [ ] T018 [US3] Implement Exercise 2: Simulate a room, add LiDAR + IMU, visualize sensor topics in `src/gazebo_worlds/room_with_sensors.world`
- [ ] T019 [US3] Implement Bonus Exercise: Create a Unity scene & link to ROS 2 in `src/unity_assets/ROS2UnityScene/`
- [ ] T020 [US3] Create integration tests for Gazebo environment setup and physics in `tests/gazebo_sim/test_environment_physics.py`
- [ ] T021 [US3] Create integration tests for Unity scene interaction and ROS-Unity bridge in `tests/unity_sim/test_ros2_unity_bridge.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T022 Integrate full Digital Twin pipeline components (Gazebo, Unity, ROS 2) in `src/sim_utils/full_digital_twin_pipeline.py`
- [ ] T023 Create comprehensive demo scripts for the entire Digital Twin system, including visualization if applicable, in `src/sim_utils/run_digital_twin_demo.py`
- [ ] T024 [P] Add end-to-end (E2E) tests for the complete Digital Twin pipeline in `tests/unity_sim/test_digital_twin_e2e.py`
- [ ] T025 Documentation updates for Digital Twin module (e.g., `README.md` in `specs/003-digital-twin-gazebo-unity/` and `src/`)
- [ ] T026 Code cleanup, refactoring, and adherence to style guides across all Digital Twin components

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (P1) and User Story 2 (P1) can proceed in parallel (if staffed)
  - User Story 3 (P2) depends on User Story 2 for sensor simulation capabilities.
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on User Story 1, but builds upon environment setup.
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on User Story 2 for integrating simulated sensors into scenes.

### Within Each User Story

- Tasks within a story follow a logical progression (e.g., content creation before code implementation, code before tests).
- Tests (if included) should ideally be written before implementation, but for this module, they are focused on validation after core logic.

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel.
- Tasks within User Story 1 (P1) can have some parallel aspects (e.g., content creation).
- Tasks within User Story 2 (P1) can have some parallel aspects.
- User Story 1 and User Story 2 can be worked on in parallel by different team members.
- Tasks within User Story 3 (P2) can have some parallel aspects.
- Tasks within the Polish phase marked [P] can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3 (dependent on US2, so B needs to finish core US2 first)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests (especially E2E) after implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
