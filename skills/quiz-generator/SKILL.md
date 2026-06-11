---
name: quiz-generator
description: Generate quiz JSON files from any content and launch the interactive quiz app. Creates multiple-choice and open-ended questions, then opens the quiz in the browser.
---

# Quiz Generator Skill

Generate quiz JSON files from any topic, content, or resource, then launch an interactive quiz application to test knowledge immediately.

## When to Use This Skill

Use this skill when the user requests:
- Creating quizzes from text, URLs, or topics
- Testing themselves on specific content
- Generating practice questions
- Building flashcard-style question sets
- Self-assessment on any subject matter

Trigger phrases: "quiz me on", "test me on", "create a quiz", "generate questions about", "make quiz questions", "test my knowledge", "practice questions for"

## Quiz JSON Format

The quiz app expects a JSON array with two question types:

### Multiple Choice Questions

```json
{
  "question": "What is the capital of France?",
  "type": "multiple-choice",
  "options": ["London", "Berlin", "Paris", "Madrid"],
  "correctAnswer": 2
}
```

**Rules:**
- `options`: Array of 3-5 answer choices
- `correctAnswer`: Zero-indexed integer pointing to correct option
- Place the correct answer randomly (not always first or last)
- Make distractors plausible but clearly wrong to someone who knows the material

### Open-Ended Questions

```json
{
  "question": "What is 2 + 2?",
  "type": "open-ended",
  "acceptedAnswers": ["4", "four", "Four"]
}
```

**Rules:**
- `acceptedAnswers`: Array of valid answer variations (case-insensitive matching)
- Include common phrasings, abbreviations, and alternate spellings
- Keep expected answers concise (1-3 words typically)
- Good for definitions, short answers, and recall questions

## Workflow

### 1. Gather Content

**For topic-based quizzes:**
- Use your knowledge to generate relevant questions
- Cover key concepts, definitions, and important details
- Include a mix of difficulty levels

**For URL-based quizzes:**
- Use WebFetch to retrieve the content
- Extract key facts, concepts, and relationships
- Generate questions that test comprehension

**For user-provided content:**
- Parse the text to identify testable concepts
- Create questions covering main points
- Include both factual and conceptual questions

### 2. Generate Quiz Questions

Create a balanced mix:
- **60-70% multiple-choice**: Test recognition and understanding
- **30-40% open-ended**: Test recall and deeper knowledge

**Question quality guidelines:**
- Clear, unambiguous wording
- One correct answer per question
- Distractors that are plausible but incorrect
- Avoid "all of the above" or "none of the above"
- Test understanding, not trick questions
- Vary difficulty: some easy, some challenging

**Recommended quiz length:**
- Quick quiz: 5-10 questions
- Standard quiz: 10-20 questions
- Comprehensive: 20-30 questions

### 3. Save the Quiz JSON

Save the quiz JSON file to the current working directory (or wherever the user asks):

```
./<topic-slug>-quiz.json
```

**Naming convention:**
- Use lowercase with hyphens
- Include descriptive topic name
- End with `-quiz.json`

Examples:
- `python-basics-quiz.json`
- `ai-fluency-quiz.json`
- `javascript-arrays-quiz.json`

### 4. Launch the Quiz App (Auto-Loaded)

After saving the JSON, launch the quiz app with the quiz **pre-loaded and auto-started** so the user can begin immediately — no manual file picking required.

The quiz app is bundled with this skill at `assets/quiz-app.html` — a single self-contained HTML file, no build step, no server. It supports a URL hash protocol:
`quiz-app.html#quiz=<base64-encoded-json>&autostart=1`

Use this Python one-liner to base64-encode the JSON and open the app with the quiz embedded in the URL hash. The hash is processed locally by the browser and works with `file://` URLs (no server needed):

```bash
python3 -c "
import base64, urllib.parse, pathlib, subprocess, time
json_path = '<path-to>/<topic-slug>-quiz.json'
app_path  = '<skill-dir>/assets/quiz-app.html'  # resolve from this skill's folder
data = pathlib.Path(json_path).read_text()
encoded = base64.b64encode(data.encode('utf-8')).decode('ascii')
# Cache-buster query param forces the page to reload even if a stale tab is already open.
url = f'file://{app_path}?t={int(time.time())}#quiz={urllib.parse.quote(encoded)}&autostart=1'
subprocess.run(['open', url])  # macOS; use xdg-open on Linux
"
```

