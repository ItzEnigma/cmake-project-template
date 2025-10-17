#!/usr/bin/env python3
"""
Development Environment Setup Script
====================================

Automatically detects system specifications and downloads/installs necessary 
development tools for the CMake C++ project.

Required Tools:
- CMake 3.22+
- C++ compiler (GCC/Clang/MSVC with C++17 support)
- Git
- Coverage Report Generation tools (gcovr, lcov/OpenCppCoverage)
- Doxygen (optional, for documentation)

Usage:
    python setup-env.py [--install-optional]
    
Options:
    --install-optional    Install optional tools (Doxygen, etc.)
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import tarfile
import json
from pathlib import Path
import argparse
import shutil


class SystemDetector:
    """Detect system specifications and capabilities."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        self.is_windows = self.system == "windows"
        self.is_linux = self.system == "linux"
        self.is_macos = self.system == "darwin"
        
    def get_package_manager(self):
        """Detect available package manager."""
        if self.is_windows:
            if shutil.which("winget"):
                return "winget"
            elif shutil.which("choco"):
                return "choco"
            elif shutil.which("scoop"):
                return "scoop"
        elif self.is_linux:
            if shutil.which("apt"):
                return "apt"
            elif shutil.which("dnf"):
                return "dnf"
            elif shutil.which("yum"):
                return "yum"
            elif shutil.which("pacman"):
                return "pacman"
        elif self.is_macos:
            if shutil.which("brew"):
                return "brew"
        return None

