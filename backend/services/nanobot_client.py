"""StellarPulse - Nanobot Client."""

import asyncio
from typing import Optional


class NanobotClient:
    """Nanobot client for AI interactions."""

    def __init__(self, config_path: Optional[str] = None, workspace: Optional[str] = None):
        self.config_path = config_path
        self.workspace = workspace
        self._agent_loop = None

    async def chat(self, message: str, session_id: str = "stellar:direct") -> str:
        """Send message to nanobot."""
        try:
            # Try to use actual nanobot
            from nanobot.config.loader import load_config
            from nanobot.bus.queue import MessageBus
            from nanobot.providers.litellm_provider import LiteLLMProvider
            from nanobot.agent.loop import AgentLoop
            from nanobot.session.manager import SessionManager

            config = load_config()

            # Create provider
            p = config.get_provider()
            if not p or not p.api_key:
                return "Error: No API key configured in nanobot. Please set it in ~/.nanobot/config.json"

            provider = LiteLLMProvider(
                api_key=p.api_key,
                api_base=config.get_api_base(),
                default_model=config.agents.defaults.model,
                provider_name=config.get_provider_name(),
            )

            bus = MessageBus()
            session_manager = SessionManager(config.workspace_path)

            agent = AgentLoop(
                bus=bus,
                provider=provider,
                workspace=config.workspace_path,
                model=config.agents.defaults.model,
                temperature=config.agents.defaults.temperature,
                max_tokens=config.agents.defaults.max_tokens,
                max_iterations=config.agents.defaults.max_tool_iterations,
                memory_window=config.agents.defaults.memory_window,
                session_manager=session_manager,
            )

            response = await agent.process_direct(message, session_key=session_id)
            return response or "No response"

        except ImportError:
            return "Error: nanobot not installed. Install with: pip install nanobot-ai"
        except Exception as e:
            return f"Error: {str(e)}"


async def chat_with_nanobot(message: str, session_id: str = "stellar:direct") -> str:
    """Chat with nanobot."""
    client = NanobotClient()
    return await client.chat(message, session_id)
