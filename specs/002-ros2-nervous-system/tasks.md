# Tasks: Module 1: The Robotic Nervous System (ROS 2)

**Input**: Design documents from `/specs/002-ros2-nervous-system/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: The feature specification for Module 1 includes functional tests and does not explicitly request a TDD approach for every component. Therefore, test tasks will focus on integration and end-to-end validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project, as defined in `specs/002-ros2-nervous-system/plan.md`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for the ROS 2 module

- [ ] T001 Create base project structure for ROS 2 module in `src/ros2_nodes/`, `src/urdf_models/`, `src/simulation_scripts/`, `tests/ros2_nodes/`, `tests/urdf_models/`, `tests/simulation/`
- [ ] T002 Initialize Python project with ROS 2 (`rclpy`) and other dependencies in `src/` root or shared `requirements.txt`
- [ ] T003 [P] Configure linting and formatting tools for Python codebase

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Setup ROS 2 workspace and necessary environment variables for ROS 2 components

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Understanding ROS 2 Fundamentals (Priority: P1) 🎯 MVP

**Goal**: Students will learn the core concepts of ROS 2, including its architecture and how it differs from ROS 1, specifically in the context of humanoid robotics.

**Independent Test**: Can be fully tested by reviewing the theoretical explanations and answering conceptual questions based on the provided content.

### Implementation for User Story 1

- [ ] T005 [US1] Create content for Introduction to ROS 2 in `specs/002-ros2-nervous-system/content.md`
- [ ] T006 [US1] Create content for ROS 2 Architecture (Nodes, Topics, Services, Actions, Message types, communication patterns, diagrams) in `specs/002-ros2-nervous-system/content.md`
- [ ] T007 [US1] Include example diagrams showing node communication in `specs/002-ros2-nervous-system/content.md`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Developing ROS 2 Python Nodes (Priority: P1)

**Goal**: Students will gain practical experience in setting up a ROS 2 workspace and writing simple Python nodes to control a robot joint.

**Independent Test**: Can be fully tested by successfully implementing and running the provided publisher/subscriber demo, demonstrating a functional ROS 2 node.

### Implementation for User Story 2

- [ ] T008 [US2] Create ROS 2 Python programming section in `specs/002-ros2-nervous-system/content.md`
- [ ] T009 [US2] Implement setup of ROS 2 workspace and writing simple Python nodes using `rclpy` in `src/ros2_nodes/` (e.g., `src/ros2_nodes/simple_publisher.py`, `src/ros2_nodes/simple_subscriber.py`)
- [ ] T010 [US2] Implement publisher/subscriber demo with a robot joint in `src/ros2_nodes/joint_publisher.py` and `src/ros2_nodes/joint_subscriber.py`
- [ ] T011 [US2] Create a unit test for ROS 2 nodes in `tests/ros2_nodes/test_simple_nodes.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Defining Humanoid Robots with URDF (Priority: P2)

**Goal**: Students will understand how to define the physical structure of humanoid robots using URDF.

**Independent Test**: Can be fully tested by successfully interpreting and modifying a sample URDF snippet to represent a different humanoid arm configuration.

### Implementation for User Story 3

- [ ] T012 [US3] Create content for Understanding URDF for Humanoids in `specs/002-ros2-nervous-system/content.md`
- [ ] T013 [US3] Create sample URDF snippet for a humanoid arm in `src/urdf_models/humanoid_arm.urdf`
- [ ] T014 [US3] Implement Exercise 1: Create a ROS 2 node that controls a joint in `src/ros2_nodes/joint_controller_exercise.py`
- [ ] T015 [US3] Implement Exercise 2: Simulate a humanoid joint movement in Gazebo using URDF in `src/simulation_scripts/gazebo_joint_sim.py` and `src/urdf_models/simulated_robot.urdf`
- [ ] T016 [US3] Create validation tests for URDF models and simulation setup in `tests/urdf_models/test_humanoid_arm.py` and `tests/simulation/test_gazebo_sim.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T017 Integrate full ROS 2 pipeline components in `src/simulation_scripts/full_ros2_pipeline.py`
- [ ] T018 Create comprehensive demo scripts for the entire ROS 2 system, including visualization if applicable, in `src/simulation_scripts/run_ros2_demo.py`
- [ ] T019 [P] Add end-to-end (E2E) tests for the complete ROS 2 pipeline (e.g., joint command -> simulated movement) in `tests/simulation/test_ros2_e2e.py`
- [ ] T020 Documentation updates for ROS 2 module (e.g., `README.md` in `specs/002-ros2-nervous-system/` and `src/`)
- [ ] T021 Code cleanup, refactoring, and adherence to style guides across all ROS 2 components

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (P1) and User Story 2 (P1) can proceed in parallel (if staffed)
  - User Story 3 (P2) depends on User Story 2 for joint control mechanisms.
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on User Story 1, but builds upon basic ROS 2 knowledge.
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on User Story 2 for creating and controlling joints.

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