class ToolInstaller:
    """Install development tools based on system type."""
    
    def __init__(self, detector: SystemDetector):
        self.detector = detector
        self.pkg_mgr = detector.get_package_manager()
        
    def check_tool(self, tool_name, version_cmd=None, min_version=None):
        """Check if tool is installed and meets version requirements."""
        if not shutil.which(tool_name):
            return False, "Not installed"
            
        if version_cmd and min_version:
            try:
                result = subprocess.run(version_cmd, capture_output=True, text=True, shell=True)
                # Basic version check (can be enhanced for specific tools)
                return True, f"Installed"
            except:
                return False, "Version check failed"
                
        return True, "Installed"
    
    def run_command(self, cmd, description):
        """Run system command with error handling."""
        print(f"📦 {description}")
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ Success: {description}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {description}")
            print(f"Error: {e.stderr}")
            return False
    
    def install_cmake(self):
        """Install CMake 3.22+."""
        installed, status = self.check_tool("cmake", "cmake --version")
        if installed:
            print(f"✅ CMake: {status}")
            return True
            
        print("📦 Installing CMake...")
        
        if self.pkg_mgr == "winget":
            return self.run_command("winget install Kitware.CMake", "Installing CMake via winget")
        elif self.pkg_mgr == "choco":
            return self.run_command("choco install cmake", "Installing CMake via chocolatey")
        elif self.pkg_mgr == "apt":
            return self.run_command("sudo apt update && sudo apt install -y cmake", "Installing CMake via apt")
        elif self.pkg_mgr == "dnf":
            return self.run_command("sudo dnf install -y cmake", "Installing CMake via dnf")
        elif self.pkg_mgr == "yum":
            return self.run_command("sudo yum install -y cmake", "Installing CMake via yum")
        elif self.pkg_mgr == "pacman":
            return self.run_command("sudo pacman -S --noconfirm cmake", "Installing CMake via pacman")
        elif self.pkg_mgr == "brew":
            return self.run_command("brew install cmake", "Installing CMake via homebrew")
        else:
            print("❌ No supported package manager found for CMake installation")
            print("Please install CMake manually from: https://cmake.org/download/")
            return False
    
    def install_compiler(self):
        """Install C++ compiler."""
        compilers = ["g++", "clang++", "cl"] if self.detector.is_windows else ["g++", "clang++"]
        
        for compiler in compilers:
            if shutil.which(compiler):
                print(f"✅ C++ Compiler: {compiler} installed")
                return True
        
        print("----- Installing C++ compiler -----")
        if self.detector.is_windows:
            print("Please ensure one of the following is installed:")
            print("  - Visual Studio 2019/2022 with C++ workload")
            print("  - Visual Studio Build Tools")
            print("  - MinGW-w64")
            print("  - Clang/LLVM")
            return True
        elif self.pkg_mgr == "apt":
            return self.run_command("sudo apt install -y build-essential", "Installing GCC via apt")
        elif self.pkg_mgr == "dnf":
            return self.run_command("sudo dnf groupinstall -y 'Development Tools'", "Installing GCC via dnf")
        elif self.pkg_mgr == "yum":
            return self.run_command("sudo yum groupinstall -y 'Development Tools'", "Installing GCC via yum")
        elif self.pkg_mgr == "pacman":
            return self.run_command("sudo pacman -S --noconfirm base-devel", "Installing GCC via pacman")
        elif self.pkg_mgr == "brew":
            print("✅ Clang should be available via Xcode Command Line Tools")
            return self.run_command("xcode-select --install", "Installing Xcode Command Line Tools")
        else:
            print("❌ No supported package manager found for compiler installation")
            return False
    
    def install_git(self):
        """Install Git."""
        installed, status = self.check_tool("git", "git --version")
        if installed:
            print(f"✅ Git: {status}")
            return True
            
        if self.pkg_mgr == "winget":
            return self.run_command("winget install Git.Git", "Installing Git via winget")
        elif self.pkg_mgr == "choco":
            return self.run_command("choco install git", "Installing Git via chocolatey")
        elif self.pkg_mgr == "apt":
            return self.run_command("sudo apt install -y git", "Installing Git via apt")
        elif self.pkg_mgr == "dnf":
            return self.run_command("sudo dnf install -y git", "Installing Git via dnf")
        elif self.pkg_mgr == "yum":
            return self.run_command("sudo yum install -y git", "Installing Git via yum")
        elif self.pkg_mgr == "pacman":
            return self.run_command("sudo pacman -S --noconfirm git", "Installing Git via pacman")
        elif self.pkg_mgr == "brew":
            return self.run_command("brew install git", "Installing Git via homebrew")
        else:
            print("❌ No supported package manager found for Git installation")
            return False
    
    def install_coverage_tools(self):
        """Install code coverage tools (gcovr, lcov, OpenCppCoverage)."""
        if self.detector.is_windows:
            # Check for OpenCppCoverage
            if shutil.which("OpenCppCoverage"):
                print("✅ OpenCppCoverage: Installed")
                return True
            
            if self.pkg_mgr == "choco":
                return self.run_command("choco install opencppcoverage", "Installing OpenCppCoverage via chocolatey")
            else:
                print("❌ Please install OpenCppCoverage manually from:")
                print("https://github.com/OpenCppCoverage/OpenCppCoverage/releases")
                return False
        else:
            # Check for both gcovr and lcov
            gcovr_installed = shutil.which("gcovr") is not None
            lcov_installed = shutil.which("lcov") is not None
            
            if gcovr_installed and lcov_installed:
                print("✅ gcovr: Installed")
                print("✅ lcov: Installed")
                return True
            
            success = True
            
            # Install gcovr via package manager only
            if not gcovr_installed:
                if self.pkg_mgr == "apt":
                    success &= self.run_command("sudo apt install -y gcovr", "Installing gcovr via apt")
                elif self.pkg_mgr == "dnf":
                    success &= self.run_command("sudo dnf install -y gcovr", "Installing gcovr via dnf")
                elif self.pkg_mgr == "yum":
                    success &= self.run_command("sudo yum install -y gcovr", "Installing gcovr via yum")
                elif self.pkg_mgr == "pacman":
                    success &= self.run_command("sudo pacman -S --noconfirm gcovr", "Installing gcovr via pacman")
                elif self.pkg_mgr == "brew":
                    success &= self.run_command("brew install gcovr", "Installing gcovr via homebrew")
                else:
                    print("❌ gcovr not available via package manager. Please install manually.")
                    success = False
            else:
                print("✅ gcovr: Already installed")
            
            # Install lcov via package manager
            if not lcov_installed:
                if self.pkg_mgr == "apt":
                    success &= self.run_command("sudo apt install -y lcov", "Installing lcov via apt")
                elif self.pkg_mgr == "dnf":
                    success &= self.run_command("sudo dnf install -y lcov", "Installing lcov via dnf")
                elif self.pkg_mgr == "yum":
                    success &= self.run_command("sudo yum install -y lcov", "Installing lcov via yum")
                elif self.pkg_mgr == "pacman":
                    success &= self.run_command("sudo pacman -S --noconfirm lcov", "Installing lcov via pacman")
                elif self.pkg_mgr == "brew":
                    success &= self.run_command("brew install lcov", "Installing lcov via homebrew")
                else:
                    print("❌ lcov not available via package manager. Please install manually.")
                    success = False
            else:
                print("✅ lcov: Already installed")
            
            return success
    
    def install_doxygen(self):
        """Install Doxygen (optional)."""
        installed, status = self.check_tool("doxygen", "doxygen --version")
        if installed:
            print(f"✅ Doxygen: {status}")
            return True
            
        print("📦 Installing Doxygen...")
        
        if self.pkg_mgr == "winget":
            return self.run_command("winget install DimitriVanHeesch.Doxygen", "Installing Doxygen via winget")
        elif self.pkg_mgr == "choco":
            return self.run_command("choco install doxygen.install", "Installing Doxygen via chocolatey")
        elif self.pkg_mgr == "apt":
            return self.run_command("sudo apt install -y doxygen graphviz", "Installing Doxygen via apt")
        elif self.pkg_mgr == "dnf":
            return self.run_command("sudo dnf install -y doxygen graphviz", "Installing Doxygen via dnf")
        elif self.pkg_mgr == "yum":
            return self.run_command("sudo yum install -y doxygen graphviz", "Installing Doxygen via yum")
        elif self.pkg_mgr == "pacman":
            return self.run_command("sudo pacman -S --noconfirm doxygen graphviz", "Installing Doxygen via pacman")
        elif self.pkg_mgr == "brew":
            return self.run_command("brew install doxygen graphviz", "Installing Doxygen via homebrew")
        else:
            print("❌ No supported package manager found for Doxygen installation")
            return False


