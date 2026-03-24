"""
BrowserAgent - Main class for AI-native browser automation
"""

import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass

# Handle imports
try:
    from playwright.async_api import async_playwright, Page, Browser, Playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# Try relative imports first, fallback to absolute
try:
    from .session import Session
    from .schema import SchemaExtractor
except ImportError:
    from session import Session
    from schema import SchemaExtractor


@dataclass
class BrowserResult:
    """Result from browser task"""
    output: Any
    success: bool
    error: Optional[str] = None
    metadata: Optional[Dict] = None


class BrowserAgent:
    """
    AI-native browser automation agent.
    """
    
    def __init__(
        self,
        session: Optional[Session] = None,
        headless: bool = False,
        stealth: bool = True,
        timeout: int = 30000,
        model: str = "minimax-m2.7:cloud"
    ):
        self.session = session
        self.headless = headless
        self.stealth = stealth
        self.timeout = timeout
        self.model = model
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
    async def __aenter__(self):
        await self.start()
        return self
        
    async def __aexit__(self, *args):
        await self.close()
        
    async def start(self):
        """Start browser"""
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright not installed. Run: pip install playwright && npx playwright install chromium"
            )
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        
        context = await self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        
        # Apply stealth mode
        if self.stealth:
            await self._apply_stealth(context)
            
        self.page = await context.new_page()
        return self
    
    async def _apply_stealth(self, context):
        """Apply anti-detection measures"""
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)
        
    async def run(
        self,
        task: str,
        output_schema: Optional[type] = None,
        steps: Optional[List[str]] = None
    ) -> BrowserResult:
        """Run browser automation task."""
        try:
            if not self.page:
                await self.start()
                
            if steps:
                for step in steps:
                    if "http" in step:
                        await self.page.goto(step)
                    await asyncio.sleep(1)
                        
            elif "goto" in task.lower() or "go to" in task.lower() or "open" in task.lower():
                url = self._extract_url(task)
                if url:
                    await self.page.goto(url)
                    await asyncio.sleep(2)
                    
            elif "scrape" in task.lower() or "extract" in task.lower() or "get" in task.lower():
                content = await self.page.content()
                
                if output_schema:
                    extractor = SchemaExtractor(output_schema)
                    data = extractor.extract_from_html(content)
                    return BrowserResult(output=data, success=True)
                else:
                    text = await self.page.inner_text("body")
                    return BrowserResult(output=text, success=True)
                    
            else:
                content = await self.page.content()
                return BrowserResult(output=content[:5000], success=True)
                
            title = await self.page.title()
            return BrowserResult(
                output={"message": "Task completed", "title": title},
                success=True
            )
            
        except Exception as e:
            return BrowserResult(output=None, success=False, error=str(e))
    
    def _extract_url(self, text: str) -> Optional[str]:
        """Extract URL from text"""
        url_match = re.search(r'https?://[^\s]+', text)
        if url_match:
            return url_match.group()
        
        domain_match = re.search(r'(?:go to|open|navigate to)\s+([^\s]+)', text, re.I)
        if domain_match:
            domain = domain_match.group(1)
            if not domain.startswith('http'):
                return f"https://{domain}"
        return None
    
    async def take_screenshot(self, path: str = "screenshot.png"):
        """Take screenshot of current page"""
        if self.page:
            await self.page.screenshot(path=path)
            return path
        return None
    
    async def get_page_content(self) -> str:
        """Get current page content"""
        if self.page:
            return await self.page.content()
        return ""
    
    async def close(self):
        """Close browser"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


async def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python browser_agent.py <task>")
        return
        
    task = " ".join(sys.argv[1:])
    
    async with BrowserAgent(headless=False) as agent:
        result = await agent.run(task)
        
        if result.success:
            print(json.dumps(result.output, indent=2))
        else:
            print(f"Error: {result.error}")


if __name__ == "__main__":
    asyncio.run(main())
