#!/usr/bin/env python3
"""
🧪 Comprehensive tests for handler_fast.py methods
Test all functions and scenarios in the FastBackend handler
"""

import sys
import os
import json
import unittest
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add parent directory to path for importing handler
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestHandlerMethods(unittest.TestCase):
    """Test all methods in handler_fast.py"""
    
    def setUp(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp()
        os.environ['TEST_MODE'] = 'true'
        
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
    def test_setup_environment_success(self):
        """Test successful environment setup"""
        from handler_fast import setup_environment, ENVIRONMENT_READY
        
        with patch('subprocess.run') as mock_run:
            # Mock successful subprocess calls
            mock_run.return_value.returncode = 0
            mock_run.return_value.stderr = ""
            
            with patch('os.path.exists', return_value=False):
                result = setup_environment()
                
            self.assertTrue(result)
            # Check that subprocess was called for installations
            self.assertTrue(mock_run.called)
    
    def test_setup_environment_failure(self):
        """Test environment setup failure scenarios"""
        from handler_fast import setup_environment
        
        with patch('subprocess.run') as mock_run:
            # Mock failed PyTorch installation
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "Installation failed"
            
            result = setup_environment()
            self.assertFalse(result)
    
    def test_lazy_import_heavy_modules_success(self):
        """Test successful lazy import of modules"""
        from handler_fast import lazy_import_heavy_modules
        
        modules = lazy_import_heavy_modules()
        
        # Check that expected modules are imported
        expected_modules = ['base64', 'uuid', 'yaml', 'threading', 'shutil', 'glob', 'Image', 'io']
        
        if modules:  # Only test if import was successful
            for module_name in expected_modules:
                self.assertIn(module_name, modules)
    
    def test_lazy_import_heavy_modules_failure(self):
        """Test lazy import failure handling"""
        from handler_fast import lazy_import_heavy_modules
        
        with patch('builtins.__import__', side_effect=ImportError("Mock import error")):
            modules = lazy_import_heavy_modules()
            self.assertIsNone(modules)
    
    def test_handler_health_check(self):
        """Test health check endpoint"""
        from handler_fast import handler
        
        job = {"input": {"type": "health"}}
        result = handler(job)
        
        self.assertEqual(result["status"], "healthy")
        self.assertIn("timestamp", result)
        self.assertIn("environment_ready", result)
        self.assertEqual(result["version"], "1.0.0-fast")
    
    def test_handler_ping(self):
        """Test ping endpoint"""
        from handler_fast import handler
        
        job = {"input": {"type": "ping"}}
        result = handler(job)
        
        self.assertEqual(result["status"], "pong")
        self.assertIn("timestamp", result)
        self.assertIn("setup_required", result)
    
    def test_handler_echo(self):
        """Test echo endpoint"""
        from handler_fast import handler
        
        test_message = "Hello FastBackend Test!"
        job = {"input": {"type": "echo", "message": test_message}}
        result = handler(job)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("echo", result)
        self.assertEqual(result["echo"]["message"], test_message)
    
    def test_handler_setup_environment(self):
        """Test manual environment setup trigger"""
        from handler_fast import handler
        
        with patch('handler_fast.setup_environment', return_value=True):
            job = {"input": {"type": "setup_environment"}}
            result = handler(job)
            
            self.assertEqual(result["status"], "success")
            self.assertIn("environment_ready", result)
    
    def test_handler_unknown_type(self):
        """Test unknown job type handling"""
        from handler_fast import handler
        
        job = {"input": {"type": "unknown_test_type"}}
        result = handler(job)
        
        self.assertEqual(result["status"], "unknown_type")
        self.assertIn("available_types", result)
        self.assertIn("received_type", result)
    
    def test_handler_heavy_operation_without_setup(self):
        """Test heavy operation triggering environment setup"""
        from handler_fast import handler
        
        with patch('handler_fast.setup_environment', return_value=True) as mock_setup:
            with patch('handler_fast.lazy_import_heavy_modules', return_value={'base64': Mock()}):
                with patch('handler_fast.handle_heavy_operation', return_value={"status": "success"}):
                    job = {"input": {"type": "upload_training_data", "files": []}}
                    result = handler(job)
                    
                    # Should trigger setup
                    mock_setup.assert_called_once()
    
    def test_handler_error_handling(self):
        """Test error handling in main handler"""
        from handler_fast import handler
        
        # Test with invalid job format
        result = handler({})
        self.assertEqual(result["status"], "unknown_type")
        
        # Test with malformed input
        result = handler({"invalid": "format"})
        self.assertEqual(result["status"], "unknown_type")
    
    def test_handle_upload_training_data_success(self):
        """Test successful training data upload"""
        from handler_fast import handle_upload_training_data
        import base64
        
        # Mock modules
        modules = {
            'base64': base64,
            'uuid': Mock()
        }
        
        # Test data
        test_content = b"test file content"
        encoded_content = base64.b64encode(test_content).decode()
        
        job_input = {
            "files": [
                {
                    "filename": "test.txt",
                    "content": encoded_content
                }
            ],
            "training_name": "test_training"
        }
        
        with patch('os.makedirs'):
            with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
                result = handle_upload_training_data(job_input, modules)
                
                self.assertEqual(result["status"], "success")
                self.assertIn("uploaded_files", result)
                self.assertEqual(len(result["uploaded_files"]), 1)
    
    def test_handle_upload_training_data_no_files(self):
        """Test upload with no files provided"""
        from handler_fast import handle_upload_training_data
        
        modules = {'base64': Mock()}
        job_input = {"files": []}
        
        result = handle_upload_training_data(job_input, modules)
        self.assertEqual(result["status"], "error")
        self.assertIn("No files provided", result["error"])
    
    def test_handle_train_with_yaml_success(self):
        """Test successful YAML training configuration"""
        from handler_fast import handle_train_with_yaml
        import yaml
        import uuid
        
        modules = {
            'yaml': yaml,
            'uuid': uuid
        }
        
        test_config = {
            "model": "test_model",
            "training": {
                "epochs": 10,
                "batch_size": 4
            }
        }
        
        job_input = {
            "yaml_config": yaml.dump(test_config)
        }
        
        with patch('builtins.open', unittest.mock.mock_open()):
            result = handle_train_with_yaml(job_input, modules)
            
            self.assertEqual(result["status"], "success")
            self.assertIn("process_id", result)
            self.assertIn("config_path", result)
    
    def test_handle_train_with_yaml_missing_config(self):
        """Test training without YAML config"""
        from handler_fast import handle_train_with_yaml
        
        modules = {'yaml': Mock()}
        job_input = {}
        
        result = handle_train_with_yaml(job_input, modules)
        self.assertEqual(result["status"], "error")
        self.assertIn("Missing yaml_config", result["error"])
    
    def test_handle_list_models_success(self):
        """Test successful model listing"""
        from handler_fast import handle_list_models
        
        modules = {}
        
        # Mock os.path.exists and os.walk
        with patch('os.path.exists', return_value=True):
            with patch('os.walk') as mock_walk:
                mock_walk.return_value = [
                    ('/workspace/ai-toolkit/output', [], ['model1.safetensors', 'model2.safetensors'])
                ]
                
                with patch('os.path.getsize', return_value=1024):
                    with patch('os.path.getmtime', return_value=1234567890):
                        result = handle_list_models(modules)
                        
                        self.assertEqual(result["status"], "success")
                        self.assertIn("models", result)
                        self.assertEqual(len(result["models"]), 2)
                        self.assertEqual(result["total_count"], 2)
    
    def test_handle_list_models_no_directory(self):
        """Test model listing when output directory doesn't exist"""
        from handler_fast import handle_list_models
        
        modules = {}
        
        with patch('os.path.exists', return_value=False):
            result = handle_list_models(modules)
            
            self.assertEqual(result["status"], "success")
            self.assertEqual(len(result["models"]), 0)
            self.assertEqual(result["total_count"], 0)
    
    def test_handle_heavy_operation_routing(self):
        """Test heavy operation routing to correct handlers"""
        from handler_fast import handle_heavy_operation
        
        modules = {'base64': Mock(), 'uuid': Mock(), 'yaml': Mock()}
        
        # Test upload_training_data routing
        with patch('handler_fast.handle_upload_training_data', return_value={"status": "success"}) as mock_upload:
            result = handle_heavy_operation("upload_training_data", {}, modules)
            mock_upload.assert_called_once()
            self.assertEqual(result["status"], "success")
        
        # Test train_with_yaml routing
        with patch('handler_fast.handle_train_with_yaml', return_value={"status": "success"}) as mock_train:
            result = handle_heavy_operation("train_with_yaml", {}, modules)
            mock_train.assert_called_once()
            self.assertEqual(result["status"], "success")
        
        # Test list_models routing
        with patch('handler_fast.handle_list_models', return_value={"status": "success"}) as mock_list:
            result = handle_heavy_operation("list_models", {}, modules)
            mock_list.assert_called_once()
            self.assertEqual(result["status"], "success")
    
    def test_handle_heavy_operation_unknown(self):
        """Test handling of unknown heavy operations"""
        from handler_fast import handle_heavy_operation
        
        modules = {}
        result = handle_heavy_operation("unknown_heavy_op", {}, modules)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("simplified", result["message"])
    
    def test_handle_heavy_operation_error(self):
        """Test error handling in heavy operations"""
        from handler_fast import handle_heavy_operation
        
        modules = {}
        
        with patch('handler_fast.handle_upload_training_data', side_effect=Exception("Test error")):
            result = handle_heavy_operation("upload_training_data", {}, modules)
            
            self.assertEqual(result["status"], "error")
            self.assertIn("Heavy operation error", result["error"])


class TestHandlerIntegration(unittest.TestCase):
    """Integration tests for complete handler workflows"""
    
    def test_complete_upload_workflow(self):
        """Test complete file upload workflow"""
        from handler_fast import handler
        import base64
        
        # Prepare test data
        test_content = b"mock training image data"
        encoded_content = base64.b64encode(test_content).decode()
        
        job = {
            "input": {
                "type": "upload_training_data",
                "files": [
                    {
                        "filename": "training_image.jpg",
                        "content": encoded_content
                    }
                ],
                "training_name": "integration_test"
            }
        }
        
        with patch('handler_fast.setup_environment', return_value=True):
            with patch('handler_fast.lazy_import_heavy_modules', return_value={'base64': base64}):
                with patch('os.makedirs'):
                    with patch('builtins.open', unittest.mock.mock_open()):
                        result = handler(job)
                        
                        # Should successfully process upload
                        self.assertEqual(result["status"], "success")
                        self.assertIn("uploaded_files", result)
    
    def test_health_to_training_workflow(self):
        """Test workflow from health check to training"""
        from handler_fast import handler
        
        # First check health
        health_job = {"input": {"type": "health"}}
        health_result = handler(health_job)
        self.assertEqual(health_result["status"], "healthy")
        
        # Then setup environment
        setup_job = {"input": {"type": "setup_environment"}}
        with patch('handler_fast.setup_environment', return_value=True):
            setup_result = handler(setup_job)
            self.assertEqual(setup_result["status"], "success")
        
        # Then start training
        training_job = {
            "input": {
                "type": "train_with_yaml",
                "yaml_config": "model: test\ntraining:\n  epochs: 1"
            }
        }
        
        with patch('handler_fast.setup_environment', return_value=True):
            with patch('handler_fast.lazy_import_heavy_modules', return_value={'yaml': __import__('yaml'), 'uuid': __import__('uuid')}):
                with patch('builtins.open', unittest.mock.mock_open()):
                    training_result = handler(training_job)
                    self.assertEqual(training_result["status"], "success")


if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_suite.addTest(unittest.makeSuite(TestHandlerMethods))
    test_suite.addTest(unittest.makeSuite(TestHandlerIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)