from typing_extensions import TypeAliasType

HistoryName = TypeAliasType("HistoryName", str)
HistoryType = TypeAliasType("HistoryType", str)
Keywords = TypeAliasType("Keywords", list)
LlmProviderId = TypeAliasType("LlmProviderId", int)
LlmProviderModelId = TypeAliasType("LlmProviderModelId", int)
LlmTemperature = TypeAliasType("LlmTemperature", float)
NumOutputs = TypeAliasType("NumOutputs", int)
SourceMaterialId = TypeAliasType("SourceMaterialId", int)
ExpandableText = TypeAliasType("ExpandableText", str)
AssistantId = TypeAliasType("AssistantId", int)
ToggleField = TypeAliasType("ToggleField", bool)
InternalToolsField = TypeAliasType("InternalToolsField", list[str])
