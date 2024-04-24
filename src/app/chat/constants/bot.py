from enum import StrEnum


class BotType(StrEnum):
    MISTRAL = "mistral"
    LLAMA = "llama"
    PHI = "phi"


class BotModel(StrEnum):
    MISTRAL7 = "Mistral-7B-Instruct-v0.2"
    LLAMA3 = "Meta-Llama-3-8B-Instruct"
    PHI2 = "Microsoft-Phi-2.Q4"


class BotStatus(StrEnum):
    INACTIVE = "inactive"
    ACTIVE = "active"