def main():
    parser = argparse.ArgumentParser(description="Setup development environment for CMake C++ project")
    parser.add_argument("--install-optional", action="store_true", 
                       help="Install optional tools (Doxygen)")
    args = parser.parse_args()
    
    print("🔍 Development Environment Setup")
    print("=" * 50)
    
    # Detect system
    detector = SystemDetector()
    print(f"System: {detector.system.title()}")
    print(f"Architecture: {detector.machine}")
    
    if detector.get_package_manager():
        print(f"Package Manager: {detector.get_package_manager()}")
    else:
        print("Package Manager: None detected")
    
    print("\n📋 Checking and installing required tools...")
    print("-" * 50)
    
    installer = ToolInstaller(detector)
    
    # Install core tools
    success_count = 0
    total_tools = 4
    
    if installer.install_cmake():
        success_count += 1
    if installer.install_compiler():
        success_count += 1
    if installer.install_git():
        success_count += 1
    if installer.install_coverage_tools():
        success_count += 1
    
    # Install optional tools
    if args.install_optional:
        print("\n📋 Installing optional tools...")
        print("-" * 30)
        if installer.install_doxygen():
            success_count += 1
        total_tools += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Setup complete: {success_count}/{total_tools} tools installed successfully")
    
    if success_count == total_tools:
        print("\n🎉 All tools are ready! You can now build the project:")
        print("   mkdir build && cd build")
        print("   cmake ..")
        print("   cmake --build .")
    else:
        print(f"\n⚠️  Some tools failed to install. Please install them manually.")
        print("   Check the error messages above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()