#!/usr/bin/env python3
"""
E2E Dual-Track Test Suite Runner.

Orchestrates execution of the 4-tier testing infrastructure for the
12-Module Humanoid Robotics Textbook & Platform.

Usage:
    python run_e2e_tests.py [--all] [--tier {1,2,3,4}] [--curriculum-only] [--backend-only] [--strict-110]
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


def get_backend_dir() -> Path:
    root = Path(__file__).resolve().parent
    backend = root / "backend"
    if not backend.exists():
        sys.exit(f"Error: backend directory not found at {backend}")
    return backend


def run_pytest_command(args: list[str], env_vars: dict = None) -> int:
    backend_dir = get_backend_dir()
    cmd = ["uv", "run", "pytest"] + args
    
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    print(f"\n[E2E Runner] Executing: {' '.join(cmd)}")
    print(f"[E2E Runner] Working directory: {backend_dir}")
    print("-" * 75)
    
    start_time = time.time()
    result = subprocess.run(cmd, cwd=str(backend_dir), env=env)
    elapsed = time.time() - start_time
    
    print("-" * 75)
    print(f"[E2E Runner] Completed in {elapsed:.2f}s with exit code {result.returncode}")
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Dual-Track E2E Test Suite Runner for Humanoid Robotics Curriculum & Platform"
    )
    parser.add_argument(
        "--all", action="store_true", default=True, help="Run all 4 tiers of E2E tests (default)"
    )
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3, 4],
        help="Run only tests from a specific tier (1, 2, 3, or 4)",
    )
    parser.add_argument(
        "--curriculum-only",
        action="store_true",
        help="Run only Curriculum Track tests (frontmatter, math, links, directory layout)",
    )
    parser.add_argument(
        "--backend-only",
        action="store_true",
        help="Run only Platform/Backend Track tests (endpoints, streaming, analytics, filtering)",
    )
    parser.add_argument(
        "--strict-110",
        action="store_true",
        help="Enforce strict presence of all 110 chapters (Milestone 5 final release gate)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=True, help="Enable verbose pytest output"
    )

    args = parser.parse_args()

    pytest_args = []
    if args.verbose:
        pytest_args.append("-v")

    env_vars = {}
    if args.strict_110:
        env_vars["STRICT_110"] = "1"
        print("[E2E Runner] STRICT_110 mode enabled: all 110 chapters must be present!")

    if args.tier == 1:
        pytest_args.extend([
            "tests/e2e/test_tier1_curriculum_coverage.py",
            "tests/e2e/test_tier1_backend_coverage.py",
        ])
    elif args.tier == 2:
        pytest_args.append("tests/e2e/test_tier2_boundary_corner_cases.py")
    elif args.tier == 3:
        pytest_args.append("tests/e2e/test_tier3_cross_feature_interactions.py")
    elif args.tier == 4:
        pytest_args.append("tests/e2e/test_tier4_real_world_scenarios.py")
    elif args.curriculum_only:
        pytest_args.extend([
            "tests/e2e/test_tier1_curriculum_coverage.py",
            "tests/e2e/test_tier2_boundary_corner_cases.py::TestTier2BoundaryCornerCases::test_complex_latex_syntax_integrity",
            "tests/e2e/test_tier2_boundary_corner_cases.py::TestTier2BoundaryCornerCases::test_no_unescaped_jsx_curlys_in_text",
            "tests/e2e/test_tier4_real_world_scenarios.py::TestTier4RealWorldScenarios::test_curriculum_wide_internal_link_resolution",
            "tests/e2e/test_tier4_real_world_scenarios.py::TestTier4RealWorldScenarios::test_module_directory_layout_compliance",
        ])
    elif args.backend_only:
        pytest_args.extend([
            "tests/e2e/test_tier1_backend_coverage.py",
            "tests/e2e/test_tier2_boundary_corner_cases.py::TestTier2BoundaryCornerCases::test_ask_empty_query_rejected",
            "tests/e2e/test_tier2_boundary_corner_cases.py::TestTier2BoundaryCornerCases::test_ask_missing_field_rejected",
            "tests/e2e/test_tier2_boundary_corner_cases.py::TestTier2BoundaryCornerCases::test_ask_ultra_long_query_handled",
            "tests/e2e/test_tier2_boundary_corner_cases.py::TestTier2BoundaryCornerCases::test_ask_unknown_module_filter",
            "tests/e2e/test_tier2_boundary_corner_cases.py::TestTier2BoundaryCornerCases::test_analytics_invalid_payload_rejected",
            "tests/e2e/test_tier2_boundary_corner_cases.py::TestTier2BoundaryCornerCases::test_concurrent_analytics_logging_integrity",
            "tests/e2e/test_tier3_cross_feature_interactions.py",
            "tests/e2e/test_tier4_real_world_scenarios.py::TestTier4RealWorldScenarios::test_end_to_end_question_answering_pipeline_simulation",
        ])
    else:
        # Default: run all tests in tests/e2e
        pytest_args.append("tests/e2e")

    exit_code = run_pytest_command(pytest_args, env_vars=env_vars)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
