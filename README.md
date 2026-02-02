# Lemonade Marketplace

This repository contains the app data for the [Lemonade](https://github.com/lemonade-sdk/lemonade) App Marketplace.

## Structure

```
marketplace/
├── apps.json              # Generated - DO NOT EDIT DIRECTLY
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
  "links": {
    "app": "https://your-app-url.com",
    "guide": "https://lemonade-server.ai/docs/server/apps/your-app/",
    "video": "https://youtube.com/watch?v=..."
  }
}
```

> **Note:** Add `"rank": N` (1-10) to make an app "featured" on the README and website front page. Omit `rank` for non-featured apps.

3. (Optional) Add a `logo.png` file (64x64 pixels recommended)
4. Submit a pull request

## Categories

| ID | Label |
|----|-------|
| `chat` | Chat |
| `code` | Code |
| `creative` | Creative |
| `automation` | Automation |
| `end-user` | End-User Apps |

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
- README.md - Top 10 featured apps

### Fetching apps.json

```javascript
const response = await fetch(
  'https://raw.githubusercontent.com/lemonade-sdk/marketplace/main/apps.json'
);
const data = await response.json();
console.log(data.apps); // Array of app objects
```

## License

Apache 2.0 - See [LICENSE](LICENSE)
