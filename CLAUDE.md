# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

DTstyler is a configuration repository for custom prompt styles used in AI image generation workflows. It contains style presets that enhance prompts with specific artistic styles, photography techniques, and aesthetic modifiers.

## File Structure

- `custom_prompt_style.json.sample` - A JSON configuration file containing 180+ predefined prompt styles
  - Each style includes a `name`, `prompt` template, `negative_prompt`, and `image_path`
  - The `image_path` field is used for custom style thumbnails (only needed for user-created styles, not the hardcoded defaults)
  - Styles are organized by categories: cinematic, artistic styles (SAI), advertising, art movements, games, photo techniques, papercraft, and miscellaneous
  - The `[prompt]` placeholder is replaced with user input when applied
- `style_manager.py` - Interactive CLI tool for managing styles (add, edit, remove, search)
- `README.md` - User documentation for the style manager tool

## Style Categories

The configuration includes the following major categories:
- **Cinematic & Photography**: cinematic, analog film, HDR, long exposure, tilt-shift, film noir, neon noir
- **SAI Styles**: 3D model, anime, comic book, digital art, fantasy art, photographic, pixel art, etc.
- **Advertising**: automotive, corporate, fashion editorial, food photography, luxury, real estate
- **Art Movements**: Abstract Expressionism, Art Deco, Art Nouveau, Baroque, Cubism, Impressionism, Pop Art, Surrealism, etc.
- **Game Styles**: Bubble Bobble, Minecraft, Pokémon, retro arcade, RPG fantasy, Street Fighter, Zelda
- **Papercraft**: collage, kirigami, paper mache, papercut shadow box, origami
- **Miscellaneous**: architectural, dystopian, gothic, horror, kawaii, minimalist, steampunk, tribal

## Usage Pattern

Each style entry follows this structure:
```json
{
  "name": "style-identifier",
  "prompt": "style description [prompt] . additional modifiers",
  "negative_prompt": "unwanted elements to avoid",
  "image_path": "./Pictures/thumbs/styleidentifier.png"
}
```

The `image_path` field:
- Auto-generated based on style name (e.g., "Damn Hip" → `./Pictures/thumbs/damnhip.png`)
- Points to an optional thumbnail image
- Can be empty or point to a non-existent file without causing crashes
- Only relevant for custom user-created styles (default styles are hardcoded in the app)

When working with this file:
- Preserve the exact JSON structure with name, prompt, negative_prompt, and image_path fields
- Keep the `[prompt]` placeholder in all prompt templates
- Maintain consistency in naming conventions (lowercase with hyphens or spaces)
- Negative prompts typically exclude: "ugly, deformed, noisy, blurry, low contrast" plus style-specific exclusions
- Image paths are auto-generated from style names and point to `./Pictures/thumbs/{sanitized-name}.png`

## Development Tools

### Style Manager (`style_manager.py`)

Interactive Python CLI for managing the style database. Run with:
```bash
python3 style_manager.py
```

Features:
- **List/Search**: Browse and search through all styles
- **View/Edit/Remove**: Smart finder lets you locate styles by name search or number (no need to memorize positions in a 200+ item list)
- **Add**: Create new styles with guided prompts (name required, prompt required, negative_prompt optional)
- **Edit**: Modify existing styles (press Enter twice to keep current values for multi-line fields)
- **Remove**: Delete styles with confirmation
- **Auto-save**: Changes are saved immediately to the JSON file with proper formatting

When adding or editing styles:
- Always include the `[prompt]` placeholder in prompt templates
- The script warns if the placeholder is missing
- Negative prompts are optional (can be left empty)
- Duplicate names are allowed but trigger a warning
- **Multi-line input supported**: Paste text with newlines - the tool automatically converts them to spaces and cleans up whitespace. Finish input by pressing Enter twice or typing END.

**Important**: The tool preserves the specific JSON formatting required by the consuming application (spaces around colons: `" : "` instead of standard `": "`). This is critical for compatibility.
