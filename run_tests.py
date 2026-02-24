"""
Run all tests from project root
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from tests.test_agents import test_agents

if __name__ == "__main__":
    asyncio.run(test_agents())
