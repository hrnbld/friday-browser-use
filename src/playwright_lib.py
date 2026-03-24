"""
Playwright wrapper with stealth features
"""

import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

try:
    from playwright.async_api import async_playwright, Page, Browser, Context, Playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@dataclass
class BrowserConfig:
    """Browser configuration"""
    headless: bool = False
    stealth: bool = True
    viewport: Dict[str, int] = None
    user_agent: Optional[str] = None
    proxy: Optional[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.viewport is None:
            self.viewport = {"width": 1920, "height": 1080}


class PlaywrightBrowser:
    """
    Enhanced Playwright browser with stealth mode.
    
    Usage:
        browser = PlaywrightBrowser()
        await browser.start()
        page = await browser.new_page()
        await page.goto("https://example.com")
    """
    
    def __init__(self, config: Optional[BrowserConfig] = None):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright not installed. Run: pip install playwright")
            
        self.config = config or BrowserConfig()
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        
    async def start(self):
        """Start browser"""
        self.playwright = await async_playwright().start()
        
        # Launch with proxy if configured
        if self.config.proxy:
            self.browser = await self.playwright.chromium.launch(
                headless=self.config.headless,
                proxy=self.config.proxy
            )
        else:
            self.browser = await self.playwright.chromium.launch(
                headless=self.config.headless
            )
            
        return self
    
    async def new_context(self) -> Context:
        """Create new browser context"""
        context = await self.browser.new_context(
            viewport=self.config.viewport,
            user_agent=self.config.user_agent
        )
        
        # Apply stealth mode
        if self.config.stealth:
            await self._apply_stealth(context)
            
        return context
    
    async def new_page(self, context: Optional[Context] = None) -> Page:
        """Create new page"""
        if context is None:
            context = await self.new_context()
        return await context.new_page()
    
    async def _apply_stealth(self, context: Context):
        """Apply anti-detection stealth mode"""
        await context.add_init_script("""
            // Remove webdriver flag
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            
            // Remove automation indicators
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """)
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


class StealthBrowser(PlaywrightBrowser):
    """Browser with maximum stealth settings"""
    
    def __init__(self):
        super().__init__(config=BrowserConfig(
            headless=False,
            stealth=True,
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ))


# Convenience functions
async def quick_browse(url: str, headless: bool = False) -> str:
    """Quick browse and return page content"""
    browser = PlaywrightBrowser(BrowserConfig(headless=headless))
    await browser.start()
    
    page = await browser.new_page()
    await page.goto(url)
    content = await page.content()
    
    await browser.close()
    return content


async def quick_screenshot(url: str, path: str = "screenshot.png"):
    """Quick take screenshot"""
    browser = PlaywrightBrowser(BrowserConfig(headless=False))
    await browser.start()
    
    page = await browser.new_page()
    await page.goto(url)
    await page.screenshot(path=path)
    
    await browser.close()
    return path
