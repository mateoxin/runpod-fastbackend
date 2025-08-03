#!/usr/bin/env python3
"""
🚀 Master test runner for all FastBackend tests
Runs all test suites and generates comprehensive report
"""

import sys
import os
import unittest
import time
import json
from datetime import datetime
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def discover_and_run_tests():
    """Discover and run all tests in the tests directory"""
    
    print("🔍 Discovering test modules...")
    
    # Test modules to run in order
    test_modules = [
        'test_handler_methods',
        'test_deployment_methods', 
        'test_local_testing',
        'test_with_matt_dataset',  # Add Matt dataset tests
        'test_all_integration'
    ]
    
    all_results = []
    total_start_time = time.time()
    
    for module_name in test_modules:
        print(f"\n{'='*60}")
        print(f"🧪 Running {module_name}")
        print(f"{'='*60}")
        
        module_start_time = time.time()
        
        try:
            # Import the test module
            test_module = __import__(module_name)
            
            # Create test suite for this module
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(test_module)
            
            # Run tests with captured output
            stream = StringIO()
            runner = unittest.TextTestRunner(stream=stream, verbosity=2)
            result = runner.run(suite)
            
            module_end_time = time.time()
            module_duration = module_end_time - module_start_time
            
            # Store results
            module_result = {
                'module': module_name,
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'success': result.wasSuccessful(),
                'duration': module_duration,
                'output': stream.getvalue()
            }
            
            all_results.append(module_result)
            
            # Print module summary
            status = "✅ PASSED" if result.wasSuccessful() else "❌ FAILED"
            print(f"\n📊 {module_name} Summary:")
            print(f"   Status: {status}")
            print(f"   Tests: {result.testsRun}")
            print(f"   Failures: {len(result.failures)}")
            print(f"   Errors: {len(result.errors)}")
            print(f"   Duration: {module_duration:.2f}s")
            
            if result.failures:
                print(f"\n❌ Failures in {module_name}:")
                for test, traceback in result.failures:
                    print(f"   - {test}")
            
            if result.errors:
                print(f"\n💥 Errors in {module_name}:")
                for test, traceback in result.errors:
                    print(f"   - {test}")
                    
        except Exception as e:
            print(f"❌ Failed to run {module_name}: {e}")
            all_results.append({
                'module': module_name,
                'tests_run': 0,
                'failures': 0,
                'errors': 1,
                'success': False,
                'duration': 0,
                'error': str(e)
            })
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    return all_results, total_duration

def generate_test_report(results, total_duration):
    """Generate comprehensive test report"""
    
    timestamp = datetime.now().isoformat()
    
    # Calculate totals
    total_tests = sum(r['tests_run'] for r in results)
    total_failures = sum(r['failures'] for r in results)
    total_errors = sum(r['errors'] for r in results)
    successful_modules = sum(1 for r in results if r['success'])
    total_modules = len(results)
    
    overall_success = total_failures == 0 and total_errors == 0
    
    # Create report
    report = {
        'timestamp': timestamp,
        'summary': {
            'overall_success': overall_success,
            'total_modules': total_modules,
            'successful_modules': successful_modules,
            'total_tests': total_tests,
            'total_failures': total_failures,
            'total_errors': total_errors,
            'total_duration': total_duration
        },
        'modules': results,
        'environment': {
            'python_version': sys.version,
            'platform': sys.platform,
            'working_directory': os.getcwd()
        }
    }
    
    # Save report to file
    report_filename = f"test_report_all_{int(time.time())}.json"
    try:
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📄 Full report saved: {report_filename}")
    except Exception as e:
        print(f"⚠️ Could not save report: {e}")
    
    return report

def print_final_summary(report):
    """Print final test summary"""
    
    summary = report['summary']
    
    print(f"\n{'='*60}")
    print(f"🏁 FINAL TEST SUMMARY")
    print(f"{'='*60}")
    
    print(f"⏱️  Total Duration: {summary['total_duration']:.2f} seconds")
    print(f"📦 Modules Tested: {summary['successful_modules']}/{summary['total_modules']}")
    print(f"🧪 Total Tests: {summary['total_tests']}")
    print(f"✅ Passed: {summary['total_tests'] - summary['total_failures'] - summary['total_errors']}")
    print(f"❌ Failed: {summary['total_failures']}")
    print(f"💥 Errors: {summary['total_errors']}")
    
    if summary['overall_success']:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"✅ FastBackend is ready for deployment!")
        print(f"🚀 All components are working correctly!")
    else:
        print(f"\n⚠️  SOME TESTS FAILED")
        print(f"🔧 Please review and fix issues before deployment")
        
        # Show failed modules
        failed_modules = [r for r in report['modules'] if not r['success']]
        if failed_modules:
            print(f"\n❌ Failed modules:")
            for module in failed_modules:
                print(f"   - {module['module']}: {module['failures']} failures, {module['errors']} errors")
    
    print(f"\n{'='*60}")

def create_test_dataset_structure():
    """Create placeholder structure for test dataset"""
    
    print("\n📁 Creating test dataset structure...")
    
    dataset_structure = {
        "images/": "Place your training images here",
        "captions/": "Place corresponding caption files here", 
        "config/": "Place training configuration files here",
        "models/": "Trained models will be saved here",
        "logs/": "Training logs and outputs",
        "README.md": """# Test Dataset Folder

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
"""
    }
    
    # Create directories
    for folder_name, description in dataset_structure.items():
        if folder_name.endswith('/'):
            folder_path = folder_name.rstrip('/')
            os.makedirs(folder_path, exist_ok=True)
            print(f"✅ Created: {folder_path}/")
            
            # Create .gitkeep to ensure folder is tracked
            gitkeep_path = os.path.join(folder_path, '.gitkeep')
            with open(gitkeep_path, 'w') as f:
                f.write(f"# {description}\n")
        else:
            # Create README.md
            with open(folder_name, 'w') as f:
                f.write(description)
            print(f"✅ Created: {folder_name}")
    
    print("📁 Test dataset structure created!")

def main():
    """Main test runner"""
    
    print("🚀 FastBackend - Master Test Runner")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Create test dataset structure
    create_test_dataset_structure()
    
    # Run all tests
    print("\n🧪 Running comprehensive test suite...")
    results, total_duration = discover_and_run_tests()
    
    # Generate report
    print(f"\n📊 Generating test report...")
    report = generate_test_report(results, total_duration)
    
    # Print final summary
    print_final_summary(report)
    
    # Return appropriate exit code
    return 0 if report['summary']['overall_success'] else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)