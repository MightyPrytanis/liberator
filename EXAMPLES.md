# Liberator Examples

## Example 1: Liberating a Simple Replit Python App

### Source Project Structure
```
my-replit-app/
├── .replit
├── main.py
├── requirements.txt
└── .env
```

### Command
```bash
liberator extract ./my-replit-app -o ./liberated-app
```

### Output
```
🔍 Detecting platform for: ./my-replit-app
✓ Detected platform: ReplitExtractor
📦 Extracting files...
✓ Extracted 3 files
✓ Found 5 dependencies

📤 Exporting to portable format...

✅ Successfully liberated project!
   Output: ./liberated-app
   Files: 3
   Dependencies: 5
```

### Generated Structure
```
liberated-app/
├── main.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

## Example 2: Liberating a Base44 Node.js App

### Source Project Structure
```
my-base44-app/
├── .base44
├── package.json
├── src/
│   ├── index.js
│   └── components/
│       └── App.js
└── public/
    └── index.html
```

### Command
```bash
liberator extract ./my-base44-app -o ./liberated-app --platform base44
```

### Output
The tool will:
1. Extract all source files
2. Analyze package.json dependencies
3. Generate Docker setup
4. Create comprehensive README

## Example 3: Analyzing Dependencies

### Command
```bash
liberator analyze ./my-project --verbose --output analysis.json
```

### Output
```
🔬 Analyzing project: ./my-project

📊 Analysis Results:
   Files analyzed: 15
   Languages: javascript, typescript

📦 Dependencies:
   NPM: 12
     - react@18.2.0
     - express@4.18.0
     - axios@1.4.0
     ... and 9 more

💾 Analysis saved to: analysis.json
```

## Example 4: Full Workflow

```bash
# Step 1: Analyze the project first
liberator analyze ./captive-project --output analysis.json

# Step 2: Extract and liberate
liberator extract ./captive-project -o ./liberated --analyze --verbose

# Step 3: Review the liberated project
cd liberated
cat README.md
```

## Example 5: Custom Platform (Generic)

For platforms not specifically supported:

```bash
liberator extract ./unknown-platform-app -o ./liberated --platform generic
```

The generic extractor will:
- Extract all files
- Attempt to detect dependencies from common config files
- Generate standard project structure
