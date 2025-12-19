#!/usr/bin/env python3
"""
DTstyler - Interactive Style Manager
Manage custom prompt styles for AI image generation
"""

import json
import os
import sys
from typing import List, Dict, Optional


class StyleManager:
    def __init__(self, filename: str = "custom_prompt_style.json"):
        self.filename = filename
        self.styles: List[Dict[str, str]] = []
        self.load_styles()

    def load_styles(self):
        """Load styles from JSON file"""
        if not os.path.exists(self.filename):
            print(f"Error: {self.filename} not found!")
            sys.exit(1)

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.styles = json.load(f)
            print(f"✓ Loaded {len(self.styles)} styles from {self.filename}\n")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            sys.exit(1)

    def save_styles(self):
        """Save styles back to JSON file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                # Use ensure_ascii=True to avoid encoding issues with Unicode characters
                # This escapes non-ASCII chars as \uXXXX sequences for maximum compatibility
                json_str = json.dumps(self.styles, indent=2, ensure_ascii=True)
                # CRITICAL: The consuming app expects " : " (space before and after colon)
                # Standard json.dump produces ": " (no space before colon)
                # We must match the original file format for compatibility
                json_str = json_str.replace('": ', '" : ')
                f.write(json_str)
            print(f"✓ Saved {len(self.styles)} styles to {self.filename}\n")
        except Exception as e:
            print(f"Error saving file: {e}")

    def generate_image_path(self, style_name: str) -> str:
        """
        Generate a default image path for a style based on its name.
        Converts style name to lowercase, removes special chars, and creates a path.
        Example: "Damn Hip" -> "./Pictures/thumbs/damnhip.png"
        """
        # Convert to lowercase and remove special characters
        sanitized = ''.join(c for c in style_name.lower() if c.isalnum() or c in ' -_')
        # Replace spaces with nothing, keep hyphens and underscores
        sanitized = sanitized.replace(' ', '')
        # Remove multiple consecutive hyphens/underscores
        while '--' in sanitized or '__' in sanitized:
            sanitized = sanitized.replace('--', '-').replace('__', '_')
        # Create the path
        return f"./Pictures/thumbs/{sanitized}.png"

    def get_multiline_input(self, prompt_text: str, allow_empty: bool = False) -> str:
        """
        Get multi-line input from user.
        User can paste multiple lines, and input ends with an empty line or 'END'.
        Newlines are converted to spaces and extra whitespace is cleaned up.
        """
        if prompt_text:
            print(prompt_text)
        print("(Paste your text - can be multiple lines. Press Enter twice or type END to finish)")
        print("> ", end="", flush=True)

        lines = []
        empty_count = 0
        first_line = True

        while True:
            try:
                if first_line:
                    line = input()
                    first_line = False
                else:
                    line = input()

                # Check for END marker
                if line.strip().upper() == 'END':
                    break

                # Track empty lines
                if not line.strip():
                    empty_count += 1
                    # Single empty line ends input (like pressing Enter twice total)
                    if empty_count >= 1:
                        break
                else:
                    empty_count = 0
                    lines.append(line)

            except EOFError:
                break

        # Join lines with spaces and clean up whitespace
        result = ' '.join(lines).strip()
        # Collapse multiple spaces into one
        result = ' '.join(result.split())

        return result

    def list_styles(self, page_size: int = 20):
        """Display all styles with pagination"""
        if not self.styles:
            print("No styles found.\n")
            return

        print(f"\n{'='*80}")
        print(f"Total Styles: {len(self.styles)}")
        print(f"{'='*80}\n")

        for i, style in enumerate(self.styles, 1):
            print(f"{i:3d}. {style.get('name', 'Unnamed')}")
            if i % page_size == 0 and i < len(self.styles):
                input("\nPress Enter to see more...")
        print()

    def search_styles(self, query: str):
        """Search for styles by name"""
        query_lower = query.lower()
        matches = [
            (i, style) for i, style in enumerate(self.styles)
            if query_lower in style.get('name', '').lower()
        ]

        if not matches:
            print(f"No styles found matching '{query}'\n")
            return

        print(f"\nFound {len(matches)} match(es):\n")
        for idx, style in matches:
            print(f"{idx + 1:3d}. {style.get('name', 'Unnamed')}")
        print()

    def view_style(self, index: int):
        """View details of a specific style"""
        if 0 <= index < len(self.styles):
            style = self.styles[index]
            print(f"\n{'='*80}")
            print(f"Style #{index + 1}")
            print(f"{'='*80}")
            print(f"Name: {style.get('name', 'N/A')}")
            print(f"\nPrompt:\n{style.get('prompt', 'N/A')}")
            print(f"\nNegative Prompt:\n{style.get('negative_prompt', '(empty)')}")
            print(f"\nImage Path:\n{style.get('image_path', '(none)')}")
            print(f"{'='*80}\n")
        else:
            print("Invalid style number.\n")

    def add_style(self):
        """Interactively add a new style"""
        print("\n" + "="*80)
        print("ADD NEW STYLE")
        print("="*80 + "\n")

        # Get name (required)
        while True:
            name = input("Style name (required): ").strip()
            if name:
                # Check for duplicates
                if any(s.get('name') == name for s in self.styles):
                    print(f"⚠ Warning: A style named '{name}' already exists.")
                    confirm = input("Continue anyway? (y/n): ").strip().lower()
                    if confirm != 'y':
                        continue
                break
            else:
                print("Name cannot be empty. Please try again.")

        # Get prompt (required)
        while True:
            prompt = self.get_multiline_input("\nPrompt template (use [prompt] as placeholder):")
            if prompt:
                if '[prompt]' not in prompt:
                    print("⚠ Warning: Your prompt doesn't contain [prompt] placeholder.")
                    confirm = input("Continue anyway? (y/n): ").strip().lower()
                    if confirm != 'y':
                        continue
                break
            else:
                print("Prompt cannot be empty. Please try again.")

        # Get negative prompt (optional)
        negative_prompt = self.get_multiline_input("\nNegative prompt (optional):", allow_empty=True)

        # Auto-generate image path based on style name
        auto_image_path = self.generate_image_path(name)
        print(f"\nAuto-generated thumbnail path: {auto_image_path}")
        print("Press Enter to use this, or type a custom path:")
        custom_image_path = input("> ").strip()
        image_path = custom_image_path if custom_image_path else auto_image_path

        # Create new style
        new_style = {
            "name": name,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "image_path": image_path
        }

        # Confirm before adding
        print("\n" + "-"*80)
        print("Preview:")
        print(f"Name: {new_style['name']}")
        print(f"Prompt: {new_style['prompt']}")
        print(f"Negative: {new_style['negative_prompt'] or '(empty)'}")
        print(f"Image: {new_style['image_path'] or '(none)'}")
        print("-"*80)

        confirm = input("\nAdd this style? (y/n): ").strip().lower()
        if confirm == 'y':
            self.styles.append(new_style)
            print(f"✓ Style '{name}' added successfully!\n")
            self.save_styles()

            # Show thumbnail instructions
            if image_path:
                print("📷 Thumbnail Tip:")
                print(f"   To add a thumbnail, place an image at: {image_path}")
                print(f"   (The app works fine without it - thumbnails are optional)\n")
        else:
            print("Cancelled.\n")

    def edit_style(self, index: int):
        """Edit an existing style"""
        if not (0 <= index < len(self.styles)):
            print("Invalid style number.\n")
            return

        style = self.styles[index]
        print("\n" + "="*80)
        print(f"EDIT STYLE #{index + 1}")
        print("="*80 + "\n")
        print("Current values (press Enter to keep current value):\n")

        # Edit name
        current_name = style.get('name', '')
        print(f"Current name: {current_name}")
        new_name = input("New name: ").strip()
        if new_name:
            style['name'] = new_name

        # Edit prompt
        current_prompt = style.get('prompt', '')
        print(f"\nCurrent prompt:\n{current_prompt}")
        print("\nEnter new prompt (or press Enter twice to keep current):")
        new_prompt = self.get_multiline_input("", allow_empty=True)
        if new_prompt:
            if '[prompt]' not in new_prompt:
                print("⚠ Warning: Your prompt doesn't contain [prompt] placeholder.")
            style['prompt'] = new_prompt

        # Edit negative prompt
        current_negative = style.get('negative_prompt', '')
        print(f"\nCurrent negative prompt:\n{current_negative or '(empty)'}")
        print("\nEnter new negative prompt (or press Enter twice to keep current):")
        new_negative = self.get_multiline_input("", allow_empty=True)
        # Update only if user entered something (even if empty)
        if new_negative != current_negative:
            # Ask for confirmation if changing to empty
            if not new_negative and current_negative:
                confirm = input("Clear the negative prompt? (y/n): ").strip().lower()
                if confirm == 'y':
                    style['negative_prompt'] = ""
            else:
                style['negative_prompt'] = new_negative

        # Edit image path
        current_image = style.get('image_path', '')
        auto_image_path = self.generate_image_path(style.get('name', ''))
        print(f"\nCurrent image path: {current_image or '(none)'}")
        print(f"Auto-generated suggestion: {auto_image_path}")
        print("Enter new path, 'auto' for suggestion, or press Enter to keep current:")
        new_image = input("> ").strip()
        if new_image:
            if new_image.lower() == 'auto':
                style['image_path'] = auto_image_path
            else:
                style['image_path'] = new_image
        elif 'image_path' not in style:
            # Ensure the field exists even if empty
            style['image_path'] = ""

        print(f"\n✓ Style updated successfully!\n")
        self.save_styles()

    def find_style_interactive(self) -> Optional[int]:
        """
        Interactively find a style by search or number.
        Returns the index of the selected style, or None if cancelled.
        """
        print("\nFind style by:")
        print("  1. Search by name")
        print("  2. Enter style number")
        print("  0. Cancel")

        choice = input("\nSelect option: ").strip()

        if choice == '0':
            return None
        elif choice == '1':
            query = input("Search query: ").strip()
            if not query:
                return None

            query_lower = query.lower()
            matches = [
                (i, style) for i, style in enumerate(self.styles)
                if query_lower in style.get('name', '').lower()
            ]

            if not matches:
                print(f"No styles found matching '{query}'\n")
                return None

            if len(matches) == 1:
                idx, style = matches[0]
                print(f"\nFound: {style.get('name', 'Unnamed')}")
                return idx

            # Multiple matches - let user choose
            print(f"\nFound {len(matches)} matches:")
            for i, (idx, style) in enumerate(matches, 1):
                print(f"  {i}. {style.get('name', 'Unnamed')} (#{idx + 1})")

            try:
                selection = int(input("\nSelect number (1-{}): ".format(len(matches))).strip())
                if 1 <= selection <= len(matches):
                    return matches[selection - 1][0]
                else:
                    print("Invalid selection.\n")
                    return None
            except ValueError:
                print("Invalid input.\n")
                return None

        elif choice == '2':
            try:
                num = int(input("Style number: ").strip())
                if 1 <= num <= len(self.styles):
                    return num - 1
                else:
                    print(f"Please enter a number between 1 and {len(self.styles)}\n")
                    return None
            except ValueError:
                print("Invalid number.\n")
                return None
        else:
            print("Invalid option.\n")
            return None

    def remove_style(self, index: int):
        """Remove a style"""
        if not (0 <= index < len(self.styles)):
            print("Invalid style number.\n")
            return

        style = self.styles[index]
        print(f"\nAre you sure you want to remove '{style.get('name', 'Unnamed')}'?")
        confirm = input("Type 'yes' to confirm: ").strip().lower()

        if confirm == 'yes':
            removed = self.styles.pop(index)
            print(f"✓ Removed '{removed.get('name', 'Unnamed')}'\n")
            self.save_styles()
        else:
            print("Cancelled.\n")

    def run(self):
        """Main interactive loop"""
        while True:
            print("="*80)
            print("DTSTYLER - STYLE MANAGER")
            print("="*80)
            print("\nOptions:")
            print("  1. List all styles")
            print("  2. Search styles")
            print("  3. View style details")
            print("  4. Add new style")
            print("  5. Edit style")
            print("  6. Remove style")
            print("  7. Reload from file")
            print("  0. Exit")
            print()

            choice = input("Select option: ").strip()

            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1':
                self.list_styles()
            elif choice == '2':
                query = input("Search query: ").strip()
                if query:
                    self.search_styles(query)
            elif choice == '3':
                index = self.find_style_interactive()
                if index is not None:
                    self.view_style(index)
            elif choice == '4':
                self.add_style()
            elif choice == '5':
                index = self.find_style_interactive()
                if index is not None:
                    self.edit_style(index)
            elif choice == '6':
                index = self.find_style_interactive()
                if index is not None:
                    self.remove_style(index)
            elif choice == '7':
                self.load_styles()
            else:
                print("Invalid option.\n")


def main():
    """Entry point"""
    manager = StyleManager()
    try:
        manager.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
