# VirtualEndo Converter

A Blender add-on for converting Diagnocat STL files to various AR/VR formats.

## 🦷 Overview

VirtualEndo Converter is a specialized Blender add-on designed for dental professionals and endodontists. It automatically processes and converts Diagnocat STL files into various formats suitable for AR/VR applications, presentations, and 3D printing.

## ✨ Features

- **Automatic STL File Detection**: Recognizes pulp, tooth, and bone files by naming patterns
- **Smart Material Assignment**: Applies realistic materials with customizable colors and transparency
- **Multiple Export Formats**: 
  - USDZ (iOS AR compatible)
  - GLB (Universal 3D format)
  - FBX (Autodesk standard)
  - STL (3D printing)
- **Preset Color Schemes**: Clinical, Educational, and Presentation presets
- **Batch Processing**: Handles multiple files simultaneously
- **User-Friendly Interface**: Intuitive sidebar panel in Blender's 3D viewport

## ⚠️ **IMPORTANT DISCLAIMER**

**THIS IS NOT A MEDICAL DEVICE**

This software is intended for **educational, research, and presentation purposes only**. It is **NOT** suitable for:
- Patient diagnosis or treatment planning
- Clinical decision making
- Medical or therapeutic use with patient data
- Any medical procedures or patient care

Users must comply with all applicable medical data protection regulations (HIPAA, GDPR, etc.) when handling patient information.

## 📋 Requirements

- Blender 3.0 or higher
- **STL Import/Export add-on must be enabled** in Blender preferences
- Diagnocat STL files with proper naming convention:
  - `pulp_XX.stl` (pulp files)
  - `tooth_XX.stl` (tooth files)
  - `mandible.stl` / `maxilla.stl` (jaw bone files)

## 🚀 Installation

### Prerequisites
1. **Enable STL Import/Export in Blender**:
   - Open Blender
   - Go to `Edit` → `Preferences` → `Add-ons`
   - Search for "STL" 
   - Enable "Import-Export: STL format" add-on
   - Click "Save Preferences"

### Install VirtualEndo Converter
1. Download the latest `VirtualEndo_Converter.py` file from the [Releases](../../releases) page
2. In Blender, go to `Edit` → `Preferences` → `Add-ons`
3. Click `Install...` and select the downloaded `.py` file
4. Enable the add-on by checking the box next to "VirtualEndo Converter"
5. The add-on will automatically attempt to enable STL support if not already active

## 📖 Usage

1. **Open the VirtualEndo Panel**: 
   - In Blender's 3D viewport, open the sidebar (press `N`)
   - Find the "VirtualEndo" tab

2. **Select Input Folder**: 
   - Choose the folder containing your Diagnocat STL files

3. **Scan Files**: 
   - Click "Dateien scannen" to verify your files are detected

4. **Customize Settings**:
   - Adjust colors, transparency, and scaling as needed
   - Choose your preferred color preset

5. **Export**: 
   - Select your desired export format
   - Click the convert button

## 🎨 Color Presets

### Clinical (Default)
- **Pulp**: Clinical red for clear nerve identification
- **Teeth**: Clean clinical white
- **Bone**: Anatomical beige for realistic appearance

### Educational
- **High contrast colors** for teaching and presentations

### Presentation
- **Professional colors** optimized for client presentations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**DISCLAIMER**: This software is provided "as is" without warranty of any kind. The authors are not liable for any damages or issues arising from the use of this software. This tool is not intended for medical use or patient care.

## 🙏 Acknowledgments

- Designed for use with Diagnocat STL files
- Built for the dental and endodontic community
- Special thanks to the Blender development community

## 📞 Support

If you encounter any issues or have questions:
- Open an [issue](../../issues) on GitHub
- Provide sample files and error messages when possible

**Note**: This is community-supported software. For medical or clinical questions, please consult qualified healthcare professionals.

## 🔄 Version History

### v2.1.1 (Current)
- Fixed FBX export compatibility with Blender 3.0+
- Updated default clinical color scheme
- Improved error handling

### v2.1.0
- Initial public release
- Support for USDZ, GLB, FBX, and STL export formats
- Automatic material assignment and color presets

