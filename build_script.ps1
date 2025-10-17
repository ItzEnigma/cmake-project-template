# CMake Build Script for PowerShell
# Usage: .\build.ps1 [prepare|build|run]

param(
    [string]$Action = "build"
)

# Set the executable name - you can modify this as needed
$EXECUTABLE_NAME = "MyApp.exe"  # or "executable.exe" based on your CMakeLists.txt

function Prepare {
    Write-Host "Preparing build environment..." -ForegroundColor Green
    
    # Remove existing build directory if it exists
    if (Test-Path "build") {
        Remove-Item -Recurse -Force "build"
        Write-Host "Removed existing build directory" -ForegroundColor Yellow
    }
    
    # Create new build directory
    New-Item -ItemType Directory -Name "build" | Out-Null
    Write-Host "Created build directory" -ForegroundColor Green
    
    # Navigate to build directory and run cmake
    Push-Location "build"
    try {
        Write-Host "Running cmake configuration..." -ForegroundColor Green
        cmake ..
        if ($LASTEXITCODE -ne 0) {
            throw "CMake configuration failed"
        }
    }
    finally {
        Pop-Location
    }
}

function Build {
    Write-Host "Building project..." -ForegroundColor Green
    
    if (-not (Test-Path "build")) {
        Write-Host "Build directory doesn't exist. Running prepare first..." -ForegroundColor Yellow
        Prepare
    }
    
    Push-Location "build"
    try {
        cmake --build . --config Release
        if ($LASTEXITCODE -ne 0) {
            throw "Build failed"
        }
        Write-Host "Build completed successfully!" -ForegroundColor Green
    }
    finally {
        Pop-Location
    }
}

function Run {
    Write-Host "Running executable..." -ForegroundColor Green
    
    $executablePath = ".\build\Debug\$EXECUTABLE_NAME"
    if (-not (Test-Path $executablePath)) {
        $executablePath = ".\build\Release\$EXECUTABLE_NAME"
    }
    
    if (-not (Test-Path $executablePath)) {
        Write-Host "Executable not found. Building first..." -ForegroundColor Yellow
        Build
        
        # Try again after building
        if (Test-Path ".\build\Debug\$EXECUTABLE_NAME") {
            $executablePath = ".\build\Debug\$EXECUTABLE_NAME"
        } elseif (Test-Path ".\build\Release\$EXECUTABLE_NAME") {
            $executablePath = ".\build\Release\$EXECUTABLE_NAME"
        } else {
            throw "Executable still not found after building"
        }
    }
    
    Write-Host "Executing: $executablePath" -ForegroundColor Green
    & $executablePath
}

function Coverage {
    Write-Host "Generating code coverage report..." -ForegroundColor Green
    
    if (-not (Test-Path "build")) {
        Write-Host "Build directory doesn't exist. Running prepare first..." -ForegroundColor Yellow
        Prepare
    }
    
    # Build with coverage enabled
    Push-Location "build"
    try {
        Write-Host "Configuring with coverage enabled..." -ForegroundColor Green
        cmake .. -DENABLE_COVERAGE=ON
        if ($LASTEXITCODE -ne 0) {
            throw "CMake configuration with coverage failed"
        }
        
        Write-Host "Building with coverage..." -ForegroundColor Green
        cmake --build . --config Debug
        if ($LASTEXITCODE -ne 0) {
            throw "Build with coverage failed"
        }
        
        Write-Host "Running coverage analysis..." -ForegroundColor Green
        cmake --build . --target coverage
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Coverage target failed, trying alternative..." -ForegroundColor Yellow
            # Try running tests manually for coverage
            ctest --output-on-failure
        }
        
        # Check if coverage report was generated
        if (Test-Path "coverage_html\index.html") {
            Write-Host "HTML coverage report generated at: build\coverage_html\index.html" -ForegroundColor Green
            Write-Host "Opening coverage report..." -ForegroundColor Green
            Start-Process "coverage_html\index.html"
        } elseif (Test-Path "coverage.xml") {
            Write-Host "XML coverage report generated at: build\coverage.xml" -ForegroundColor Green
        } else {
            Write-Host "Coverage report generation may have failed. Check build output." -ForegroundColor Yellow
        }
    }
    finally {
        Pop-Location
    }
}

function Test {
    Write-Host "Running tests..." -ForegroundColor Green
    
    if (-not (Test-Path "build")) {
        Write-Host "Build directory doesn't exist. Running prepare first..." -ForegroundColor Yellow
        Prepare
    }
    
    Push-Location "build"
    try {
        # Build tests
        cmake --build . --config Debug
        if ($LASTEXITCODE -ne 0) {
            throw "Test build failed"
        }
        
        # Run tests
        ctest --output-on-failure --build-config Debug
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Some tests failed!" -ForegroundColor Red
        } else {
            Write-Host "All tests passed!" -ForegroundColor Green
        }
    }
    finally {
        Pop-Location
    }
}

# Main script logic
try {
    switch ($Action.ToLower()) {
        "prepare" { Prepare }
        "build" { Build }
        "run" { Run }
        "test" { Test }
        "coverage" { Coverage }
        default {
            Write-Host "Usage: .\build_script.ps1 [prepare|build|run|test|coverage]" -ForegroundColor Yellow
            Write-Host "  prepare  - Clean and configure build environment"
            Write-Host "  build    - Build the project (default)"
            Write-Host "  run      - Run the executable"
            Write-Host "  test     - Run unit tests"
            Write-Host "  coverage - Generate code coverage report"
            exit 1
        }
    }
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}