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

# Search keywords and configurations
SEARCH_CONFIG = {
    'keywords': [
        'pytorch',
        'tensorflow',
        'keras',
        'scikit-learn',
        'llm',
        'neural network',
        'machine learning',
        'deep learning',
        'transformers',
        'huggingface',
        'gpt',
        'bert',
        'reinforcement learning',
        'computer vision'
    ],
    'file_types': ['py', 'ipynb'],
    'min_file_size': 1024,  # Skip very small files
    'max_file_size': 1024 * 100,  # Skip huge files
    'results_per_query': 10
}

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
            # Build a more targeted search query
            extensions = ' OR '.join(f'extension:{ext}' for ext in SEARCH_CONFIG['file_types'])
            size_range = f'{SEARCH_CONFIG["min_file_size"]}..{SEARCH_CONFIG["max_file_size"]}'
            query = f'{keyword} in:file ({extensions}) size:{size_range}'
            
            # Add some qualifiers to find more interesting code
            qualifiers = [
                'NOT in:name test',  # Avoid test files
                'NOT in:name example',  # Avoid example files
                'NOT filename:README',  # Avoid documentation
                'fork:false'  # Only search in original repositories
            ]
            query = f'{query} {" ".join(qualifiers)}'
            
            # Search for code using PyGithub
            results = self.github.search_code(query)
            
            if results.totalCount == 0:
                return None
            
            # Get multiple pages of results if available
            files = []
            try:
                for i, result in enumerate(results):
                    if i >= SEARCH_CONFIG['results_per_query']:
                        break
                    files.append(result)
            except Exception as e:
                print(f"Warning: Error fetching results: {e}", file=sys.stderr)
                if not files:  # Only fail if we have no results at all
                    return None
            
            if not files:
                return None
                
            # Try to find an interesting file (with actual code)
            for _ in range(3):  # Try up to 3 times
                selected_file = random.choice(files)
                try:
                    content = selected_file.decoded_content.decode('utf-8')
                    
                    # Basic validation of content
                    if len(content.strip()) < 100:  # Skip very short files
                        continue
                        
                    if not any(keyword in content.lower() for keyword in [
                        'def ', 'class ', 'import ', 'model', 'train'
                    ]):
                        continue
                    
                    return {
                        'file_content': content,
                        'source_url': selected_file.html_url,
                        'repo_url': selected_file.repository.html_url,
                        'file_path': selected_file.path,
                        'timestamp': datetime.utcnow().isoformat(),
                        'search_keyword': keyword
                    }
                except Exception as e:
                    print(f"Warning: Error processing file: {e}", file=sys.stderr)
                    continue
            
            return None
            
        except Exception as e:
            print(f"Error during code search: {e}")
            return None

    def excavate(self) -> Optional[Dict[str, Any]]:
        """
        Main function to search for and retrieve a random code fragment.
        """
        # Try different keywords until we find something interesting
        keywords = list(SEARCH_CONFIG['keywords'])
        random.shuffle(keywords)
        
        for keyword in keywords[:5]:  # Try up to 5 random keywords
            try:
                result = self.search_code(keyword)
                if result:
                    return result
            except Exception as e:
                print(f"Warning: Search failed for keyword '{keyword}': {e}", file=sys.stderr)
                continue
        
        return None

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
