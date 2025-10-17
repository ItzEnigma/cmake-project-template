# Development Scripts

This directory contains scripts to help set up and manage the development environment.

## setup-env.py

Automatically detects your system and installs necessary development tools for this CMake C++ project.

### Required Tools Installed:
- **CMake 3.22+** - Build system generator
- **C++ Compiler** - GCC/Clang (Linux/macOS) or MSVC (Windows) with C++17 support
- **Git** - Version control and dependency fetching
- **Coverage Tools** - gcovr (Linux/macOS) or OpenCppCoverage (Windows)

### Optional Tools:
- **Doxygen** - Documentation generation (use `--install-optional`)

### Usage:

```bash
# Install required tools only
python scripts/setup-env.py

# Install required + optional tools
python scripts/setup-env.py --install-optional

# Show help
python scripts/setup-env.py --help
```

### Supported Systems:
- **Windows**: winget, chocolatey, scoop
- **Linux**: apt (Ubuntu/Debian), dnf/yum (RHEL/Fedora), pacman (Arch)
- **macOS**: homebrew

### After Setup:
Once the script completes successfully, you can build the project:

```bash
mkdir build && cd build
cmake ..
cmake --build .

# Run tests
ctest

# Generate coverage (if enabled)
cmake -DENABLE_COVERAGE=ON ..
make my_coverage  # or your coverage target name
```

### Manual Installation:
If the script fails to install some tools, you can install them manually:

- **CMake**: https://cmake.org/download/
- **Visual Studio Build Tools** (Windows): https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
- **OpenCppCoverage** (Windows): https://github.com/OpenCppCoverage/OpenCppCoverage/releases
- **Doxygen**: https://www.doxygen.nl/download.html