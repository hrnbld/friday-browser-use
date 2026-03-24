"""
Session management for persistent browser states
"""

import json
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Session:
    """
    Browser session with persistent state.
    
    Usage:
        session = Session("chrome")
        await session.apply_to_context(context)
        session.save()
    """
    
    name: str = "default"
    cookies: list = field(default_factory=list)
    local_storage: Dict[str, str] = field(default_factory=dict)
    session_storage: Dict[str, str] = field(default_factory=dict)
    viewport: Optional[Dict] = None
    user_agent: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    
    _storage_dir: Path = Path("~/.browser-use/sessions").expanduser()
    
    def __post_init__(self):
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        
    @property
    def storage_path(self) -> Path:
        return self._storage_dir / f"{self.name}.json"
    
    def save(self, name: Optional[str] = None):
        """Save session state to file"""
        if name:
            self.name = name
            
        data = {
            "name": self.name,
            "cookies": self.cookies,
            "local_storage": self.local_storage,
            "session_storage": self.session_storage,
            "viewport": self.viewport,
            "user_agent": self.user_agent,
            "headers": self.headers
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        return self.storage_path
    
    def load(self, name: Optional[str] = None):
        """Load session state from file"""
        if name:
            self.name = name
            
        if not self.storage_path.exists():
            return None
            
        with open(self.storage_path, 'r') as f:
            data = json.load(f)
            
        self.cookies = data.get("cookies", [])
        self.local_storage = data.get("local_storage", {})
        self.session_storage = data.get("session_storage", {})
        self.viewport = data.get("viewport")
        self.user_agent = data.get("user_agent")
        self.headers = data.get("headers", {})
        
        return self
    
    async def apply_to_context(self, context):
        """Apply session state to Playwright context"""
        # Add cookies
        if self.cookies:
            await context.add_cookies(self.cookies)
            
        # Set viewport
        if self.viewport:
            await context.set_viewport_size(**self.viewport)
            
        # Set extra HTTP headers
        if self.headers:
            await context.set_extra_http_headers(self.headers)
            
        return context
    
    @classmethod
    def list_sessions(cls) -> list:
        """List all saved sessions"""
        storage_dir = Path("~/.browser-use/sessions").expanduser()
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        return [p.stem for p in storage_dir.glob("*.json")]
    
    @classmethod
    def load_from_storage(cls, name: str) -> "Session":
        """Load session from storage by name"""
        session = cls(name=name)
        return session.load()
    
    def clear(self):
        """Clear session data"""
        self.cookies = []
        self.local_storage = {}
        self.session_storage = {}
        
        if self.storage_path.exists():
            self.storage_path.unlink()


class SessionManager:
    """Manage multiple sessions"""
    
    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or Path("~/.browser-use/sessions").expanduser()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._sessions: Dict[str, Session] = {}
        
    def create_session(self, name: str) -> Session:
        """Create new session"""
        session = Session(name=name)
        self._sessions[name] = session
        return session
    
    def get_session(self, name: str) -> Optional[Session]:
        """Get session by name"""
        if name not in self._sessions:
            session = Session(name=name)
            if session.storage_path.exists():
                session.load()
            self._sessions[name] = session
        return self._sessions[name]
    
    def delete_session(self, name: str):
        """Delete session"""
        if name in self._sessions:
            del self._sessions[name]
            
        session = Session(name=name)
        if session.storage_path.exists():
            session.storage_path.unlink()
            
    def list_sessions(self) -> list:
        """List all sessions"""
        return Session.list_sessions()
