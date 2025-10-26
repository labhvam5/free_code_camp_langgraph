# LangGraph Learning Project

A hands-on project for learning LangGraph with observability through LangSmith tracing.

## 📋 Prerequisites

- Docker installed and running
- Basic knowledge of Python
- LangSmith API key (optional, for observability)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd free_code_camp_langgraph
```

### 2. Configure LangSmith (Optional but Recommended)

Create a `.env` file in the project root:

```bash
# LangSmith Configuration
LANGSMITH_API_KEY=your_actual_api_key_here
LANGSMITH_PROJECT=langgraph-greeting-app
```

> **Note**: The `.env` file is already in `.gitignore` to prevent accidental commits of your API key.

### 3. Run with Docker

The project includes a convenient script to build and run the application:

```bash
chmod +x local.sh
./local.sh
```

This script will:
- Build the Docker image with all dependencies
- Start a container with hot-reload capabilities
- Mount your local directory for development

### 4. Execute Examples

Once the container is running, you can execute the example applications:

```bash
# Run the greeting example
docker exec free_code python basics/graph1.py

# Run the math operations example  
docker exec free_code python basics/graph2.py
```

## 📁 Project Structure

```
free_code_camp_langgraph/
├── basics/
│   ├── graph1.py          # Simple greeting LangGraph
│   └── graph2.py          # Math operations LangGraph
├── Dockerfile             # Container configuration
├── local.sh              # Build and run script
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🎯 Examples Explained

### Graph1.py - Simple Greeting
A basic LangGraph that demonstrates:
- Basic node creation and graph flow
- State management with TypedDict
- Simple string manipulation

**Input**: `{"message": "Alice"}`
**Output**: `{"message": "Hey Alice, how is your day going?"}`

### Graph2.py - Math Operations
A more complex example showing:
- Multiple data types in state
- Conditional logic in nodes
- List processing operations

**Input**: `{"values": [1, 2, 3, 4, 5], "name": "Alice", "operation": "+"}`
**Output**: Processed mathematical result with personalized message

## 🔍 LangSmith Observability

When properly configured with your LangSmith API key, you'll see:

✅ **Success indicators:**
```
🔍 LangSmith tracing enabled for project: langgraph-greeting-app
```

❌ **If not configured:**
```
ℹ️ LangSmith not configured. Set LANGSMITH_API_KEY and LANGSMITH_PROJECT to enable tracing.
```

### Viewing Traces

1. Visit [LangSmith](https://smith.langchain.com/)
2. Navigate to your project: `langgraph-greeting-app`
3. View detailed execution traces and performance metrics

## 🛠 Development Workflow

### Hot Reload Development

The Docker setup supports hot reload - any changes you make to the Python files will be immediately available in the container without rebuilding.

### Running Individual Files

```bash
# Access the container shell
docker exec -it free_code bash

# Run any Python file
python basics/graph1.py
python basics/graph2.py
```

### Stopping the Container

```bash
docker stop free_code
docker rm free_code
```

## 📚 Learning Path

1. **Start with Graph1.py** - Understand basic LangGraph concepts
2. **Move to Graph2.py** - Learn state management and conditional logic  
3. **Experiment** - Modify the examples and see results in LangSmith
4. **Build your own** - Create new graph examples

## 🔧 Troubleshooting

### Container Issues
```bash
# Rebuild if needed
docker build -t langgraph-app .
./local.sh
```

### Permission Issues
```bash
# Make script executable
chmod +x local.sh
```

### LangSmith Connection Issues
- Verify your API key is correct in `.env`
- Check that `.env` file is in the project root
- Ensure no trailing spaces in the API key

## 🤝 Contributing

Feel free to add new examples or improve existing ones. Follow the established patterns for consistency.