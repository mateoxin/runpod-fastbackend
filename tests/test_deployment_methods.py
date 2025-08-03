#!/usr/bin/env python3
"""
🧪 Comprehensive tests for deploy_fast.py methods
Test all deployment functions and scenarios
"""

import sys
import os
import json
import unittest
import tempfile
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestDeploymentMethods(unittest.TestCase):
    """Test all methods in deploy_fast.py"""
    
    def setUp(self):
        """Setup test environment"""
        self.original_env = os.environ.copy()
        os.environ['RUNPOD_API_KEY'] = 'test_api_key'
        os.environ['GITHUB_USERNAME'] = 'test_user'
        os.environ['GITHUB_REPO'] = 'test_repo'
        
    def tearDown(self):
        """Clean up test environment"""
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def test_create_fast_endpoint_success(self):
        """Test successful endpoint creation"""
        from deploy_fast import create_fast_endpoint
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test_endpoint_123"}
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            endpoint_id = create_fast_endpoint()
            
            self.assertEqual(endpoint_id, "test_endpoint_123")
            
            # Check that POST was called with correct parameters
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            
            # Check URL
            self.assertIn("endpoints", call_args[0][0])
            
            # Check headers
            headers = call_args[1]['headers']
            self.assertIn('Authorization', headers)
            self.assertEqual(headers['Content-Type'], 'application/json')
            
            # Check config
            config = call_args[1]['json']
            self.assertIn('name', config)
            self.assertIn('lora-fast-', config['name'])
            self.assertEqual(config['image_name'], "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04")
    
    def test_create_fast_endpoint_failure(self):
        """Test endpoint creation failure"""
        from deploy_fast import create_fast_endpoint
        
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        
        with patch('requests.post', return_value=mock_response):
            endpoint_id = create_fast_endpoint()
            
            self.assertIsNone(endpoint_id)
    
    def test_create_fast_pod_success(self):
        """Test successful pod creation"""
        from deploy_fast import create_fast_pod
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test_pod_456"}
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            pod_id = create_fast_pod()
            
            self.assertEqual(pod_id, "test_pod_456")
            
            # Check that POST was called with pod endpoint
            call_args = mock_post.call_args
            self.assertIn("pods", call_args[0][0])
            
            # Check pod config
            config = call_args[1]['json']
            self.assertIn('name', config)
            self.assertIn('lora-fast-pod-', config['name'])
            self.assertEqual(config['ports'], "8000/http")
    
    def test_create_fast_pod_failure(self):
        """Test pod creation failure"""
        from deploy_fast import create_fast_pod
        
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        
        with patch('requests.post', return_value=mock_response):
            pod_id = create_fast_pod()
            
            self.assertIsNone(pod_id)
    
    def test_test_endpoint_success(self):
        """Test successful endpoint testing"""
        from deploy_fast import test_endpoint
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "output": {"status": "healthy"}
        }
        
        with patch('requests.post', return_value=mock_response) as mock_post:
            result = test_endpoint("test_endpoint_123")
            
            self.assertTrue(result)
            
            # Check test payload
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            self.assertEqual(payload['input']['type'], 'health')
    
    def test_test_endpoint_failure(self):
        """Test endpoint testing failure"""
        from deploy_fast import test_endpoint
        
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Endpoint not found"
        
        with patch('requests.post', return_value=mock_response):
            result = test_endpoint("invalid_endpoint")
            
            self.assertFalse(result)
    
    def test_update_github_urls(self):
        """Test GitHub URL update instructions"""
        from deploy_fast import update_github_urls
        
        # This function just prints instructions, so we test that it runs without error
        try:
            update_github_urls()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_deploy_with_mcp_success(self):
        """Test MCP deployment configuration"""
        from deploy_fast import deploy_with_mcp
        
        config = deploy_with_mcp()
        
        self.assertIsNotNone(config)
        self.assertIn('name', config)
        self.assertIn('lora-fast-mcp-', config['name'])
        self.assertEqual(config['imageName'], "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04")
        self.assertEqual(config['gpuCount'], 1)
        self.assertEqual(config['containerDiskInGb'], 50)
        self.assertEqual(config['volumeInGb'], 100)
    
    def test_environment_variables(self):
        """Test environment variable handling"""
        from deploy_fast import RUNPOD_API_KEY, GITHUB_USERNAME, GITHUB_REPO
        
        self.assertEqual(RUNPOD_API_KEY, 'test_api_key')
        self.assertEqual(GITHUB_USERNAME, 'test_user')
        self.assertEqual(GITHUB_REPO, 'test_repo')
    
    def test_github_url_construction(self):
        """Test GitHub URL construction"""
        from deploy_fast import GITHUB_RAW_URL, STARTUP_SCRIPT_URL
        
        self.assertIn('test_user', GITHUB_RAW_URL)
        self.assertIn('test_repo', GITHUB_RAW_URL)
        self.assertIn('startup.sh', STARTUP_SCRIPT_URL)


