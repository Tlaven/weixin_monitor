# Weixin Monitor

Weixin Monitor is a Python-based application designed to monitor and analyze chat content in real-time from a specified Windows application window (e.g., WeChat). It captures screenshots of the chat region, detects updates, extracts text using OCR, analyzes content with AI, and triggers alerts for significant messages. The project is built with a modular architecture, leveraging tools like PaddleOCR, OpenCV, and DashScope AI for robust functionality.

## Features
- **Real-Time Chat Monitoring**: Continuously captures and monitors a specified chat window region for new messages.
- **Change Detection**: Uses pixel difference analysis to detect chat updates with a debounce mechanism to avoid redundant processing.
- **OCR Processing**: Extracts text from screenshots using PaddleOCR with preprocessing for enhanced accuracy.
- **AI Analysis**: Analyzes extracted text or images using DashScope API to identify significant content based on configurable prompts.
- **Automated Interaction**: Simulates mouse clicks to interact with the application UI (e.g., opening/closing details windows).
- **Alert System**: Plays an audio alert (`alert.wav`) when significant content is detected.
- **Logging**: Comprehensive logging with Loguru to a rotating log file (`logs/app.log`) for debugging and monitoring.
- **Configurable**: Uses a configuration file (`config.config`) for window titles, regions, thresholds, and API settings.

## Requirements
- **Operating System**: Windows (due to `pywin32` dependency for window handling).
- **Python**: Version 3.12 or higher.
- **Dependencies**: Managed via Poetry (see `pyproject.toml`).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/weixin_monitor.git
   cd weixin_monitor
   ```

2. **Install Poetry** (if not already installed):
   ```bash
   pip install poetry
   ```

3. **Install Dependencies**:
   ```bash
   poetry install
   ```

4. **Activate Virtual Environment**:
   ```bash
   poetry shell
   ```

5. **Configure Settings**:
   - Create a `config/config.py` file (or update the existing one) with necessary configurations:
     - `app.window_title`: Title of the target application window (e.g., "WeChat").
     - `app.details_window_title`: Title of the details window.
     - `chat_box`: Dictionary with `x`, `y_offset`, `width`, `height` for the chat region.
     - `paths.screenshots`, `paths.judgments`, `paths.ocr_results`: Directories for saving screenshots, judgments, and OCR results.
     - `ai.base_url`, `ai.prompt`: DashScope API base URL and prompt for AI analysis.
     - `thresholds.change_detection`: Pixel difference threshold for detecting chat updates.
     - `app.polling_interval`: Interval (in seconds) for monitoring loop.
   - Set the `DASHSCOPE_API_KEY` environment variable for AI analysis:
     ```bash
     export DASHSCOPE_API_KEY=your_api_key
     ```

6. **Provide Alert Sound**:
   - Place an `alert.wav` file in the project root for the alert system (`alert_service.py`).

## Usage
1. **Start the Monitor**:
   ```bash
   poetry run python main.py
   ```
   The application will start monitoring the specified chat window, detecting updates, extracting text, analyzing content, and triggering alerts as configured.

2. **Output**:
   - Screenshots are saved to the configured `paths.screenshots` directory.
   - Significant content (based on AI analysis) is saved to `paths.judgments`.
   - OCR results are appended to `ocr_results.json` in `paths.ocr_results`.
   - Logs are written to `logs/app.log`.

3. **Stop Monitoring**:
   - Press `Ctrl+C` to stop the monitoring loop gracefully.

## Project Structure
```
weixin_monitor/
├── config/
│   └── config.py           # Configuration settings
├── core/
│   ├── ai_analyzer.py      # AI analysis with DashScope API
│   ├── chat_monitor.py     # Chat update detection
│   ├── image_processor.py  # Image encoding and saving
│   ├── ocr_processor.py    # OCR text extraction
│   └── window_manager.py   # Window handling and screenshot capture
├── services/
│   ├── alert_service.py    # Audio alert system
│   ├── analysis_service.py # AI-based content analysis
│   └── screenshot_service.py # Screenshot capture orchestration
├── utils/
│   ├── file_utils.py      # File operations (e.g., saving images)
│   └── logger.py          # Logging setup with Loguru
├── logs/
│   └── app.log            # Log files
├── main.py                # Main monitoring loop
├── pyproject.toml         # Poetry configuration
└── README.md              # This file
```

## Dependencies
Managed via Poetry (`pyproject.toml`):
- `paddleocr>=2.8.1`: For OCR text extraction.
- `paddlepaddle>=2.6.1`: PaddlePaddle framework for OCR.
- `opencv-python>=4.10.0`: Image processing.
- `pillow>=10.4.0`: Image handling.
- `numpy>=1.26.4`: Numerical operations.
- `openai>=1.8.0`: DashScope API integration.
- `pywin32>=306`: Windows API for window handling.
- `setuptools>=80.2.0`: Build tools.
- `pygame>=2.6.0`: Audio alerts.

## Notes
- The project is Windows-specific due to `pywin32` usage. For cross-platform support, the `WindowManager` class would need adaptation.
- Ensure the target application window is open and correctly titled as per `CONFIG` settings.
- Performance may vary based on the polling interval and system resources; adjust `app.polling_interval` and `thresholds.change_detection` as needed.
- The `alert.wav` file must be provided for audio alerts to work.

## Contributing
Contributions are welcome! Please submit issues or pull requests to the repository.

## License
This project is licensed under the MIT License (or specify your preferred license).