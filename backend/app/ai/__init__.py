"""
AI 模块 - 基于 Langchain
"""
from .chains import OrderAnalysisChain, DelegationAssistant
from .prompts import ORDER_ANALYSIS_PROMPT, DELEGATION_ADVICE_PROMPT

__all__ = [
    "OrderAnalysisChain",
    "DelegationAssistant",
    "ORDER_ANALYSIS_PROMPT",
    "DELEGATION_ADVICE_PROMPT"
]
