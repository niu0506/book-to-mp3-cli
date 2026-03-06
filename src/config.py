"""
Configuration module for book-to-mp3-cli
Centralizes logging and configuration settings
"""

import logging

# Configure logging globally
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
