#!/usr/bin/env python3
"""
Browser Use CLI - Command line interface
"""

import asyncio
import sys
import argparse
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from browser_agent import BrowserAgent


async def main():
    parser = argparse.ArgumentParser(description="Browser Use CLI")
    parser.add_argument("task", help="Task description")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--session", "-s", help="Session name to use")
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument("--screenshot", help="Take screenshot")
    parser.add_argument("--stealth", action="store_true", default=True, help="Enable stealth mode")
    
    args = parser.parse_args()
    
    # Create session if specified
    session = None
    if args.session:
        from session import Session
        session = Session.load_from_storage(args.session)
    
    # Create agent
    agent = BrowserAgent(
        session=session,
        headless=args.headless,
        stealth=args.stealth
    )
    
    try:
        await agent.start()
        result = await agent.run(args.task)
        
        if result.success:
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result.output, f, indent=2)
                print(f"Output saved to {args.output}")
            else:
                print(json.dumps(result.output, indent=2, ensure_ascii=False))
                
            if args.screenshot:
                path = await agent.take_screenshot(args.screenshot)
                print(f"Screenshot saved to {path}")
        else:
            print(f"Error: {result.error}", file=sys.stderr)
            sys.exit(1)
            
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
