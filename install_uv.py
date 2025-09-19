"""
UV Installation Script
Installs uv and sets up the project environment.
"""

import subprocess
import sys
import os
import platform


def install_uv():
    """Install uv package manager."""
    print("Installing uv package manager...")
    
    system = platform.system().lower()
    
    try:
        if system == "windows":
            # Install uv on Windows
            cmd = 'powershell -c "irm https://astral.sh/uv/install.ps1 | iex"'
            subprocess.run(cmd, shell=True, check=True)
        else:
            # Install uv on macOS/Linux
            cmd = "curl -LsSf https://astral.sh/uv/install.sh | sh"
            subprocess.run(cmd, shell=True, check=True)
        
        print("✓ uv installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install uv: {e}")
        return False


def setup_project():
    """Set up the project with uv."""
    print("Setting up project with uv...")
    
    try:
        # Sync dependencies
        subprocess.run(["uv", "sync"], check=True)
        print("✓ Dependencies installed successfully")
        
        # Create activation script
        create_activation_script()
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to set up project: {e}")
        return False


def create_activation_script():
    """Create activation script for easy environment activation."""
    system = platform.system().lower()
    
    if system == "windows":
        script_content = """@echo off
echo Activating PDF Text Summarizer environment...
call .venv\\Scripts\\activate.bat
echo Environment activated! You can now run:
echo   python main.py your_document.pdf
echo   python summary_cli.py summarize-pdf your_document.pdf
echo   python voice_cli.py generate-voice summary.txt
pause
"""
        with open("activate_env.bat", "w") as f:
            f.write(script_content)
        print("✓ Created activate_env.bat for easy environment activation")
    else:
        script_content = """#!/bin/bash
echo "Activating PDF Text Summarizer environment..."
source .venv/bin/activate
echo "Environment activated! You can now run:"
echo "  python main.py your_document.pdf"
echo "  python summary_cli.py summarize-pdf your_document.pdf"
echo "  python voice_cli.py generate-voice summary.txt"
"""
        with open("activate_env.sh", "w") as f:
            f.write(script_content)
        os.chmod("activate_env.sh", 0o755)
        print("✓ Created activate_env.sh for easy environment activation")


def main():
    """Main installation process."""
    print("PDF TEXT SUMMARIZER - UV INSTALLATION")
    print("=" * 50)
    
    # Check if uv is already installed
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        print("✓ uv is already installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        if not install_uv():
            print("Failed to install uv. Please install manually:")
            print("  Windows: powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"")
            print("  macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh")
            return False
    
    # Set up project
    if not setup_project():
        return False
    
    print("\n" + "=" * 50)
    print("INSTALLATION COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Set up API keys:")
    print("   - OpenAI: https://platform.openai.com/api-keys")
    print("   - VBee: Contact VBee for TTS API access")
    print("2. Activate environment:")
    if platform.system().lower() == "windows":
        print("   Run: activate_env.bat")
        print("   Or: .venv\\Scripts\\activate")
    else:
        print("   Run: ./activate_env.sh")
        print("   Or: source .venv/bin/activate")
    print("3. Run the application:")
    print("   python main.py your_document.pdf")
    print("\nFor help: python main.py --help")


if __name__ == "__main__":
    main()
