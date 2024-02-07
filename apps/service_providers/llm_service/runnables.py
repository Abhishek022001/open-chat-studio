from datetime import datetime
from operator import itemgetter
from typing import Any, Dict, List, Literal, Optional

import pytz
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.load import Serializable
from langchain_core.memory import BaseMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain_core.runnables import (
    Runnable,
    RunnableConfig,
    RunnableLambda,
    RunnablePassthrough,
    RunnableSerializable,
    ensure_config,
)

from apps.chat.agent.tools import get_tools
from apps.chat.conversation import compress_chat_history
from apps.chat.models import ChatMessage, ChatMessageType
from apps.experiments.models import Experiment, ExperimentSession


def create_experiment_runnable(experiment: Experiment, session: ExperimentSession = None) -> "ExperimentRunnable":
    """Create an experiment runnable based on the experiment configuration."""
    if experiment.tools_enabled and session:
        return AgentExperimentRunnable(experiment=experiment, session=session)
    else:
        return SimpleExperimentRunnable(experiment=experiment, session=session)


class ChainOutput(Serializable):
    output: str
    """String text."""
    prompt_tokens: int
    """Number of tokens in the prompt."""
    completion_tokens: int
    """Number of tokens in the completion."""

    type: Literal["OcsChainOutput"] = "ChainOutput"

    @classmethod
    def is_lc_serializable(cls) -> bool:
        """Return whether this class is serializable."""
        return True

    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object."""
        return ["ocs", "schema", "chain_output"]


class ExperimentRunnable(RunnableSerializable[Dict, ChainOutput]):
    experiment: Experiment
    session: ExperimentSession
    memory: BaseMemory = ConversationBufferMemory(return_messages=True)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def is_lc_serializable(cls) -> bool:
        return False

    def invoke(self, input: str, config: Optional[RunnableConfig] = None) -> ChainOutput:
        callback = self.callback_handler
        config = ensure_config(config)
        config["callbacks"] = config["callbacks"] or []
        config["callbacks"].append(callback)

        chain = self._build_chain()
        self._populate_memory()

        self._save_message_to_history(input, ChatMessageType.HUMAN)

        output = chain.invoke(input, config)

        self._save_message_to_history(output, ChatMessageType.AI)
        return ChainOutput(
            output=output, prompt_tokens=callback.prompt_tokens, completion_tokens=callback.completion_tokens
        )

    @property
    def llm_service(self):
        return self.experiment.llm_provider.get_llm_service()

    @property
    def source_material(self):
        return self.experiment.source_material.material if self.experiment.source_material else ""

    def _build_chain(self) -> Runnable[Dict[str, Any], str]:
        raise NotImplementedError

    @property
    def callback_handler(self):
        model = self.llm_service.get_chat_model(self.experiment.llm, self.experiment.temperature)
        return self.llm_service.get_callback_handler(model)

    @property
    def prompt(self):
        system_prompt = SystemMessagePromptTemplate.from_template(self.experiment.chatbot_prompt.prompt)
        return ChatPromptTemplate.from_messages(
            [
                system_prompt,
                MessagesPlaceholder("history", optional=True),
                ("human", "{input}"),
            ]
        )

    def format_input(self, input: dict):
        input["input"] = self.experiment.chatbot_prompt.format(input["input"])
        return input

    def _populate_memory(self):
        # TODO: convert to use BaseChatMessageHistory object
        model = self.llm_service.get_chat_model(self.experiment.llm, self.experiment.temperature)
        messages = compress_chat_history(self.session.chat, model, self.experiment.max_token_limit)
        self.memory.chat_memory.messages = messages

    def _save_message_to_history(self, message: str, type_: ChatMessageType):
        ChatMessage.objects.create(
            chat=self.session.chat,
            message_type=type_.value,
            content=message,
        )


class SimpleExperimentRunnable(ExperimentRunnable):
    def _build_chain(self) -> Runnable[Dict[str, Any], str]:
        model = self.llm_service.get_chat_model(self.experiment.llm, self.experiment.temperature)
        return (
            {"input": RunnablePassthrough()}
            | RunnablePassthrough.assign(source_material=RunnableLambda(lambda x: self.source_material))
            | RunnablePassthrough.assign(
                history=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")
            )
            | RunnableLambda(self.format_input)
            | self.prompt
            | model
            | StrOutputParser()
        )


class AgentExperimentRunnable(ExperimentRunnable):
    def _build_chain(self) -> Runnable[Dict[str, Any], str]:
        assert self.experiment.tools_enabled
        model = self.llm_service.get_chat_model(self.experiment.llm, self.experiment.temperature)
        tools = get_tools(self.session)
        # TODO: use https://python.langchain.com/docs/integrations/chat/anthropic_functions
        # when we implement this for anthropic
        agent = (
            RunnablePassthrough.assign(source_material=RunnableLambda(lambda x: self.source_material))
            | RunnableLambda(self.format_input)
            | create_openai_tools_agent(llm=model, tools=tools, prompt=self.prompt)
        )
        executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            memory=self.memory,
            max_execution_time=120,
        )
        return executor | itemgetter("output")

    @property
    def prompt(self):
        prompt = super().prompt
        prompt.extend(
            [
                ("system", str(datetime.now().astimezone(pytz.UTC))),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        return prompt
