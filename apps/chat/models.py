import logging
from enum import StrEnum
from functools import cache
from urllib.parse import quote

from django.db import models
from django.utils.functional import classproperty
from langchain.schema import BaseMessage, messages_from_dict

from apps.annotations.models import TaggedModelMixin, UserCommentsMixin
from apps.files.models import File
from apps.teams.models import BaseTeamModel
from apps.utils.models import BaseModel

logger = logging.getLogger(__name__)


class Chat(BaseTeamModel, TaggedModelMixin, UserCommentsMixin):
    """
    A chat instance.
    """

    class MetadataKeys(StrEnum):
        OPENAI_THREAD_ID = "openai_thread_id"

    # must match or be greater than experiment name field
    name = models.CharField(max_length=128, default="Unnamed Chat")
    metadata = models.JSONField(default=dict)

    def get_metadata(self, key: MetadataKeys):
        return self.metadata.get(key, None)

    def set_metadata(self, key: MetadataKeys, value, commit=True):
        self.metadata[key] = value
        if commit:
            self.save()

    def get_langchain_messages(self) -> list[BaseMessage]:
        return messages_from_dict([m.to_langchain_dict() for m in self.messages.all()])

    def get_langchain_messages_until_summary(self) -> list[BaseMessage]:
        messages = []
        for message in self.message_iterator():
            messages.append(message.to_langchain_dict())
            if message.is_summary:
                break

        return messages_from_dict(list(reversed(messages)))

    def message_iterator(self):
        for message in self.messages.order_by("-created_at").iterator(100):
            yield message
            if message.summary:
                yield message.get_summary_message()

    @cache
    def get_attached_files(self):
        return list(File.objects.filter(chatattachment__chat=self))


class ChatMessageType(models.TextChoices):
    #  these must correspond to the langchain values
    HUMAN = "human", "Human"
    AI = "ai", "AI"
    SYSTEM = "system", "System"

    @classproperty
    def safety_layer_choices(cls):
        return (
            (choice[0], f"{choice[1]} messages")
            for choice in ChatMessageType.choices
            if choice[0] != ChatMessageType.SYSTEM
        )

    @staticmethod
    def from_role(role: str):
        return {
            "user": ChatMessageType.HUMAN,
            "assistant": ChatMessageType.AI,
            "system": ChatMessageType.SYSTEM,
        }[role]

    @property
    def role(self):
        return {
            ChatMessageType.HUMAN: "user",
            ChatMessageType.AI: "assistant",
            ChatMessageType.SYSTEM: "system",
        }[self]


class ChatMessage(BaseModel, TaggedModelMixin, UserCommentsMixin):
    """
    A message in a chat. Analogous to the BaseMessage class in langchain.
    """

    # Metadata keys that should be excluded from the API response
    INTERNAL_METADATA_KEYS = {
        "openai_file_ids",
    }

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    message_type = models.CharField(max_length=10, choices=ChatMessageType.choices)
    content = models.TextField()
    summary = models.TextField(  # noqa DJ001
        null=True, blank=True, help_text="The summary of the conversation up to this point (not including this message)"
    )
    metadata = models.JSONField(default=dict)

    class Meta:
        ordering = ["created_at"]

    @classmethod
    def make_summary_message(cls, message):
        """A 'summary message' is a special message only ever exists in memory. It is
        not saved to the database. It is used to represent the summary of a chat up to a certain point."""
        return ChatMessage(
            created_at=message.created_at,
            message_type=ChatMessageType.SYSTEM,
            content=message.content,
            metadata={"is_summary": True},
        )

    def save(self, *args, **kwargs):
        if self.is_summary:
            raise ValueError("Cannot save a summary message")
        super().save(*args, **kwargs)

    def get_summary_message(self):
        if not self.summary:
            raise ValueError("Message does not have a summary")
        return ChatMessage.make_summary_message(self)

    @property
    def is_ai_message(self):
        return self.message_type == ChatMessageType.AI

    @property
    def is_human_message(self):
        return self.message_type == ChatMessageType.HUMAN

    @property
    def is_summary(self):
        return self.metadata.get("is_summary", False)

    @property
    def created_at_datetime(self):
        return quote(self.created_at.isoformat())

    def to_langchain_dict(self) -> dict:
        return self._get_langchain_dict(self.content, self.message_type)

    def to_langchain_message(self) -> BaseMessage:
        return messages_from_dict([self.to_langchain_dict()])[0]

    def _get_langchain_dict(self, content, message_type):
        return {
            "type": message_type,
            "data": {
                "content": content,
                "additional_kwargs": {
                    "id": self.id,
                },
            },
        }

    def get_attached_files(self):
        """For display purposes. Returns the tool resource files for which this message has references to. The
        reference will be the file's external id

        Message metadata example:
        {
            "openai_file_ids": ["file_id_1", "file_id_2", ...]
        }
        """
        if file_ids := self.metadata.get("openai_file_ids", []):
            # We should not show files that are on the assistant level. Users should only be able to download
            # those on the thread (chat) level, since they uploaded them
            return [file for file in self.chat.get_attached_files() if file.external_id in file_ids]
        return []


class ChatAttachment(BaseModel):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="attachments")
    tool_type = models.CharField(max_length=128)
    files = models.ManyToManyField("files.File", blank=True)
    extra = models.JSONField(default=dict, blank=True)

    @property
    def label(self):
        return self.tool_type.replace("_", " ").title()

    def __str__(self):
        return f"Tool Resources for chat {self.chat.id}: {self.tool_type}"
