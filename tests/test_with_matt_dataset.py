#!/usr/bin/env python3
"""
🧪 Test FastBackend with real Matt dataset
Test using actual images and captions from 10_Matt folder
"""

import sys
import os
import json
import base64
import glob
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_matt_dataset():
    """Load real Matt dataset from 10_Matt folder"""
    print("📂 Loading Matt dataset...")
    
    # Look for Matt folder in tests/ directory or current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    matt_folder_in_tests = os.path.join(script_dir, "10_Matt")
    matt_folder_current = "10_Matt"
    
    if os.path.exists(matt_folder_in_tests):
        matt_folder = matt_folder_in_tests
    elif os.path.exists(matt_folder_current):
        matt_folder = matt_folder_current
    else:
        print(f"❌ Matt dataset folder not found: 10_Matt")
        print(f"💡 Expected location: tests/10_Matt/ or current directory")
        return None
    
    # Find all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(matt_folder, ext)))
        # Also check uppercase
        image_files.extend(glob.glob(os.path.join(matt_folder, ext.upper())))
    
    print(f"📸 Found {len(image_files)} images")
    
    dataset = []
    
    for image_path in image_files[:5]:  # Limit to first 5 for testing
        try:
            # Get base filename without extension
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            caption_path = os.path.join(matt_folder, base_name + '.txt')
            
            # Read image file
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Encode image to base64
            image_b64 = base64.b64encode(image_data).decode('utf-8')
            
            # Read caption if exists
            caption = ""
            if os.path.exists(caption_path):
                with open(caption_path, 'r', encoding='utf-8') as f:
                    caption = f.read().strip()
            
            dataset.append({
                'filename': os.path.basename(image_path),
                'content': image_b64,
                'caption': caption,
                'size': len(image_data)
            })
            
            print(f"✅ Loaded: {os.path.basename(image_path)} ({len(image_data)} bytes)")
            if caption:
                print(f"   📝 Caption: {caption[:100]}...")
                
        except Exception as e:
            print(f"❌ Failed to load {image_path}: {e}")
    
    print(f"\n📦 Dataset ready: {len(dataset)} files loaded")
    return dataset

def test_upload_matt_dataset():
    """Test uploading Matt dataset"""
    print("\n🧪 Testing upload with Matt dataset...")
    
    try:
        from handler_fast import handler
        
        # Load dataset
        dataset = load_matt_dataset()
        if not dataset:
            return False
        
        # Prepare upload job
        upload_job = {
            "input": {
                "type": "upload_training_data",
                "files": dataset,
                "training_name": "matt_training_test"
            }
        }
        
        print(f"📤 Uploading {len(dataset)} files...")
        
        # Mock the heavy modules and environment
        import unittest.mock as mock
        with mock.patch('handler_fast.setup_environment', return_value=True):
            with mock.patch('handler_fast.lazy_import_heavy_modules', return_value={'base64': base64}):
                with mock.patch('os.makedirs'):
                    with mock.patch('builtins.open', mock.mock_open()) as mock_file:
                        
                        result = handler(upload_job)
                        
                        print(f"📊 Upload result: {result}")
                        
                        if result.get("status") == "success":
                            print("✅ Matt dataset upload test PASSED!")
                            return True
                        else:
                            print("❌ Matt dataset upload test FAILED!")
                            return False
                            
    except Exception as e:
        print(f"❌ Upload test error: {e}")
        return False

