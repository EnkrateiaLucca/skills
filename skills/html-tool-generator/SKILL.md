---
name: html-tool-generator
description: Generate single-file HTML tools following Simon Willison's patterns. Creates client-side utilities with localStorage API key management, no build steps, and CDN dependencies.
---

# Single-File HTML Tool Generator

Generate self-contained HTML tools that work entirely in the browser. Based on [Simon Willison's patterns](https://simonwillison.net/2025/Dec/10/html-tools/) for building useful utilities without servers, build steps, or frameworks.

## When to Use This Skill

Use this skill when the user requests:
- Building a single-file HTML utility or tool
- Creating a browser-based tool that uses an API
- Making a client-side data processor or converter
- Building a tool that should work offline or without a server
- Creating utilities for LLM API testing/interaction

Trigger phrases: "create an HTML tool", "build a single-file tool", "make a browser utility", "create a client-side tool", "build an API playground"

## Core Principles

### 1. Single File, No Build Steps
- Everything in one HTML file: HTML, CSS, and JavaScript
- **Never use React, Vue, or anything requiring compilation**
- No JSX, no TypeScript, no bundlers
- Vanilla JavaScript only

### 2. CDN Dependencies Only
- Load libraries from cdnjs, jsDelivr, or unpkg
- Always use versioned URLs for stability
- Common libraries:
  - `marked` for Markdown rendering
  - `highlight.js` for syntax highlighting
  - `pdf.js` for PDF handling
  - `Tesseract.js` for OCR
  - `Pyodide` for Python execution

### 3. API Keys in localStorage (NEVER in HTML)
- Prompt user for API keys on first use
- Store in localStorage immediately
- Never send keys to any server
- Provide a way to clear/reset stored keys

### 4. State Management
- URL hash/params for shareable state (configs, settings)
- localStorage for user data (drafts, preferences)
- No server-side storage needed

## Template Structure

Every HTML tool follows this anatomy:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tool Name</title>
    <style>
        /* All CSS inline - no external stylesheets */
    </style>
</head>
<body>
    <!-- Tool UI -->

    <script>
        /* All JavaScript inline - no external scripts except CDN libs */
    </script>
</body>
</html>
```

## CSS Patterns

### Base Styling
```css
* {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    line-height: 1.6;
    background: #f5f5f5;
}

/* Prevent mobile zoom on input focus */
input, textarea, select {
    font-size: 16px;
}
```

### Common UI Components
```css
/* Card container */
.card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Primary button */
button {
    background: #2563eb;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
}

button:hover {
    background: #1d4ed8;
}

button:disabled {
    background: #9ca3af;
    cursor: not-allowed;
}

/* Text inputs */
textarea, input[type="text"], input[type="url"] {
    width: 100%;
    padding: 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-family: inherit;
    resize: vertical;
}

textarea:focus, input:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Error display */
.error {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 12px;
    border-radius: 6px;
    margin: 12px 0;
}

/* Success display */
.success {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #16a34a;
    padding: 12px;
    border-radius: 6px;
    margin: 12px 0;
}

/* Loading state */
.loading {
    opacity: 0.7;
    pointer-events: none;
}

/* Code/output display */
pre {
    background: #1e293b;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 6px;
    overflow-x: auto;
    font-family: 'SF Mono', Monaco, 'Consolas', monospace;
    font-size: 14px;
}
```

### File Upload Styling
```css
/* Drag and drop zone */
.drop-zone {
    border: 2px dashed #d1d5db;
    border-radius: 8px;
    padding: 40px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}

.drop-zone:hover, .drop-zone.dragover {
    border-color: #2563eb;
    background: #eff6ff;
}

.drop-zone input[type="file"] {
    display: none;
}

/* File list */
.file-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
}

.file-item {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #f3f4f6;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 14px;
}

.file-item button {
    background: none;
    color: #6b7280;
    padding: 2px 6px;
    font-size: 12px;
}

.file-item button:hover {
    color: #dc2626;
    background: none;
}
```

## JavaScript Patterns

### API Key Management (CRITICAL)
```javascript
// Get or prompt for API key
function getApiKey(keyName, providerName) {
    let key = localStorage.getItem(keyName);
    if (!key) {
        key = prompt(`Please enter your ${providerName} API key:`);
        if (key) {
            localStorage.setItem(keyName, key.trim());
        }
    }
    return key;
}

// Clear stored API key
function clearApiKey(keyName) {
    localStorage.removeItem(keyName);
}

