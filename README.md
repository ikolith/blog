# Static Site Generator

Based on makesite by Sunaina Pai with title extraction modification.

## Commands
- `uv run python scripts/makesite.py` - build site only
- `uv run python main.py` - build, serve, and watch for changes

## Content
- Add `.md` files to `content/blog/` 
- Use `YYYY-MM-DD-filename.md` for chronological order
- Tables are clickable (ready for dice rolling JS)
- Titles automatically extracted from first `# header` in markdown files

## Features
- Markdown to HTML
- Print-optimized CSS (A4 format)
- Auto-generated blog index and RSS feed
- Static file serving from `static/`