def test_training_with_matt_config():
    """Test training configuration with Matt dataset"""
    print("\n🧪 Testing training config for Matt dataset...")
    
    try:
        from handler_fast import handler
        
        # Create training config for Matt
        matt_config = f"""
# Matt LoRA Training Config
job: extension
config:
  name: "matt_lora_v1"
  process:
    - type: sd_trainer
      training_folder: "/workspace/training_data/matt_training_test"
      device: cuda:0
      trigger_word: "Matt"
      
  model:
    name_or_path: "runwayml/stable-diffusion-v1-5"
    is_v2: false
    is_v_pred: false
    is_xl: false
    
  save:
    dtype: float16
    save_every: 250
    max_step_saves_to_keep: 3
    
  datasets:
  - folder_path: "/workspace/training_data/matt_training_test"
    caption_ext: "txt"
    caption_dropout_rate: 0.05
    shuffle_tokens: false
    cache_latents_to_disk: true
    resolution: 512
    
  train:
    batch_size: 1
    steps: 1000
    gradient_accumulation_steps: 4
    train_unet: true
    train_text_encoder: false
    gradient_checkpointing: true
    noise_scheduler: "ddim"
    optimizer: "adamw8bit"
    lr: 4e-4
    
  sample:
    sampler: "ddim"
    sample_every: 250
    width: 512
    height: 512
    prompts:
    - "Matt, a man at the beach, high quality, detailed"
    - "Matt, a man in casual clothes, portrait, professional photo"
    - "Matt, a man wearing a leather jacket, urban style"
    neg: "blurry, low quality, distorted"
"""
        
        training_job = {
            "input": {
                "type": "train_with_yaml",
                "yaml_config": matt_config
            }
        }
        
        print("🎯 Testing training configuration...")
        
        # Mock the required modules
        import unittest.mock as mock
        import yaml
        import uuid
        
        mock_uuid = mock.Mock()
        mock_uuid.uuid4.return_value = mock.Mock()
        mock_uuid.uuid4.return_value.__str__ = lambda: "matt-training-12345"
        
        with mock.patch('handler_fast.setup_environment', return_value=True):
            with mock.patch('handler_fast.lazy_import_heavy_modules', return_value={'yaml': yaml, 'uuid': mock_uuid}):
                with mock.patch('builtins.open', mock.mock_open()):
                    
                    result = handler(training_job)
                    
                    print(f"📊 Training config result: {result}")
                    
                    if result.get("status") == "success":
                        print("✅ Matt training config test PASSED!")
                        return True
                    else:
                        print("❌ Matt training config test FAILED!")
                        return False
                        
    except Exception as e:
        print(f"❌ Training config test error: {e}")
        return False

def test_matt_dataset_analysis():
    """Analyze Matt dataset for training insights"""
    print("\n📊 Analyzing Matt dataset...")
    
    try:
        dataset = load_matt_dataset()
        if not dataset:
            return False
        
        print(f"\n📈 Dataset Analysis:")
        print(f"   📸 Total images: {len(dataset)}")
        
        # Analyze file sizes
        sizes = [item['size'] for item in dataset]
        avg_size = sum(sizes) / len(sizes) if sizes else 0
        min_size = min(sizes) if sizes else 0
        max_size = max(sizes) if sizes else 0
        
        print(f"   📏 Average file size: {avg_size/1024:.1f} KB")
        print(f"   📏 Size range: {min_size/1024:.1f} - {max_size/1024:.1f} KB")
        
        # Analyze captions
        captions = [item['caption'] for item in dataset if item['caption']]
        caption_count = len(captions)
        
        print(f"   📝 Images with captions: {caption_count}/{len(dataset)}")
        
        if captions:
            avg_caption_length = sum(len(cap) for cap in captions) / len(captions)
            print(f"   📝 Average caption length: {avg_caption_length:.1f} characters")
            
            # Show common words
            all_words = []
            for caption in captions:
                all_words.extend(caption.lower().split())
            
            word_count = {}
            for word in all_words:
                word_count[word] = word_count.get(word, 0) + 1
            
            common_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]
            print(f"   🔤 Most common words: {', '.join([f'{word}({count})' for word, count in common_words[:5]])}")
        
        # File format analysis
        formats = {}
        for item in dataset:
            ext = os.path.splitext(item['filename'])[1].lower()
            formats[ext] = formats.get(ext, 0) + 1
        
        print(f"   📋 File formats: {dict(formats)}")
        
        print("\n✅ Dataset analysis complete!")
        return True
        
    except Exception as e:
        print(f"❌ Dataset analysis error: {e}")
        return False

def run_matt_tests():
    """Run all tests with Matt dataset"""
    print("🚀 FastBackend Tests with Matt Dataset")
    print("=" * 50)
    
    tests = [
        ("Dataset Analysis", test_matt_dataset_analysis),
        ("Upload Test", test_upload_matt_dataset),
        ("Training Config", test_training_with_matt_config)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 Running: {test_name}")
        print(f"{'='*50}")
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"\n📊 {test_name}: {status}")
            
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
            results.append((test_name, False))
    
    # Final summary
    print(f"\n{'='*50}")
    print("🏁 MATT DATASET TEST SUMMARY")
    print(f"{'='*50}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"📊 Tests: {passed}/{total} passed")
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"   {status} {test_name}")
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"✅ Matt dataset is ready for training!")
    else:
        print(f"\n⚠️  Some tests failed")
        print(f"🔧 Check the output above for details")
    
    return passed == total

if __name__ == "__main__":
    success = run_matt_tests()
    sys.exit(0 if success else 1)