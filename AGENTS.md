# Repository Guidelines

## Project Structure & Roles
- `agency.py` is the single entry point. It loads `.env`, selects a model, instantiates agents, defines cross-agent communication, and launches the terminal demo.
- `agency_code_agent/` hosts the primary developer agent (AgencyCodeAgent), its instruction templates (`instructions.md`, `instructions-gpt-5.md`), and a full toolbelt under `tools/`.
- `qa_agent/` provides a web QA/testing agent with Selenium-powered browser utilities and screenshot capture.
- `data_analyst_agent/` provides a data analysis/visualization agent, including plotting and page screenshot tools.
- `ad_creator_agent/` provides a creative agent for image/logo generation and editing.
- `shared/` includes model-selection utilities, instruction rendering, and system hooks reused across agents.

## Setup & Running
- Create a Python 3.13 virtual environment and install requirements:
  - `python3.13 -m venv .venv && source .venv/bin/activate`
  - `python -m pip install --upgrade pip`
  - `python -m pip install -r requirements.txt`
- Known LiteLLM/Anthropic note (from `README.md`):
  - `python -m pip install git+https://github.com/openai/openai-agents-python.git@main`
- Set required API keys in `.env` (see “Models & Configuration”).
- Launch the interactive demo:
  - macOS: `sudo python agency.py` (sudo required for some filesystem operations)
  - Windows/Linux: `python agency.py`

## Coding Style & Naming Conventions
- Use 4-space indentation, targeted type hints, and docstrings on public agent or tool factories.
- Files remain snake_case, classes PascalCase, and instruction templates stay under `agency_code_agent/`.
- Ruff owns linting and formatting (`ruff check . --fix`, `ruff format .`); expose `create_*` factories for new agents, hooks, or tools.

## Testing Guidelines
- Pytest with `pytest-asyncio` powers the suite; new files follow `test_<area>.py` and mark async cases with `@pytest.mark.asyncio`.
- Reuse fixtures from `tests/conftest.py`, and extend `tests/test_tool_integration.py` for orchestration coverage.
- Exercise both success and failure paths for any tool or planner change, and add regression tests when fixing bugs.

## Commit & Pull Request Guidelines
- Keep commit titles short and descriptive (e.g., `Enable reasoning effort for anthropic models`), using the imperative mood where possible.
- Group related edits, call out instruction or template updates in the PR description, and list the verification commands you ran.
- Reference issues or tasks and include terminal output or screenshots when UX or agent behaviour changes.

## Configuration & Secrets
- Store provider keys and model overrides in `.env`; `dotenv` loads them in `agency.py`, so never commit secrets.
- Document new environment variables in `README.md`, and update both agent factories when introducing models or reasoning modes.
