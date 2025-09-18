#!/usr/bin/env python3
"""
Standalone file watcher that runs pytest automatically when Python files change.
This can be used independently of the Discord bot for development.
"""

import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class AutoTestRunner(FileSystemEventHandler):
    def __init__(self):
        self.last_test_time = 0

    def run_tests(self):
        """Run pytest and return True if tests pass."""
        try:
            print("\n" + "="*50)
            print("🧪 Running tests...")
            print("="*50)

            result = subprocess.run(
                ['python', '-m', 'pytest', '--tb=short', '-v'],
                capture_output=True,
                text=True,
                timeout=60
            )

            print(result.stdout)
            if result.stderr:
                print(result.stderr)

            if result.returncode == 0:
                print("✅ All tests passed!")
                return True
            else:
                print("❌ Some tests failed!")
                return False

        except subprocess.TimeoutExpired:
            print("⏰ Tests timed out after 60 seconds")
            return False
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return False

    def on_modified(self, event):
        if event.is_directory:
            return

        # Only run tests when Python files are modified
        if event.src_path.endswith('.py'):
            print(f"\n📝 File modified: {event.src_path}")

            # Debounce: avoid running tests too frequently
            current_time = time.time()
            if current_time - self.last_test_time < 3:  # Wait 3 seconds between test runs
                return
            self.last_test_time = current_time

            # Run tests
            self.run_tests()


def main():
    """Start the file watcher for automatic testing."""
    print("🔍 Starting automatic test runner...")
    print("Watching for changes in Python files...")
    print("Press Ctrl+C to stop")

    event_handler = AutoTestRunner()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        # Run tests once at startup
        print("\n🚀 Running initial test suite...")
        event_handler.run_tests()

        # Keep watching for changes
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Stopping test watcher...")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()