Replace the two placeholder paths with the actual saved JSON file and this skill's `assets/quiz-app.html` (absolute paths).

The quiz will be open and ready to answer the first question. The JSON file is still saved to disk so the user can reload it later via "Choose Quiz File" if desired.

**Fallback:** if the auto-load URL approach fails for any reason, open `assets/quiz-app.html` directly and tell the user to pick the JSON file manually via "Choose Quiz File".

## Example Workflows

### Example 1: Topic-based quiz

```
User: "Quiz me on JavaScript array methods"

Actions:
1. Generate 10-15 questions about array methods (map, filter, reduce, forEach, etc.)
2. Include multiple-choice for method selection and open-ended for syntax
3. Save as ./javascript-arrays-quiz.json
4. Run the auto-load Python one-liner from step 4 above (pointing at javascript-arrays-quiz.json) — quiz opens auto-started on question 1
5. Tell user: "Quiz is loaded and ready — answer away."
```

### Example 2: URL-based quiz

```
User: "Create a quiz from this article: https://example.com/python-tutorial"

Actions:
1. WebFetch the URL to extract content
2. Identify key concepts and generate 10-15 questions
3. Save as ./python-tutorial-quiz.json
4. Run the auto-load Python one-liner to open the app with the quiz embedded in the URL hash and auto-started
5. Tell user: "Quiz is loaded and ready to start."
```

### Example 3: Content-based quiz

```
User: "Test me on this content: [user provides text or notes]"

Actions:
1. Parse the provided content
2. Extract key facts and concepts
3. Generate questions covering the material
4. Save with descriptive filename
5. Launch quiz app
```

## Question Templates

### Multiple-Choice Patterns

**Definition questions:**
```json
{
  "question": "What is [term]?",
  "type": "multiple-choice",
  "options": ["Correct definition", "Related but wrong", "Common misconception", "Unrelated concept"],
  "correctAnswer": 0
}
```

**Best practice questions:**
```json
{
  "question": "What is the recommended way to [action]?",
  "type": "multiple-choice",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correctAnswer": 2
}
```

**Comparison questions:**
```json
{
  "question": "What is the key difference between [X] and [Y]?",
  "type": "multiple-choice",
  "options": ["Difference A", "Difference B", "They are the same", "Difference C"],
  "correctAnswer": 0
}
```

### Open-Ended Patterns

**Short answer:**
```json
{
  "question": "What command is used to [action]?",
  "type": "open-ended",
  "acceptedAnswers": ["command", "command()", "the command command"]
}
```

**Definition recall:**
```json
{
  "question": "Define [term] in one or two words.",
  "type": "open-ended",
  "acceptedAnswers": ["answer1", "answer2", "Answer1"]
}
```

## Quality Checklist

Before saving the quiz file, verify:

**Content:**
- [ ] Questions are clear and unambiguous
- [ ] Each question has exactly one correct answer
- [ ] Multiple-choice distractors are plausible
- [ ] Open-ended acceptedAnswers include common variations
- [ ] Mix of difficulty levels included
- [ ] No duplicate questions

**Format:**
- [ ] Valid JSON array structure
- [ ] Each object has required fields (question, type)
- [ ] Multiple-choice: options array and correctAnswer integer
- [ ] Open-ended: acceptedAnswers array
- [ ] correctAnswer is valid index (0 to options.length - 1)

**File:**
- [ ] Saved to the working directory (or user-specified location)
- [ ] Descriptive filename with -quiz.json suffix
- [ ] No spaces in filename

## Error Handling

**If user wants more/fewer questions:**
- Adjust the count based on their preference
- Quick assessment: 5-8 questions
- Standard review: 10-15 questions
- Comprehensive test: 20-30 questions

**If content is too short for many questions:**
- Generate quality over quantity
- Focus on key concepts
- Explain that limited content means fewer questions

**If quiz app doesn't open:**
- Provide the file path for manual opening
- Instruct user to open quiz-app.html in browser
- Remind them to select the generated JSON file

## Tips for Success

**Writing good questions:**
- Focus on understanding, not memorization
- Avoid negatively phrased questions when possible
- Make sure context is provided in the question
- Test one concept per question

**Creating effective distractors:**
- Use common misconceptions
- Include related but incorrect terms
- Avoid obviously wrong answers
- Keep answer lengths similar

**Open-ended answers:**
- Include singular and plural forms
- Add common abbreviations
- Consider case variations (already case-insensitive)
- Keep accepted answers to reasonable variations
