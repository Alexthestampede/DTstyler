# DTstyler - Custom Prompt Style Manager

A simple interactive tool for managing custom prompt styles for AI image generation.

## Files

- `custom_prompt_style.json.sample` - The style database (100+ predefined styles)
- `style_manager.py` - Interactive CLI tool for managing styles

## Usage

Run the style manager:

```bash
python3 style_manager.py
# or
./style_manager.py
```

## Features

The interactive menu provides the following options:

1. **List all styles** - Browse all available styles with pagination
2. **Search styles** - Find styles by name (case-insensitive)
3. **View style details** - Find and view full details of a style (by search or number)
4. **Add new style** - Create a new style with guided prompts
5. **Edit style** - Find and modify an existing style (by search or number)
6. **Remove style** - Find and delete a style (by search or number)
7. **Reload from file** - Refresh from the JSON file

## Adding a Style

When adding a new style, you'll be prompted for:

- **Name** (required) - A unique identifier for the style
- **Prompt** (required) - The prompt template with `[prompt]` placeholder
- **Negative Prompt** (optional) - Elements to exclude from generation

### Multi-line Input Support

Both prompt and negative prompt fields support **multi-line input**. This means you can:
- Paste text with newlines directly from other sources
- Type multiple lines naturally
- Finish by pressing **Enter twice** or typing **END**

The tool automatically:
- Converts all newlines to spaces
- Removes extra whitespace
- Formats the text as a single clean line for the JSON file

Example session:
```
Name: my-custom-style
Prompt template:
(Paste your text - can be multiple lines. Press Enter twice or type END to finish)
> artistic rendering of [prompt]
  highly detailed, vibrant colors
  professional quality
[press Enter to finish]

Result: "artistic rendering of [prompt] highly detailed, vibrant colors professional quality"
```

## Editing a Style

When you select "Edit style", you'll be prompted to find the style first:
- **Search by name** - Type part of the style name to find it (if multiple matches, you can choose)
- **Enter style number** - If you know the exact number from a list

Then you can edit the fields (press Enter twice to keep current value for multi-line fields).

## Style Format

Each style follows this JSON structure:

```json
{
  "name": "style-identifier",
  "prompt": "description [prompt] . modifiers",
  "negative_prompt": "unwanted elements"
}
```

The `[prompt]` placeholder is replaced with user input during image generation.

## Adding Thumbnails

When you create a style, the tool automatically generates a thumbnail path like:
```
./Pictures/thumbs/mystylename.png
```

To add a thumbnail image for your custom style:
1. Create the directory `Pictures/thumbs/` in your app folder (if it doesn't exist)
2. Save your thumbnail image with the suggested filename
3. The app will display it - but **works fine without it!** (no crashes if missing)

**Supported formats**: PNG, JPG, or any image format your app supports

**Example**:
- Style name: "Damn Hip"
- Auto-generated path: `./Pictures/thumbs/damnhip.png`
- Place your image at that path to see it in the app

You can also override the auto-generated path when creating/editing a style.

## Tips

- Use descriptive, lowercase names with hyphens (e.g., `cyberpunk-neon`)
- Always include the `[prompt]` placeholder in your prompt template
- Common negative prompt elements: "ugly, deformed, noisy, blurry, low contrast"
- Styles are saved automatically after add/edit/remove operations
- Thumbnails are completely optional - the app won't crash if they're missing
- The included json is the stock one, and once edited it goes in the Models folder inside the Draw Things one. Requires Draw Things to be restarted to see the changes.
