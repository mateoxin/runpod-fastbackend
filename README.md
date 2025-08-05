# Test Dataset Folder

## Structure
- `images/` - Training images (jpg, png)
- `captions/` - Caption files (txt)
- `config/` - Training configuration YAML files
- `models/` - Output trained models
- `logs/` - Training logs and outputs

## Usage
1. Place your training images in the `images/` folder
2. Add corresponding captions in the `captions/` folder
3. Configure training parameters in `config/`
4. Run tests with: `python run_all_tests.py`

## Supported Formats
- Images: .jpg, .jpeg, .png, .webp
- Captions: .txt, .caption
- Config: .yaml, .yml, .json
