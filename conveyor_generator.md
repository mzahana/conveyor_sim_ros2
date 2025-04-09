

# Conveyor Belt Model Generator

This Python script generates a Gazebo model of a conveyor belt with customizable dimensions and material properties. You can specify options such as the belt’s length, width, thickness, height of the legs, and custom material textures for the belt, rollers, and legs. Additionally, the script supports both standard and Physically-Based Rendering (PBR) material setups using texture maps for albedo, metalness, roughness, and normal maps.

![custom conveyor](resource/conveyor.png)
## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Command-Line Arguments](#command-line-arguments)
- [Examples](#examples)
- [Output Files](#output-files)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- **Customizable Dimensions:** Set the length, width, thickness, and leg height of the conveyor belt.
- **Material Customization:**  
  - Option to use custom textures.
  - PBR material support with texture maps for albedo, normal, metalness, and roughness.
  - Separate textures for the belt, rollers, and legs.
- **Automatic File Generation:**  
  - Creates the necessary directory structure.
  - Generates a `model.config` file.
  - Generates the `model.sdf` file with properly formatted XML.
  - Copies provided texture files into the model’s materials folder.
- **Plugin Integration:** Includes Gazebo plugins for conveyor belt functionality and key-triggered commands for moving the belt (e.g., forward, backward, and stop).

## Requirements

- **Python 3.x**
- Standard Python modules: `os`, `sys`, `argparse`, `math`, `shutil`, `xml.dom.minidom`, and `xml.etree.ElementTree`.

## Installation

1. Ensure that Python 3 is installed on your system.
2. Download or clone this repository.
3. Make sure the script (`conveyor_generator.py`) has execute permissions. You can set the permission using:
   ```bash
   chmod +x conveyor_generator.py
   ```

## Usage

The script can be run directly from the command line. It uses a set of command-line arguments to configure the model and material properties.

### Basic Syntax

```bash
python conveyor_generator.py [options]
```

### Command-Line Arguments

#### Basic Model Parameters

- `--length`  
  *Type:* `float`  
  *Default:* `5.0`  
  *Description:* Length of the conveyor belt in meters.

- `--width`  
  *Type:* `float`  
  *Default:* `1.0`  
  *Description:* Width of the conveyor belt in meters.

- `--thickness`  
  *Type:* `float`  
  *Default:* `0.1`  
  *Description:* Thickness of the conveyor belt in meters.

- `--height`  
  *Type:* `float`  
  *Default:* `0.5`  
  *Description:* Height of the legs supporting the conveyor belt in meters.

- `--model-name`  
  *Type:* `str`  
  *Default:* `conveyor`  
  *Description:* The name assigned to the generated model.

#### Material Options

- `--use-custom-materials`  
  *Type:* `flag`  
  *Description:* Enables the use of custom texture materials for the model. If not specified, default material colors are applied.

- `--use-pbr-materials`  
  *Type:* `flag`  
  *Description:* Activates Physically-Based Rendering (PBR) materials. This option is effective only when `--use-custom-materials` is also set.

#### Texture File Paths

**For the Belt:**
- `--belt-texture`  
  *Description:* Path to the belt’s albedo texture (PNG file).

- `--belt-normal`  
  *Description:* Path to the belt’s normal map (PNG file).

- `--belt-metalness`  
  *Description:* Path to the belt’s metalness map (PNG file).

- `--belt-roughness`  
  *Description:* Path to the belt’s roughness map (PNG file).

**For the Rollers:**
- `--roller-texture`  
  *Description:* Path to the roller’s albedo texture (PNG file).

- `--roller-metalness`  
  *Description:* Path to the roller’s metalness map (PNG file).  
  *Usage:* If provided, this texture is used for the roller metalness; otherwise, a default value of `0.9` is used.

- `--roller-roughness`  
  *Description:* Path to the roller’s roughness map (PNG file).  
  *Usage:* If provided, this texture is used for the roller roughness; otherwise, a default value of `0.1` is used.

**For the Legs:**
- `--leg-texture`  
  *Description:* Path to the leg’s albedo texture (PNG file).

- `--leg-metalness`  
  *Description:* Path to the leg’s metalness map (PNG file).  
  *Usage:* If provided, this texture is used for the leg metalness; otherwise, a default value of `0.9` is used.

- `--leg-roughness`  
  *Description:* Path to the leg’s roughness map (PNG file).  
  *Usage:* If provided, this texture is used for the leg roughness; otherwise, a default value of `0.2` is used.

## Examples

### Example 1: Basic Model with Default Materials

```bash
python conveyor_generator.py --model-name my_conveyor
```

This command creates a conveyor belt model named `my_conveyor` in the directory `my_conveyor` using default material colors.

### Example 2: Model with Custom PBR Materials for Belt Only

```bash
python conveyor_generator.py --model-name custom_conveyor  \
--use-custom-materials --use-pbr-materials \
--belt-texture textures/Leather032_1K_Color.png \
--belt-normal textures/Leather032_1K_Normal.png \
--belt-metalness textures/Leather032_1K_Metalness.png \
--belt-roughness textures/Leather032_1K_Roughness.png
```

This command creates a model with custom PBR materials for the belt by copying the provided texture files. The rollers and legs will use default material settings.

### Example 3: Model with Custom Materials for All Components

```bash
python conveyor_generator.py --model-name full_custom_conveyor \
--use-custom-materials --use-pbr-materials \
--belt-texture textures/Belt_Albedo.png \
--belt-normal textures/Belt_Normal.png \
--belt-metalness textures/Belt_Metalness.png \
--belt-roughness textures/Belt_Roughness.png \
--roller-texture textures/Roller_Albedo.png \
--roller-metalness textures/Roller_Metalness.png \
--roller-roughness textures/Roller_Roughness.png \
--leg-texture textures/Leg_Albedo.png \
--leg-metalness textures/Leg_Metalness.png \
--leg-roughness textures/Leg_Roughness.png
```

This example sets custom textures for the belt, rollers, and legs. If any of the optional metalness or roughness texture files for rollers or legs are not provided, the script will use its default values.

## Output Files

After running the script, the following will be generated in the specified directory (directory name is the same as the model name):

- **Model Configuration:**
  - `model.config` — Contains model metadata such as the model name, version, and description.

- **SDF File:**
  - `model.sdf` — Defines the model’s geometry, collision, visual elements, material properties, and plugin configurations for Gazebo.

- **Materials Directory:**
  - `materials/` — Contains the following:
    - `textures/` — All provided texture files are copied here.
    - `scripts/` — Contains a material script (`model.material`) that defines the custom materials for the belt, rollers, and legs.

## Troubleshooting

- **Texture File Not Found:**  
  If a specified texture file path is incorrect or the file does not exist, the script prints a warning and uses default colors or default numeric values.
  
- **Directory Issues:**  
  Ensure that the target directory is writeable and the script has the necessary permissions to create subdirectories and files.

- **PBR Options:**  
  The PBR options (`--use-pbr-materials`) are only active if `--use-custom-materials` is specified. Make sure to include both flags if you want to use texture maps.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


---