class TestDeploymentConfig(unittest.TestCase):
    """Test deployment configuration generation"""
    
    def test_endpoint_config_completeness(self):
        """Test that endpoint config has all required fields"""
        from deploy_fast import create_fast_endpoint
        
        with patch('requests.post') as mock_post:
            # Mock to capture the config without making actual request
            mock_post.return_value.status_code = 400  # Force function to return None
            
            create_fast_endpoint()
            
            # Get the config that was passed
            config = mock_post.call_args[1]['json']
            
            required_fields = [
                'name', 'image_name', 'docker_start_cmd', 'container_disk_in_gb',
                'volume_in_gb', 'gpu_type_id', 'env', 'workers_min', 'workers_max',
                'idle_timeout', 'locations'
            ]
            
            for field in required_fields:
                self.assertIn(field, config, f"Missing required field: {field}")
    
    def test_pod_config_completeness(self):
        """Test that pod config has all required fields"""
        from deploy_fast import create_fast_pod
        
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 400
            
            create_fast_pod()
            
            config = mock_post.call_args[1]['json']
            
            required_fields = [
                'name', 'image_name', 'gpu_type_id', 'container_disk_in_gb',
                'volume_in_gb', 'docker_start_cmd', 'env', 'ports'
            ]
            
            for field in required_fields:
                self.assertIn(field, config, f"Missing required field: {field}")
    
    def test_environment_variables_in_config(self):
        """Test that environment variables are properly set in configs"""
        from deploy_fast import create_fast_endpoint
        
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 400
            
            create_fast_endpoint()
            
            config = mock_post.call_args[1]['json']
            env = config['env']
            
            # Check required environment variables
            required_env = ['HF_TOKEN', 'PYTHONUNBUFFERED', 'GITHUB_USERNAME', 'GITHUB_REPO']
            
            for env_var in required_env:
                self.assertIn(env_var, env, f"Missing environment variable: {env_var}")


class TestDeploymentIntegration(unittest.TestCase):
    """Integration tests for deployment workflows"""
    
    def setUp(self):
        """Setup test environment"""
        os.environ['RUNPOD_API_KEY'] = 'test_api_key'
        os.environ['GITHUB_USERNAME'] = 'test_user'
        os.environ['GITHUB_REPO'] = 'test_repo'
    
    def test_endpoint_creation_and_testing_workflow(self):
        """Test complete endpoint creation and testing workflow"""
        from deploy_fast import create_fast_endpoint, test_endpoint
        
        # Mock endpoint creation
        mock_create_response = Mock()
        mock_create_response.status_code = 200
        mock_create_response.json.return_value = {"id": "test_endpoint_789"}
        
        # Mock endpoint testing
        mock_test_response = Mock()
        mock_test_response.status_code = 200
        mock_test_response.json.return_value = {
            "status": "success",
            "output": {"status": "healthy"}
        }
        
        with patch('requests.post', side_effect=[mock_create_response, mock_test_response]):
            # Create endpoint
            endpoint_id = create_fast_endpoint()
            self.assertEqual(endpoint_id, "test_endpoint_789")
            
            # Test endpoint
            test_result = test_endpoint(endpoint_id)
            self.assertTrue(test_result)
    
    def test_full_deployment_workflow_simulation(self):
        """Simulate complete deployment workflow"""
        from deploy_fast import create_fast_endpoint, test_endpoint
        
        # Simulate the full workflow
        responses = [
            # Endpoint creation response
            Mock(status_code=200, json=lambda: {"id": "endpoint_123"}),
            # Endpoint test response
            Mock(status_code=200, json=lambda: {"status": "success", "output": {"status": "healthy"}})
        ]
        
        with patch('requests.post', side_effect=responses):
            with patch('time.sleep'):  # Skip actual waiting
                # Create endpoint
                endpoint_id = create_fast_endpoint()
                self.assertIsNotNone(endpoint_id)
                
                # Test endpoint
                test_result = test_endpoint(endpoint_id)
                self.assertTrue(test_result)


class TestDeploymentErrorHandling(unittest.TestCase):
    """Test error handling in deployment functions"""
    
    def test_network_error_handling(self):
        """Test handling of network errors"""
        from deploy_fast import create_fast_endpoint
        
        with patch('requests.post', side_effect=ConnectionError("Network error")):
            # Should handle exception gracefully
            try:
                endpoint_id = create_fast_endpoint()
                # Function should handle the error and return None or raise appropriately
                self.assertTrue(True)  # If we get here, error was handled
            except ConnectionError:
                self.fail("Network error not handled properly")
    
    def test_invalid_api_key_simulation(self):
        """Test handling of invalid API key"""
        from deploy_fast import create_fast_endpoint
        
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        
        with patch('requests.post', return_value=mock_response):
            endpoint_id = create_fast_endpoint()
            self.assertIsNone(endpoint_id)
    
    def test_missing_environment_variables(self):
        """Test behavior with missing environment variables"""
        # Remove environment variables
        env_backup = {}
        for key in ['RUNPOD_API_KEY', 'GITHUB_USERNAME', 'GITHUB_REPO']:
            if key in os.environ:
                env_backup[key] = os.environ[key]
                del os.environ[key]
        
        try:
            # Import should still work but use defaults
            import deploy_fast
            
            # Check that defaults are used
            self.assertEqual(deploy_fast.RUNPOD_API_KEY, "YOUR_API_KEY_HERE")
            self.assertEqual(deploy_fast.GITHUB_USERNAME, "mateoxin")
            self.assertEqual(deploy_fast.GITHUB_REPO, "runpod-fastbackend")
            
        finally:
            # Restore environment variables
            for key, value in env_backup.items():
                os.environ[key] = value


if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_suite.addTest(unittest.makeSuite(TestDeploymentMethods))
    test_suite.addTest(unittest.makeSuite(TestDeploymentConfig))
    test_suite.addTest(unittest.makeSuite(TestDeploymentIntegration))
    test_suite.addTest(unittest.makeSuite(TestDeploymentErrorHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)