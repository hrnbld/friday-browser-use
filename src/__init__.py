"""
Browser Use Clone - Friday AI Edition
AI-native browser automation with structured output
"""

from .browser_agent import BrowserAgent
from .session import Session
from .schema import extract_schema

__all__ = ["BrowserAgent", "Session", "extract_schema"]
