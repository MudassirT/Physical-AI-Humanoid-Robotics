# Contributing to Physical AI & Humanoid Robotics

Thank you for your interest in contributing! This project is an open-source, graduate- and industry-grade reference textbook and RAG system for **Physical AI & Humanoid Robotics**.

We welcome contributions from robotics researchers, systems engineers, and AI practitioners.

---

## Code of Conduct

All contributors and maintainers are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to the project maintainers.

---

## Development Workflow

### 1. Branching Strategy
- `main`: Production-ready, deployable branch. All PRs target `main`.
- Feature branches: `feat/<feature-name>`, `fix/<bug-description>`, `docs/<chapter-or-module>`.

### 2. Commit Message Standards (Conventional Commits)
We enforce the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/) specification:

```text
<type>(<scope>): <short summary>

[optional body]

[optional footer(s)]
```

Common types:
- `feat`: A new feature (e.g. `feat(chat): add streaming message support`)
- `fix`: A bug fix (e.g. `fix(theme): prevent toggle state desync on rapid click`)
- `docs`: Documentation and curriculum changes (e.g. `docs(m3): expand Isaac cuVSLAM chapter`)
- `refactor`: Code changes that neither fix a bug nor add a feature
- `test`: Adding or updating test suites
- `chore`: Maintenance tasks, dependency bumps, configuration updates

---

## Local Setup & Verification

### Frontend (Docusaurus)
```bash
# Install dependencies
npm install

# Start development server
npm start

# Verify production build before committing
npm run build
```

### Backend (FastAPI + Qdrant RAG)
```bash
cd backend

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Run test suite
pytest

# Code quality check
ruff check .
```

### Documentation Ingestion Pipeline
When updating or adding chapters in `ai-book-docs/`, re-index the vector database:
```bash
cd backend
python ingest_docs.py
```

---

## Submitting a Pull Request

1. Fork the repository and create your branch from `main`.
2. Ensure both `npm run build` and `pytest` pass with **zero errors**.
3. Verify that your MDX documentation compiles cleanly with proper formatting (no unescaped math tags or broken links).
4. Submit your Pull Request using the provided [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md).
5. A maintainer will review your submission and provide feedback.
