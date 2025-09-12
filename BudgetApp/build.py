#!/usr/bin/env python3
"""
Build script for Budget App executables.
Creates standalone executables for Windows and macOS using PyInstaller.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


class BudgetAppBuilder:
    """Handles building Budget App executables for different platforms."""
    
    def __init__(self):
        self.app_name = "BudgetApp"
        self.version = "1.0.0"
        self.root_dir = Path.cwd()
        self.build_dir = self.root_dir / "build"
        self.dist_dir = self.root_dir / "dist"
        self.assets_dir = self.root_dir / "assets"
        
    def create_assets_directory(self):
        """Create assets directory with placeholder icons."""
        self.assets_dir.mkdir(exist_ok=True)
        
        # Create placeholder icon files (in real project, use actual icons)
        ico_path = self.assets_dir / "icon.ico"
        icns_path = self.assets_dir / "icon.icns"
        
        if not ico_path.exists():
            print("ℹ️  Creating placeholder Windows icon...")
            # Create a minimal ICO file (in production, use a real icon)
            ico_path.touch()
            
        if not icns_path.exists():
            print("ℹ️  Creating placeholder macOS icon...")
            # Create a minimal ICNS file (in production, use a real icon)
            icns_path.touch()
    
    def clean_build_dirs(self):
        """Clean previous build directories."""
        print("🧹 Cleaning previous builds...")
        
        dirs_to_clean = [self.build_dir, self.dist_dir]
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   Removed {dir_path}")
    
    def check_dependencies(self):
        """Check if required dependencies are installed."""
        print("🔍 Checking dependencies...")
        
        try:
            import PyInstaller
            print(f"   ✅ PyInstaller {PyInstaller.__version__}")
        except ImportError:
            print("   ❌ PyInstaller not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller==6.3.0"])
        
        try:
            import customtkinter
            print(f"   ✅ CustomTkinter {customtkinter.__version__}")
        except ImportError:
            print("   ❌ CustomTkinter not found. Please install requirements.txt")
            return False
        
        try:
            import bcrypt
            print(f"   ✅ bcrypt available")
        except ImportError:
            print("   ❌ bcrypt not found. Please install requirements.txt")
            return False
        
        return True
    
    def create_spec_file(self):
        """Create PyInstaller spec file."""
        print("📝 Creating PyInstaller spec file...")
        
        # Run the spec creation script
        exec(open("build_spec.py").read())
        
        if Path("BudgetApp.spec").exists():
            print("   ✅ Spec file created successfully")
            return True
        else:
            print("   ❌ Failed to create spec file")
            return False
    
    def build_executable(self):
        """Build the executable using PyInstaller."""
        print(f"🔨 Building executable for {platform.system()}...")
        
        try:
            # Run PyInstaller with the spec file
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--clean",
                "--noconfirm",
                "BudgetApp.spec"
            ]
            
            print(f"   Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   ✅ Build completed successfully")
                return True
            else:
                print("   ❌ Build failed:")
                print(f"   Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ❌ Build error: {e}")
            return False
    
    def verify_build(self):
        """Verify the built executable."""
        print("🔍 Verifying build...")
        
        if platform.system() == "Darwin":
            # macOS app bundle
            app_path = self.dist_dir / f"{self.app_name}.app"
            executable_path = app_path / "Contents" / "MacOS" / self.app_name
        else:
            # Windows executable
            executable_path = self.dist_dir / f"{self.app_name}.exe"
        
        if executable_path.exists():
            size_mb = executable_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ Executable created: {executable_path}")
            print(f"   📦 Size: {size_mb:.1f} MB")
            return True
        else:
            print(f"   ❌ Executable not found: {executable_path}")
            return False
    
    def create_distribution_package(self):
        """Create distribution package with additional files."""
        print("📦 Creating distribution package...")
        
        # Create distribution directory
        package_name = f"{self.app_name}-{self.version}-{platform.system().lower()}"
        package_dir = self.dist_dir / package_name
        package_dir.mkdir(exist_ok=True)
        
        # Copy executable/app bundle
        if platform.system() == "Darwin":
            app_bundle = self.dist_dir / f"{self.app_name}.app"
            if app_bundle.exists():
                shutil.copytree(app_bundle, package_dir / f"{self.app_name}.app")
        else:
            exe_file = self.dist_dir / f"{self.app_name}.exe"
            if exe_file.exists():
                shutil.copy2(exe_file, package_dir)
        
        # Copy additional files
        additional_files = ["README.md", "LICENSE"]
        for file_name in additional_files:
            file_path = self.root_dir / file_name
            if file_path.exists():
                shutil.copy2(file_path, package_dir)
        
        # Create installation instructions
        install_instructions = self.create_install_instructions()
        (package_dir / "INSTALL.txt").write_text(install_instructions)
        
        # Create ZIP package
        zip_path = self.dist_dir / f"{package_name}.zip"
        shutil.make_archive(str(zip_path.with_suffix('')), 'zip', self.dist_dir, package_name)
        
        print(f"   ✅ Distribution package: {zip_path}")
        return zip_path
    
    def create_install_instructions(self):
        """Create installation instructions for the platform."""
        system = platform.system()
        
        if system == "Darwin":
            return f"""Budget App {self.version} - macOS Installation
================================================

Installation:
1. Extract this ZIP file to your desired location
2. Move BudgetApp.app to your Applications folder (optional)
3. Double-click BudgetApp.app to run

Note: If you see a security warning, right-click the app and select "Open"
to bypass Gatekeeper on the first run.

System Requirements:
- macOS 10.14 or later
- 100MB free disk space

Support:
- GitHub: https://github.com/marcus-gray/BudgetApp
- Report issues via GitHub Issues

Built with PyInstaller on {platform.platform()}
"""
        else:
            return f"""Budget App {self.version} - Windows Installation
==================================================

Installation:
1. Extract this ZIP file to your desired location
2. Double-click BudgetApp.exe to run
3. (Optional) Create a desktop shortcut

Note: Windows may show a security warning for unsigned applications.
Click "More info" then "Run anyway" to proceed.

System Requirements:
- Windows 10 or later
- 100MB free disk space

Support:
- GitHub: https://github.com/marcus-gray/BudgetApp
- Report issues via GitHub Issues

Built with PyInstaller on {platform.platform()}
"""
    
    def build(self):
        """Main build process."""
        print(f"🚀 Building Budget App {self.version} for {platform.system()}")
        print("=" * 60)
        
        try:
            # Check dependencies
            if not self.check_dependencies():
                return False
            
            # Create assets
            self.create_assets_directory()
            
            # Clean previous builds
            self.clean_build_dirs()
            
            # Create spec file
            if not self.create_spec_file():
                return False
            
            # Build executable
            if not self.build_executable():
                return False
            
            # Verify build
            if not self.verify_build():
                return False
            
            # Create distribution package
            package_path = self.create_distribution_package()
            
            print("=" * 60)
            print("🎉 Build completed successfully!")
            print(f"📦 Distribution package: {package_path}")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ Build failed with error: {e}")
            return False


def main():
    """Main entry point."""
    builder = BudgetAppBuilder()
    
    # Check if we're in the right directory
    if not Path("src/main.py").exists():
        print("❌ Error: Please run this script from the project root directory")
        print("   (The directory containing src/main.py)")
        return 1
    
    # Build the application
    success = builder.build()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())