"""
controller.py
----------------
This file acts as the SINGLE orchestrator for backend logic.
Nothing in this file runs automatically on import.
Flask explicitly calls main().
"""

import traceback

def main():
    print("✅ Controller.main() started")

    # Run each module in isolation so one failure doesn't break everything
    run_hack_module()

    print("✅ Controller.main() finished")


def run_hack_module():
    try:
        print("▶ Importing hack module...")
        import hack   # lazy import (VERY IMPORTANT)

        # check function existence
        if hasattr(hack, "run"):
            print("▶ Calling hack.run()")
            hack.run()
            print("✅ hack.run() completed")
        else:
            print("⚠ hack.run() not found (function missing)")

    except Exception as e:
        print("❌ Error while running hack module")
        print(e)
        traceback.print_exc()

def run():
    print("🟢 hack.run() executed")