#!/bin/bash
# Setup script for PDF to Markdown Converter

# #region agent log
mkdir -p /Users/habuild/codes/ocr/.cursor 2>&1 || true
echo "{\"id\":\"log_$(date +%s)_start\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:4\",\"message\":\"Script execution started\",\"data\":{\"shell\":\"$SHELL\",\"pwd\":\"$(pwd)\",\"script_path\":\"$0\",\"args\":\"$@\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"A,B,C,D,E,F\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true 2>&1 || true
# #endregion

set -e

# #region agent log
echo "{\"id\":\"log_$(date +%s)_sete\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:7\",\"message\":\"set -e executed successfully\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"C\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true 2>/dev/null || true
# #endregion

# #region agent log
echo "{\"id\":\"log_$(date +%s)_before_echo\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:10\",\"message\":\"Before first echo command\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"C,D\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion

echo "Setting up PDF to Markdown Converter..."

# #region agent log
echo "{\"id\":\"log_$(date +%s)_after_echo1\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:13\",\"message\":\"First echo command executed\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"C,D\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion

echo ""

# #region agent log
echo "{\"id\":\"log_$(date +%s)_after_echo2\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:16\",\"message\":\"Second echo command executed\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"C,D\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion

# Check for Python 3.10+
# #region agent log
echo "{\"id\":\"log_$(date +%s)_before_python_check\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:25\",\"message\":\"Before Python version check\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"C\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion
PYTHON_CMD=""
# #region agent log
echo "{\"id\":\"log_$(date +%s)_python_search_start\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:36\",\"message\":\"Starting Python version search\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"G\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion
if command -v python3.14 &> /dev/null; then
    PYTHON_CMD="python3.14"
    # #region agent log
    echo "{\"id\":\"log_$(date +%s)_python_found\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:39\",\"message\":\"Python version found\",\"data\":{\"python_cmd\":\"$PYTHON_CMD\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"G\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
    # #endregion
    echo "✓ Found Python 3.14"
elif command -v python3.13 &> /dev/null; then
    PYTHON_CMD="python3.13"
    # #region agent log
    echo "{\"id\":\"log_$(date +%s)_python_found\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:44\",\"message\":\"Python version found\",\"data\":{\"python_cmd\":\"$PYTHON_CMD\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"G\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
    # #endregion
    echo "✓ Found Python 3.13"
elif command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
    # #region agent log
    echo "{\"id\":\"log_$(date +%s)_python_found\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:49\",\"message\":\"Python version found\",\"data\":{\"python_cmd\":\"$PYTHON_CMD\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"G\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
    # #endregion
    echo "✓ Found Python 3.12"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    # #region agent log
    echo "{\"id\":\"log_$(date +%s)_python_found\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:54\",\"message\":\"Python version found\",\"data\":{\"python_cmd\":\"$PYTHON_CMD\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"G\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
    # #endregion
    echo "✓ Found Python 3.11"
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
    # #region agent log
    echo "{\"id\":\"log_$(date +%s)_python_found\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:59\",\"message\":\"Python version found\",\"data\":{\"python_cmd\":\"$PYTHON_CMD\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"G\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
    # #endregion
    echo "✓ Found Python 3.10"
else
    # #region agent log
    echo "{\"id\":\"log_$(date +%s)_python_not_found\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:64\",\"message\":\"Python 3.10+ not found\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"G\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
    # #endregion
    echo "✗ Error: Python 3.10 or higher is required"
    echo "  Please install Python 3.10+ first:"
    echo "    macOS: brew install python@3.10"
    echo "    Or download from: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
# #region agent log
echo "{\"id\":\"log_$(date +%s)_before_version_check\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:72\",\"message\":\"Before Python version check\",\"data\":{\"python_cmd\":\"$PYTHON_CMD\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"G\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
# #region agent log
echo "{\"id\":\"log_$(date +%s)_version_check_result\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:75\",\"message\":\"Python version check result\",\"data\":{\"python_version\":\"$PYTHON_VERSION\",\"exit_code\":\"$?\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"G\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion
echo "  Using: $PYTHON_VERSION"
echo ""

# Create or recreate venv
# #region agent log
echo "{\"id\":\"log_$(date +%s)_before_venv_check\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:82\",\"message\":\"Before venv check\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"H\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion
if [ -d "venv" ]; then
    echo "Recreating virtual environment with $PYTHON_CMD..."
    # #region agent log
    echo "{\"id\":\"log_$(date +%s)_venv_exists\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:85\",\"message\":\"Venv exists, removing\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"H\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
    # #endregion
    rm -rf venv
else
    echo "Creating virtual environment with $PYTHON_CMD..."
    # #region agent log
    echo "{\"id\":\"log_$(date +%s)_venv_not_exists\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:90\",\"message\":\"Venv does not exist, creating\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"H\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
    # #endregion
fi

# #region agent log
echo "{\"id\":\"log_$(date +%s)_before_venv_create\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:94\",\"message\":\"Before venv creation\",\"data\":{\"python_cmd\":\"$PYTHON_CMD\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"H\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion
$PYTHON_CMD -m venv venv
# #region agent log
echo "{\"id\":\"log_$(date +%s)_after_venv_create\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:96\",\"message\":\"After venv creation\",\"data\":{\"exit_code\":\"$?\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"H\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion

# Activate venv
echo "Activating virtual environment..."
# #region agent log
echo "{\"id\":\"log_$(date +%s)_before_venv_activate\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:101\",\"message\":\"Before venv activation\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"I\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion
source venv/bin/activate
# #region agent log
echo "{\"id\":\"log_$(date +%s)_after_venv_activate\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:104\",\"message\":\"After venv activation\",\"data\":{\"exit_code\":\"$?\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"I\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion

# Upgrade pip
echo "Upgrading pip..."
# #region agent log
echo "{\"id\":\"log_$(date +%s)_before_pip_upgrade\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:109\",\"message\":\"Before pip upgrade\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"J\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion
pip install --upgrade pip > /dev/null 2>&1
# #region agent log
echo "{\"id\":\"log_$(date +%s)_after_pip_upgrade\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:111\",\"message\":\"After pip upgrade\",\"data\":{\"exit_code\":\"$?\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"J\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion

# Install dependencies
echo "Installing dependencies (this may take a few minutes)..."
# #region agent log
echo "{\"id\":\"log_$(date +%s)_before_pip_install\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:116\",\"message\":\"Before pip install\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"K\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion
pip install -r requirements.txt
# #region agent log
echo "{\"id\":\"log_$(date +%s)_after_pip_install\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:118\",\"message\":\"After pip install\",\"data\":{\"exit_code\":\"$?\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"K\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion

echo ""
echo "✓ Setup complete!"
echo ""
echo "To use the converter:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the converter:"
echo "     python main.py your_file.pdf"
echo ""

# #region agent log
echo "{\"id\":\"log_$(date +%s)_script_complete\",\"timestamp\":$(date +%s)000,\"location\":\"setup.sh:130\",\"message\":\"Script completed successfully\",\"data\":{},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"ALL\"}" >> /Users/habuild/codes/ocr/.cursor/debug.log 2>/dev/null || true
# #endregion