// Example usage:
// const apiKey = getApiKey('ANTHROPIC_API_KEY', 'Anthropic');
// const apiKey = getApiKey('OPENAI_API_KEY', 'OpenAI');
// const apiKey = getApiKey('GEMINI_API_KEY', 'Google Gemini');
```

### Settings Management Link
```javascript
// Add settings link to manage API keys
function addSettingsUI(keyName, providerName) {
    const settingsHtml = `
        <div class="settings">
            <small>
                <a href="#" onclick="clearApiKey('${keyName}'); location.reload(); return false;">
                    Reset ${providerName} API key
                </a>
            </small>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', settingsHtml);
}
```

### File Handling
```javascript
// Setup drag and drop
function setupDropZone(dropZone, onFilesSelected) {
    const fileInput = dropZone.querySelector('input[type="file"]');

    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        onFilesSelected(Array.from(e.dataTransfer.files));
    });

    fileInput.addEventListener('change', (e) => {
        onFilesSelected(Array.from(e.target.files));
    });
}

// Read file as base64
async function readFileAsBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            const base64 = reader.result.split(',')[1];
            resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Read file as text
async function readFileAsText(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsText(file);
    });
}
```

### Clipboard Operations
```javascript
// Copy to clipboard with feedback
async function copyToClipboard(text, button) {
    try {
        await navigator.clipboard.writeText(text);
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(() => button.textContent = originalText, 2000);
    } catch (err) {
        console.error('Copy failed:', err);
    }
}

// Paste from clipboard
async function pasteFromClipboard() {
    try {
        return await navigator.clipboard.readText();
    } catch (err) {
        console.error('Paste failed:', err);
        return null;
    }
}
```

### Download Generated Files
```javascript
// Download text as file
function downloadAsFile(content, filename, mimeType = 'text/plain') {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Download JSON
function downloadJSON(data, filename) {
    downloadAsFile(JSON.stringify(data, null, 2), filename, 'application/json');
}
```

### URL State Persistence
```javascript
// Save state to URL
function saveStateToUrl(state) {
    const params = new URLSearchParams(state);
    history.replaceState(null, '', '?' + params.toString());
}

// Load state from URL
function loadStateFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return Object.fromEntries(params.entries());
}

// Hash-based state (for larger data)
function saveToHash(data) {
    location.hash = encodeURIComponent(JSON.stringify(data));
}

function loadFromHash() {
    if (!location.hash) return null;
    try {
        return JSON.parse(decodeURIComponent(location.hash.slice(1)));
    } catch {
        return null;
    }
}
```

### API Calls Pattern
```javascript
// Generic API call with error handling
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.error?.message || `HTTP ${response.status}`);
        }
        return await response.json();
    } catch (err) {
        throw err;
    }
}

// Show loading state
function setLoading(button, isLoading) {
    button.disabled = isLoading;
    button.textContent = isLoading ? 'Processing...' : button.dataset.originalText;
}
```

### Streaming Responses (for LLM APIs)
```javascript
// Handle streaming response
async function handleStreamingResponse(response, onChunk) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Keep incomplete line in buffer

        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = line.slice(6);
                if (data === '[DONE]') return;
                try {
                    onChunk(JSON.parse(data));
                } catch {}
            }
        }
    }
}
```

## Common LLM API Integrations

### Anthropic Claude API
```javascript
async function callClaude(apiKey, messages, model = 'claude-sonnet-4-20250514') {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': apiKey,
            'anthropic-version': '2023-06-01',
            'anthropic-dangerous-direct-browser-access': 'true'
        },
        body: JSON.stringify({
            model,
            max_tokens: 4096,
            messages
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error?.message || 'API call failed');
    }

    return response.json();
}
```

### OpenAI API
```javascript
async function callOpenAI(apiKey, messages, model = 'gpt-4o') {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            model,
            messages
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error?.message || 'API call failed');
    }

    return response.json();
}
```

### Google Gemini API
```javascript
async function callGemini(apiKey, contents, model = 'gemini-2.0-flash-exp') {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ contents })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error?.message || 'API call failed');
    }

    return response.json();
}
```

## Tool Categories & Examples

### 1. Data Converters
- JSON ↔ YAML converter
- CSV viewer/editor
- Markdown preview
- Base64 encoder/decoder
- URL encoder/decoder

### 2. API Playgrounds
- LLM chat interfaces (Claude, GPT, Gemini)
- Token counters
- Image generators
- Text-to-speech tools

### 3. File Processors
- Image resizer/cropper
- PDF text extractor
- OCR tool (with Tesseract.js)
- Audio transcription

### 4. Development Utilities
- JSON formatter/validator
- Regex tester
- Color picker/converter
- Hash generator (MD5, SHA)

### 5. Productivity Tools
- QR code generator
- Timestamp converter
- Text diff viewer
- Clipboard manager

## Workflow

### 1. Understand the Tool Requirements
- What is the main function?
- Does it need an API? Which one?
- What inputs/outputs are needed?
- Should state be shareable (URL) or private (localStorage)?

### 2. Choose the Right Patterns
- API key management if calling external services
- File upload if processing user files
- Clipboard operations for copy/paste workflows
- URL state for shareable configurations

### 3. Build the HTML Structure
- Clean, semantic HTML
- Accessible form controls
- Clear visual hierarchy

### 4. Add Styling
- Mobile-friendly (16px fonts, touch targets)
- Dark mode support (optional)
- Clear loading/error states

### 5. Implement JavaScript
- API key handling FIRST
- Core functionality
- Error handling
- Loading states

### 6. Test & Deliver
- Test in browser
- Verify API keys stay in localStorage
- Check mobile responsiveness
- Save to user's preferred location

## Security Checklist

Before delivering any HTML tool:

- [ ] API keys stored in localStorage, NEVER in HTML source
- [ ] No hardcoded secrets or credentials
- [ ] API calls use HTTPS
- [ ] User data stays client-side
- [ ] No eval() or innerHTML with user input (use textContent)
- [ ] File inputs sanitized before processing

## File Naming Convention

Save tools with descriptive, hyphenated names:
- `claude-chat-tool.html`
- `json-yaml-converter.html`
- `image-resizer.html`
- `token-counter.html`

Default save location: User's current working directory or specified path.

## Example Complete Tool

See `template-basic.html` in this skill directory for a complete working example demonstrating all patterns.

## Tips for Success

**Keep it simple:**
- One file, one purpose
- No over-engineering
- If it needs a build step, you're doing it wrong

**User experience:**
- Clear instructions on first load
- Obvious "Reset API key" option
- Copy-to-clipboard buttons
- Mobile-friendly touch targets

**Reliability:**
- Graceful error handling
- Works offline after first load (if no API needed)
- No external CSS/fonts that might fail

**Performance:**
- Lazy-load heavy libraries only when needed
- Use async/await properly
- Don't block the main thread
