# El AI Assistant and Sanskrit NLP Tool

A mobile-friendly AI assistant and Sanskrit NLP tool built with Kivy, designed for Android deployment.

## Features

- **Sanskrit Text Analysis**: Tokenization, grammar analysis, POS tagging, and semantics
- **Instruction Learning**: Teach the assistant new grammar rules and patterns
- **Code Generation**: Generate code with AI assistance
- **Repository Analysis**: Analyze code repositories for patterns and insights
- **Data Comparison**: Compare and visualize datasets
- **Model Training**: Train custom models for specific tasks
- **File Management**: Browse local files for model loading
- **Offline Capabilities**: Works without internet when local models are available

## Requirements

- Python 3.8+
- Kivy 2.1.0+
- Other dependencies as listed in `buildozer.spec`

## Installation

### For Development

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/el-ai-assistant.git
   cd el-ai-assistant
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python run.py
   ```

### Building for Android

1. Install Buildozer:
   ```
   pip install buildozer
   ```

2. Build the APK:
   ```
   buildozer android debug
   ```

3. The APK will be in the `bin` directory

## Usage

1. **API Keys**: Add API keys in the Settings screen to enable AI features
   - Gemma API
   - OpenAI (ChatGPT) API
   - IBM Quantum API

2. **Local Models**: Use Settings to browse and select local model files for offline use

3. **Sanskrit Analysis**: Enter Sanskrit text to analyze grammar, tokenization, and meaning

4. **Instruction Learning**: Teach new grammar rules by providing instructions

5. **Code Generation**: Generate code by providing a description of what you want

## Project Structure

- `kivy_app/`: Main application package
  - `models/`: Model handler and AI model integrations
  - `screens/`: Application screens
  - `styles/`: Kivy style files
  - `utils/`: Utility functions and helpers
  - `resources/`: Application resources
- `run.py`: Entry point for running the app
- `buildozer.spec`: Configuration for building Android APK

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.