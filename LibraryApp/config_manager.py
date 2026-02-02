#!/usr/bin/env python3
"""
Configuration Manager for Hybrid Database Mode
Determines whether to use local or remote database
"""

import os
import json

class ConfigManager:
    """Manages application configuration for database mode"""
    
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'app_config.json')
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        default_config = {
            'database_mode': 'auto',  # 'local', 'remote', or 'auto'
            'auto_sync_enabled': True,
            'sync_interval_minutes': 30,
            'use_connection_pool': True,
            'batch_email_enabled': True,
            'max_email_workers': 5,
            'email_batch_size': 10
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except:
                pass
        else:
            self._save_config(default_config)
        
        return default_config
    
    def _save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_database_mode(self):
        """
        Determine which database to use
        Returns: 'local' or 'remote'
        """
        mode = self.config.get('database_mode', 'auto')
        
        if mode == 'local':
            return 'local'
        elif mode == 'remote':
            return 'remote'
        else:  # auto mode
            # Check if remote DB is configured
            if os.getenv('DB_HOST') and os.getenv('DB_HOST') != 'localhost':
                return 'remote'
            else:
                return 'local'
    
    def is_sync_enabled(self):
        """Check if auto-sync is enabled"""
        return self.config.get('auto_sync_enabled', True)
    
    def get_sync_interval(self):
        """Get sync interval in minutes"""
        return self.config.get('sync_interval_minutes', 30)
    
    def use_connection_pool(self):
        """Check if connection pooling should be used"""
        return self.config.get('use_connection_pool', True)
    
    def is_batch_email_enabled(self):
        """Check if batch email sending is enabled"""
        return self.config.get('batch_email_enabled', True)
    
    def get_email_config(self):
        """Get email configuration"""
        return {
            'max_workers': self.config.get('max_email_workers', 5),
            'batch_size': self.config.get('email_batch_size', 10)
        }
    
    def set_database_mode(self, mode):
        """Set database mode ('local', 'remote', or 'auto')"""
        if mode in ['local', 'remote', 'auto']:
            self.config['database_mode'] = mode
            self._save_config()
            return True
        return False
    
    def enable_auto_sync(self, enabled=True):
        """Enable or disable auto-sync"""
        self.config['auto_sync_enabled'] = enabled
        self._save_config()
    
    def set_sync_interval(self, minutes):
        """Set sync interval in minutes"""
        if minutes > 0:
            self.config['sync_interval_minutes'] = minutes
            self._save_config()
            return True
        return False


# Global config instance
_config_instance = None

def get_config():
    """Get singleton config instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance
