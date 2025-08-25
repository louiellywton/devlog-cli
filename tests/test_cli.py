#!/usr/bin/env python3
"""
Tests for DevLog CLI functionality.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from devlog.cli import (
    ensure_directory, load_config, load_logs, save_logs,
    log_entry, show_log, show_stats, search_logs,
    export_logs, show_categories
)


class TestDevLogCLI(unittest.TestCase):
    """Test cases for DevLog CLI functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_config_dir = None
        
        # Patch the config directory for testing
        if hasattr(sys.modules['devlog.cli'], 'CONFIG_DIR'):
            self.original_config_dir = sys.modules['devlog.cli'].CONFIG_DIR
            sys.modules['devlog.cli'].CONFIG_DIR = self.temp_dir
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
        
        # Restore original config directory
        if self.original_config_dir:
            sys.modules['devlog.cli'].CONFIG_DIR = self.original_config_dir
    
    def test_ensure_directory(self):
        """Test directory creation."""
        test_dir = os.path.join(self.temp_dir, "test_subdir")
        with patch('devlog.cli.CONFIG_DIR', test_dir):
            ensure_directory()
            self.assertTrue(os.path.exists(test_dir))
    
    def test_load_config_default(self):
        """Test loading default configuration."""
        with patch('devlog.cli.CONFIG_FILE', os.path.join(self.temp_dir, "config.json")):
            config = load_config()
            self.assertIn("categories", config)
            self.assertIn("default_category", config)
            self.assertIn("tags_enabled", config)
    
    def test_load_config_existing(self):
        """Test loading existing configuration."""
        test_config = {"categories": ["test"], "default_category": "test"}
        config_file = os.path.join(self.temp_dir, "config.json")
        
        with open(config_file, 'w') as f:
            json.dump(test_config, f)
        
        with patch('devlog.cli.CONFIG_FILE', config_file):
            config = load_config()
            self.assertEqual(config["categories"], ["test"])
            self.assertEqual(config["default_category"], "test")
    
    def test_load_logs_empty(self):
        """Test loading empty logs."""
        with patch('devlog.cli.LOG_FILE', os.path.join(self.temp_dir, "logs.json")):
            logs = load_logs()
            self.assertIn("entries", logs)
            self.assertIn("metadata", logs)
            self.assertEqual(len(logs["entries"]), 0)
    
    def test_load_logs_existing(self):
        """Test loading existing logs."""
        test_logs = {
            "entries": [{"id": 1, "text": "test"}],
            "metadata": {"created": "2025-01-01"}
        }
        log_file = os.path.join(self.temp_dir, "logs.json")
        
        with open(log_file, 'w') as f:
            json.dump(test_logs, f)
        
        with patch('devlog.cli.LOG_FILE', log_file):
            logs = load_logs()
            self.assertEqual(len(logs["entries"]), 1)
            self.assertEqual(logs["entries"][0]["text"], "test")
    
    def test_save_logs(self):
        """Test saving logs."""
        test_logs = {"entries": [], "metadata": {"created": "2025-01-01"}}
        log_file = os.path.join(self.temp_dir, "logs.json")
        
        with patch('devlog.cli.LOG_FILE', log_file):
            save_logs(test_logs)
            self.assertTrue(os.path.exists(log_file))
            
            with open(log_file, 'r') as f:
                saved_logs = json.load(f)
            self.assertEqual(saved_logs, test_logs)
    
    @patch('devlog.cli.load_config')
    @patch('devlog.cli.load_logs')
    @patch('devlog.cli.save_logs')
    def test_log_entry_basic(self, mock_save, mock_load, mock_config):
        """Test basic log entry creation."""
        mock_config.return_value = {
            "categories": ["coding"],
            "default_category": "coding",
            "tags_enabled": True,
            "max_tags": 5
        }
        mock_load.return_value = {"entries": [], "metadata": {}}
        
        with patch('builtins.print') as mock_print:
            log_entry("Test entry")
            
            mock_save.assert_called_once()
            mock_print.assert_called_with("✓ Logged: Test entry (coding)")
    
    @patch('devlog.cli.load_config')
    @patch('devlog.cli.load_logs')
    @patch('devlog.cli.save_logs')
    def test_log_entry_with_tags(self, mock_save, mock_load, mock_config):
        """Test log entry with automatic tag extraction."""
        mock_config.return_value = {
            "categories": ["coding"],
            "default_category": "coding",
            "tags_enabled": True,
            "max_tags": 5
        }
        mock_load.return_value = {"entries": [], "metadata": {}}
        
        with patch('builtins.print') as mock_print:
            log_entry("Test entry #bug #frontend")
            
            mock_save.assert_called_once()
            # Check that tags were extracted and text was cleaned
            saved_logs = mock_save.call_args[0][0]
            entry = saved_logs["entries"][0]
            self.assertEqual(entry["text"], "Test entry")
            self.assertEqual(entry["tags"], ["bug", "frontend"])
    
    @patch('devlog.cli.load_logs')
    def test_show_log_empty(self, mock_load):
        """Test showing empty log."""
        mock_load.return_value = {"entries": []}
        
        with patch('builtins.print') as mock_print:
            show_log()
            mock_print.assert_called_with("No entries found matching your criteria.")
    
    @patch('devlog.cli.load_logs')
    def test_show_log_with_entries(self, mock_load):
        """Test showing log with entries."""
        mock_load.return_value = {
            "entries": [{
                "date": "2025-01-01",
                "time": "10:00",
                "text": "Test entry",
                "category": "coding",
                "tags": ["test"]
            }]
        }
        
        with patch('builtins.print') as mock_print:
            show_log()
            mock_print.assert_called_with("2025-01-01 10:00 [coding]: Test entry #test")
    
    @patch('devlog.cli.load_logs')
    def test_show_stats_empty(self, mock_load):
        """Test statistics with empty log."""
        mock_load.return_value = {"entries": []}
        
        with patch('builtins.print') as mock_print:
            show_stats()
            mock_print.assert_called_with("📊 No entries found. Start logging to see statistics!")
    
    @patch('devlog.cli.load_logs')
    def test_show_stats_with_entries(self, mock_load):
        """Test statistics with entries."""
        mock_load.return_value = {
            "entries": [
                {"date": "2025-01-01", "category": "coding", "tags": ["bug"]},
                {"date": "2025-01-01", "category": "debugging", "tags": ["bug"]},
                {"date": "2025-01-02", "category": "coding", "tags": ["feature"]}
            ]
        }
        
        with patch('builtins.print') as mock_print:
            show_stats()
            # Check that statistics were displayed
            calls = [call[0][0] for call in mock_print.call_args_list]
            self.assertTrue(any("Total entries: 3" in call for call in calls))
            self.assertTrue(any("Days with entries: 2" in call for call in calls))
    
    @patch('devlog.cli.load_logs')
    def test_search_logs(self, mock_load):
        """Test log search functionality."""
        mock_load.return_value = {
            "entries": [
                {"date": "2025-01-01", "time": "10:00", "text": "Bug fix", "category": "coding", "tags": ["bug"]},
                {"date": "2025-01-02", "time": "11:00", "text": "Feature implementation", "category": "coding", "tags": ["feature"]}
            ]
        }
        
        with patch('builtins.print') as mock_print:
            search_logs("bug")
            # Check that search results were displayed
            calls = [call[0][0] for call in mock_print.call_args_list]
            self.assertTrue(any("Search Results for 'bug'" in call for call in calls))
    
    def test_export_logs_json(self):
        """Test JSON export functionality."""
        test_logs = {
            "entries": [{"date": "2025-01-01", "time": "10:00", "text": "Test", "category": "coding", "tags": []}],
            "metadata": {}
        }
        
        with patch('devlog.cli.load_logs', return_value=test_logs), \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('builtins.print') as mock_print:
            
            export_logs("json")
            mock_file.assert_called()
            # Check that the message contains the right format, ignoring timestamp
            mock_print.assert_called()
            call_args = mock_print.call_args[0][0]
            self.assertIn("📤 Exported 1 entries to devlog_export_", call_args)
            self.assertIn(".json", call_args)
    
    def test_export_logs_csv(self):
        """Test CSV export functionality."""
        test_logs = {
            "entries": [{"date": "2025-01-01", "time": "10:00", "text": "Test", "category": "coding", "tags": []}],
            "metadata": {}
        }
        
        with patch('devlog.cli.load_logs', return_value=test_logs), \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('builtins.print') as mock_print:
            
            export_logs("csv")
            mock_file.assert_called()
            # Check that the message contains the right format, ignoring timestamp
            mock_print.assert_called()
            call_args = mock_print.call_args[0][0]
            self.assertIn("📤 Exported 1 entries to devlog_export_", call_args)
            self.assertIn(".csv", call_args)
    
    def test_export_logs_markdown(self):
        """Test Markdown export functionality."""
        test_logs = {
            "entries": [{"date": "2025-01-01", "time": "10:00", "text": "Test", "category": "coding", "tags": []}],
            "metadata": {}
        }
        
        with patch('devlog.cli.load_logs', return_value=test_logs), \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('builtins.print') as mock_print:
            
            export_logs("markdown")
            mock_file.assert_called()
            # Check that the message contains the right format, ignoring timestamp
            mock_print.assert_called()
            call_args = mock_print.call_args[0][0]
            self.assertIn("📤 Exported 1 entries to devlog_export_", call_args)
            self.assertIn(".md", call_args)
    
    @patch('devlog.cli.load_config')
    def test_show_categories(self, mock_config):
        """Test showing available categories."""
        mock_config.return_value = {
            "categories": ["coding", "debugging", "planning"]
        }
        
        with patch('builtins.print') as mock_print:
            show_categories()
            # Check that categories were displayed
            calls = [call[0][0] for call in mock_print.call_args_list]
            self.assertTrue(any("coding" in call for call in calls))
            self.assertTrue(any("debugging" in call for call in calls))
            self.assertTrue(any("planning" in call for call in calls))


if __name__ == '__main__':
    unittest.main()
