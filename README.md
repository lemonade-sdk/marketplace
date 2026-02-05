# Lemonade Marketplace

This repository contains the app data for the [Lemonade](https://github.com/lemonade-sdk/lemonade) App Marketplace.

## Structure

```
marketplace/
├── apps.json              # Generated - DO NOT EDIT DIRECTLY
├── pinned.json            # Pinned apps list (CODEOWNERS only)
├── apps/
│   ├── open-webui/
│   │   ├── app.json       # App metadata
│   │   └── logo.png       # App logo (optional, 64x64 recommended)
│   ├── n8n/
│   │   ├── app.json
│   │   └── logo.png
│   └── ...
└── scripts/
    └── build.py           # Generates apps.json from app.json files
```

## Adding a New App

1. Create a new folder in `apps/` with your app's ID (lowercase, hyphenated)
2. Add an `app.json` file with the following structure:

```json
{
  "id": "your-app-id",
  "name": "Your App Name",
  "description": "A brief description of what your app does with Lemonade",
  "category": ["code"],
  "date_added": "2025-02-05",
  "links": {
    "app": "https://your-app-url.com",
    "guide": "https://lemonade-server.ai/docs/server/apps/your-app/",
    "video": "https://youtube.com/watch?v=..."
  }
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique app identifier (lowercase, hyphenated) |
| `name` | string | Display name of the app |
| `description` | string | Brief description of what the app does with Lemonade |
| `category` | string[] | Array of category IDs (see Categories below) |
| `date_added` | string | Date the app was added, in `YYYY-MM-DD` format |
| `links.app` | string | Primary URL to the app |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `links.guide` | string | URL to integration guide/documentation |
| `links.video` | string | URL to demo/tutorial video |

3. (Optional) Add a `logo.png` file (64x64 pixels recommended)
4. Submit a pull request

## Categories

| ID | Label |
|----|-------|
| `chat` | Chat |
| `code` | Code |
| `creative` | Creative |
| `automation` | Automation |
| `app` | Apps |

## Pinned Apps

Pinned apps appear first in the marketplace and are highlighted on the website. The list of pinned apps is managed in `pinned.json`.

> **Note:** Only repository CODEOWNERS may modify `pinned.json`. External contributors should not include changes to this file in their pull requests.

### pinned.json Format

```json
{
  "pinned": [
    "app-id-1",
    "app-id-2"
  ]
}
```

## App Ordering

Apps in the marketplace are ordered as follows:
1. **Pinned apps first** - Apps listed in `pinned.json` appear at the top
2. **By date added** - Newer apps appear before older apps
3. **Alphabetically** - Apps with the same date are sorted by name

## Building

The `apps.json` file is automatically generated when changes are pushed to `main`.

To build locally:

```bash
python scripts/build.py
```

## Usage

The generated `apps.json` is consumed by:
- [lemonade-server.ai/marketplace](https://lemonade-server.ai/marketplace) - Web marketplace
- Lemonade Desktop App - Embedded marketplace panel

### Fetching apps.json

```javascript
const response = await fetch(
  'https://raw.githubusercontent.com/lemonade-sdk/marketplace/main/apps.json'
);
const data = await response.json();
console.log(data.apps); // Array of app objects
```

### App Object Schema

Each app in `data.apps` includes:

```javascript
{
  "id": "open-webui",
  "name": "Open WebUI",
  "description": "Feature-rich web interface for chatting with LLMs locally",
  "category": ["chat"],
  "date_added": "2025-02-05",
  "links": {
    "app": "https://...",
    "guide": "https://...",
    "video": "https://..."
  },
  "logo": "https://raw.githubusercontent.com/.../logo.png",
  "pinned": true  // Derived field - true if app is in pinned.json
}
```

## License

Apache 2.0 - See [LICENSE](LICENSE)
