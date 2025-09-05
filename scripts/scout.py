#!/usr/bin/env python3
"""
scout.py - The Digital Archaeologist

This script searches GitHub for AI-related code fragments, acting as the first stage
of the Memoria Residua project's autonomous archival system.
"""

import os
import json
import random
import base64
from typing import Dict, Any, Optional
from datetime import datetime
import requests
from github import Github
from github.ContentFile import ContentFile

# Search keywords for finding AI-related code
SEARCH_KEYWORDS = [
    'pytorch',
    'tensorflow',
    'keras',
    'scikit-learn',
    'llm',
    'neural network',
    'machine learning',
    'deep learning'
]

class ScoutBot:
    def __init__(self, token: str):
        """Initialize the scout with a GitHub API token."""
        self.token = token
        self.github = Github(token)
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def search_code(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        Search for AI-related code files on GitHub.
        Returns a dict with file information if successful, None otherwise.
        """
        try:
            # Construct the search query
            query = f'{keyword} in:file language:python size:>1024'
            
            # Search for code using PyGithub
            results = self.github.search_code(query)
            
            if results.totalCount == 0:
                return None
            
            # Select a random result from the first page
            files = list(results[:10])  # Limit to first 10 results to avoid rate limits
            if not files:
                return None
                
            selected_file = random.choice(files)
            
            # Get the file content
            content = selected_file.decoded_content.decode('utf-8')
            
            return {
                'file_content': content,
                'source_url': selected_file.html_url,
                'repo_url': selected_file.repository.html_url,
                'file_path': selected_file.path,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Error during code search: {e}")
            return None

    def excavate(self) -> Optional[Dict[str, Any]]:
        """
        Main function to search for and retrieve a random code fragment.
        """
        # Choose a random keyword
        keyword = random.choice(SEARCH_KEYWORDS)
        
        # Search for code using the keyword
        result = self.search_code(keyword)
        
        return result

def main():
    """Main entry point for the scout bot."""
    # Get GitHub token from environment
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")

    # Initialize and run the scout
    scout = ScoutBot(github_token)
    result = scout.excavate()

    if result:
        # Output the result as JSON
        print(json.dumps(result))
        return 0
    else:
        print("No suitable fragments found")
        return 1

if __name__ == '__main__':
    exit(main())
