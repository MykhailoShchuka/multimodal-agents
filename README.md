# 👨‍💻 Multimodal-agency

Fully open sourced version of Claude Code built with [Agency Swarm](https://agency-swarm.ai/welcome/overview) framework.

## 🔥 Key features

- **Developer Agent (AgencyCodeAgent)**: Full code editing, search, git, bash, and notebook tools.
- **QA Agent**: Selenium-powered browser automation for DOM discovery, interaction, screenshots.
- **Data Analyst Agent**: Plotting and dashboard screenshot tools for quick analysis tasks.
- **Ad Creator Agent**: Image generation and editing utilities for creative tasks.
- **Cross-agent handoff**: Built-in coder → QA communication flow in the orchestrator.
- **Multi-provider models**: Switch between OpenAI, Anthropic, Gemini, and Grok via LiteLLM.

👨‍💻 Additionally, you can experiment with Agency Swarm features like multi-level hybrid communication flows.

## 🧩 Agents & Roles
- `AgencyCodeAgent` (developer): primary CLI-focused coder with toolbelt under `agency_code_agent/tools/`.
- `QAAgent`: web QA/testing with Selenium; artifacts saved to `qa_agent/screenshots/`.
- `DataAnalystAgent`: plotting and page screenshot tooling; artifacts in `data_analyst_agent/screenshots/`.
- `AdCreatorAgent`: image generation/editing utilities.

The entrypoint `agency.py` loads `.env`, selects the model (default `gpt-5`), creates agents, wires coder → QA communication, and launches the terminal demo.

## 🚀 Quick start

1. Create and activate a virtual environment (Python 3.13), then install deps:

   ```
   python3.13 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

   > ⚠️ There is currently a bug in LiteLLM with Anthropic reasoning models.  
   > To fix this, after installing the requirements, run:
   >
   > ```
   > python -m pip install git+https://github.com/openai/openai-agents-python.git@main
   > ```

2. Try the agency (terminal demo):

   macOS:

   ```
   sudo python agency.py
   ```

   Windows/Linux:

   ```
   python agency.py
   ```

- Don't forget to run the command with sudo if you're on macOS.
- The agent won't be able to edit files outside of your current directory.

## ⚙️ Models & Configuration
- Select your model in `agency.py` (default: `gpt-5`).
- `litellm_config.yaml` defines supported providers/models and reads keys from env vars:
  - `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `XAI_API_KEY`
- Put secrets in `.env` (not committed); `dotenv` is loaded in `agency.py`.
- Model behavior is standardized via `shared/agent_utils.py` (instructions selection, reasoning settings, provider extras).

## 🛠️ Agents & Tools
- Developer toolbelt (`agency_code_agent/tools/`): filesystem and code editors (`Read`, `Write`, `Edit`, `MultiEdit`, notebooks), search (`Glob`, `Grep`, `LS`), ops (`Bash`, `Git`, `TodoWrite`, `ExitPlanMode`).
- Web search: `agents.WebSearchTool` when using OpenAI models; `ClaudeWebSearch` when using Anthropic models.
- QA tools (`qa_agent/tools/`): DOM discovery, interaction, screenshots (Selenium + `webdriver-manager`).
- Data analyst tools (`data_analyst_agent/tools/`): `plot_chart.py`, `get_page_screenshot.py`.
- Ad creator tools (`ad_creator_agent/tools/`): `generate_image.py`, `edit_image.py`, `combine_images.py`.

## 🔧 Adding Agents
- Create a new folder mirroring an existing agent (e.g., `qa_agent/`), including an `instructions.md`, a `tools/` folder (optional), and a factory like `create_<agent_name>(model, reasoning_effort)`.
- Wire it in `agency.py` (instantiate, add to `Agency(...)`, and optionally add communication flows).
- Keep naming/style consistent with existing agents; see `AGENTS.md` for details.

## 🧹 Linting & Formatting
- Pre-commit hooks are configured. Run:

  ```
  pre-commit run --all-files
  ```

- If using Ruff locally, format with:

  ```
  ruff check . --fix
  ruff format .
  ```

## 📝 Demo Tasks

### 🎨 Website development

```
Create a shared pixel art canvas like r/place using Next.js and Socket.io:

- 50x50 grid where each player can color one pixel at a time
- 16 color palette at the bottom
- See other players' cursors moving in real-time with their names
- 5-second cooldown between placing pixels (show countdown on cursor)
- Minimap in corner showing full canvas
- Chat box for players to coordinate
- Download canvas as image button
- Show "Player X placed a pixel" notifications
- Persist canvas state in JSON file
- Mobile friendly with pinch to zoom

Simple and fun - just a shared canvas everyone can draw on together. Add rainbow gradient background.

Ask QA agent to perform a qa once finished developing.
```

### 🖼️ Ad creative generation (real-world example)

```
Create an ad creative package for a new product, then generate its logo.

Product: "Lumos LED Desk Lamp" — dimmable, eye-care desk lamp with adjustable color temperature.

- Ad requirements:
  - Produce an ad post highlighting eye-care LEDs, stepless dimming, and 4 color temps (warm to cool).
  - Add a short tagline "Bright Ideas, Gentle on Eyes".

- Logo requirements:
  - Generate a 1024x1024 logo for Lumos with a clean, modern aesthetic.
  - Use a palette of cool white (#F5F8FF), slate gray (#2A2F3A), and electric blue accent (#2D7DFF); prefer a minimal vector lamp/beam motif.
```

### 📈 Data analysis and visualization

```
Analyze my dashboard: [DASHBOARD_VIEW_URL] and provide insides on the current performance. Extract hidden trends and build a graph for future estimates.
```
