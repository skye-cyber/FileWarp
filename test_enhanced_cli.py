#!/usr/bin/env python3
"""
Test script for the enhanced FileMAC CLI
"""

from filewarp.cli.app import enhanced_argsdev, RichConsoleUtils, EnhancedHelpSystem, ClipboardManager
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_basic_functionality():
    """Test basic functionality of the enhanced CLI"""
    print("Testing Enhanced FileMAC CLI...")

    # Test Rich console utilities
    print("\n1. Testing Rich Console Utilities:")
    RichConsoleUtils.print_info("This is an info message")
    RichConsoleUtils.print_success("This is a success message")
    RichConsoleUtils.print_warning("This is a warning message")
    RichConsoleUtils.print_error("This is an error message")
    RichConsoleUtils.print_header("Test Header", "Subtitle")

    # Test clipboard manager
    print("\n2. Testing Clipboard Manager:")
    print(f"Clipboard available: {ClipboardManager.is_available()}")

    if ClipboardManager.is_available():
        # Test copy to clipboard
        test_text = "FileMAC Enhanced CLI Test"
        if ClipboardManager.copy_to_clipboard(test_text):
            # Test paste from clipboard
            pasted = ClipboardManager.paste_from_clipboard()
            if pasted == test_text:
                RichConsoleUtils.print_success("Clipboard test passed!")
            else:
                RichConsoleUtils.print_warning("Clipboard paste test failed")

    # Test help system
    print("\n3. Testing Help System:")
    print("Showing quick start guide...")
    EnhancedHelpSystem.show_quick_start()

    print("\n4. Testing Enhanced CLI Entry Point:")
    print("This would normally call enhanced_argsdev(), but we'll skip it for testing")

    RichConsoleUtils.print_success("All basic tests completed!")


if __name__ == "__main__":
    test_basic_functionality()
