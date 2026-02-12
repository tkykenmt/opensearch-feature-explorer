# Images Reference

Source: https://kiro.dev/docs/cli/chat/images/

Kiro can analyze images directly in chat sessions.

## Methods

- **Drag and drop**: Drag image into terminal, path auto-inserted into prompt
- **Mention path**: `Can you analyze this screenshot at /path/to/screenshot.png?` — Kiro auto-uses fs_read Image mode
- **Clipboard paste**: `/paste`

## Supported Formats

JPEG/JPG, PNG, GIF, WebP. Max 10MB per image, up to 10 images per request.

## Use Cases

- Analyzing error message screenshots
- Converting architecture diagrams to code
- Discussing UI/UX designs → HTML/CSS
- Translating flowcharts to algorithms
- Reviewing code snippets shared as images
- Interpreting technical diagrams

## Tips

- Use high-resolution images with clear text
- Provide specific instructions about what to do with the image
- For complex diagrams, add additional context
