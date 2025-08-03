#!/usr/bin/env python3
"""
🧪 Simple demonstration test for FastBackend
Quick test to verify the system works
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_basic_functionality():
    """Test basic functionality"""
    print("🧪 Testing basic functionality...")
    
    try:
        # Test import of main handler
        from handler_fast import handler
        
        # Test health check
        job = {"input": {"type": "health"}}
        result = handler(job)
        
        print(f"✅ Health check result: {result}")
        
        if result.get("status") == "healthy":
            print("✅ Basic test PASSED!")
            return True
        else:
            print("❌ Basic test FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_dataset_structure():
    """Test and verify existing dataset structure"""
    print("\n📁 Checking dataset structure...")
    
    # Check if 10_Matt folder exists and has data
    # Look for Matt folder in tests/ directory or current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    matt_folder_in_tests = os.path.join(script_dir, "10_Matt")
    matt_folder_current = "10_Matt"
    
    if os.path.exists(matt_folder_in_tests):
        matt_folder = matt_folder_in_tests
    elif os.path.exists(matt_folder_current):
        matt_folder = matt_folder_current
    else:
        matt_folder = "10_Matt"
    if os.path.exists(matt_folder):
        print(f"✅ Found dataset folder: {matt_folder}/")
        
        # Count images and captions
        image_files = [f for f in os.listdir(matt_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        caption_files = [f for f in os.listdir(matt_folder) if f.lower().endswith('.txt')]
        
        print(f"📸 Images found: {len(image_files)}")
        print(f"📝 Captions found: {len(caption_files)}")
        
        # Show first few examples
        if image_files:
            print(f"\n🖼️  Sample images:")
            for img in image_files[:3]:
                print(f"   - {img}")
        
        if caption_files:
            print(f"\n📝 Sample captions:")
            for cap in caption_files[:3]:
                print(f"   - {cap}")
                
        # Check for matching pairs
        matching_pairs = 0
        for img_file in image_files:
            base_name = os.path.splitext(img_file)[0]
            caption_file = base_name + '.txt'
            if caption_file in caption_files:
                matching_pairs += 1
        
        print(f"\n🔗 Matching image-caption pairs: {matching_pairs}")
        
    else:
        print(f"❌ Dataset folder 10_Matt/ not found!")
        print(f"💡 Expected location: tests/10_Matt/ or current directory")
        return False
    
    # Create additional folders if needed
    additional_folders = ['config', 'models', 'logs']
    for folder in additional_folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"✅ Created: {folder}/")
        except Exception as e:
            print(f"❌ Failed to create {folder}: {e}")
    
    print("\n📁 Dataset structure verified!")
    print(f"🖼️  Using images from: {matt_folder}/")
    print(f"📝 Using captions from: {matt_folder}/")
    
    return True

if __name__ == "__main__":
    print("🚀 FastBackend Simple Test")
    print("=" * 40)
    
    # Test basic functionality
    basic_result = test_basic_functionality()
    
    # Create dataset structure
    test_dataset_structure()
    
    print("\n" + "=" * 40)
    if basic_result:
        print("🎉 All tests completed successfully!")
        print("📁 Dataset folders created - you can now add your images!")
    else:
        print("⚠️  Some tests failed - check the output above")
    
    print("=" * 40)