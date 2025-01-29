# Thought Tag Remover

## Overview
This project is designed to filter out "thought tags" from conversations with an AI model, ensuring cleaner and more readable interactions. It works by processing the output from the model and removing any thought-related metadata, leaving only the final responses.

## Dependencies
- **[Ollama](https://ollama.ai/)** (Required to run the AI model locally)
- A locally installed AI model (Must be specified in the `MODEL` variable)

## Setup
1. Ensure **Ollama** is installed and running on your system.
2. Download and install your preferred AI model through Ollama.
3. Set the `MODEL` variable in the code to match the installed model.
4. Run the script to start filtering out thought tags from the AI responses.

## Usage
- The selected model is defined in the `MODEL` global variable.
- The model name is also displayed in the **window title** for clarity.
- The script will process AI responses and remove any thought tags automatically.

## Example
Before:
```
[THOUGHT] The user might be asking about installation steps.
Response: You can install Ollama by downloading it from their official website.
```

After:
```
Response: You can install Ollama by downloading it from their official website.
```

## Notes
- If the model is not installed or incorrectly specified in `MODEL`, the script will not function correctly.
- This tool does not modify the model's behavior but simply processes the output for readability.

## TODO:
- Seperate out the concerns of removing the thoughts, from the concern of a UI frontend for this data. This repo should primarily be focused on being a lean mean thought-cutting machine. A default gui may be provided, but it will use the same general backend API for a daemon.

## License
This project is licensed under the MIT License. You are free to use, modify, distribute, and even use it commercially. 
