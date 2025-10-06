import os

from shared.utils import silence_warnings_and_logs

silence_warnings_and_logs()

import litellm  # noqa: E402 - must import after warning suppression
from agency_swarm import Agency  # noqa: E402 - must import after warning suppression
from dotenv import load_dotenv  # noqa: E402 - must import after warning suppression

from agency_code_agent.agency_code_agent import (  # noqa: E402 - must import after warning suppression
    create_agency_code_agent,
)

from qa_agent.qa_agent import (  # noqa: E402 - must import after warning suppression
    create_qa_agent,
)

from data_analyst_agent.data_analyst_agent import (  # noqa: E402 - must import after warning suppression
    create_data_analyst_agent,
)

from ad_creator_agent.ad_creator_agent import (  # noqa: E402 - must import after warning suppression
    create_ad_creator,
)

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
litellm.modify_params = True

# switch between models here
# model = "anthropic/claude-sonnet-4-20250514"
model = "gpt-5"
# coder = create_agency_code_agent(model="gpt-5", reasoning_effort="high")
coder = create_agency_code_agent(
    model=model, reasoning_effort="high"
)

qa = create_qa_agent(model=model, reasoning_effort="medium")

data_analyst = create_data_analyst_agent(model=model, reasoning_effort="medium")

ad_creator = create_ad_creator(model=model, reasoning_effort="medium")

agency = Agency(
    coder, data_analyst, ad_creator,
    name="AgencyCode",
    communication_flows=[
        (coder, qa),
    ],
)

if __name__ == "__main__":
    # from tools.bash import Bash
    # bash = Bash(command="npm run dev --prefix \"D:\\work\\VRSEN\\code\\multimodal-agents\\Agency-Code\\rplace\"", background=True)
    # print("Starting development server in background...")
    # print(bash.run())
    # print("Server started! Agent can now continue with other tasks.")
    # while True:
    #     pass
    
    # Uncomment the line below to run the agency terminal demo
    agency.terminal_demo(show_reasoning=False if model.startswith("anthropic") else True)
    # agency.visualize()
