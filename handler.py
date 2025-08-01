#!/usr/bin/env python3
"""
🚀 RunPod Handler Entry Point
Compatibility alias for handler_fast.py
"""

# Import the main handler from handler_fast.py
from handler_fast import handler

# Re-export for RunPod compatibility
__all__ = ['handler']

if __name__ == "__main__":
    # Forward to main handler
    import handler_fast