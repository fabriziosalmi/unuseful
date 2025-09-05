#!/usr/bin/env python3
"""
archivist.py - The Memory Curator

This script handles the final stage of the Memoria Residua project's autonomous
archival system, storing code fragments and committing them to the repository.
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import git

class MemoryArchivist:
    def __init__(self, repo_path: str):
        """Initialize the archivist with the repository path."""
        self.repo_path = Path(repo_path)
        self.repo = git.Repo(self.repo_path)
        
        # Ensure the memories directories exist
        self.python_dir = self.repo_path / 'memorie' / 'python'
        self.jupyter_dir = self.repo_path / 'memorie' / 'jupyter'
        self.python_dir.mkdir(parents=True, exist_ok=True)
        self.jupyter_dir.mkdir(parents=True, exist_ok=True)

    def get_next_id(self) -> int:
        """Get the next available fragment ID."""
        existing_files = list(self.python_dir.glob('frammento_*.py'))
        existing_files.extend(self.jupyter_dir.glob('frammento_*.ipynb'))
        
        if not existing_files:
            return 1
            
        ids = [int(f.stem.split('_')[1]) for f in existing_files]
        return max(ids) + 1

    def format_commit_message(self, data: Dict[str, Any], fragment_id: int) -> str:
        """Format the commit message according to the template."""
        template = f"""Frammento #{fragment_id}: {data['generated_title']}

- ID Frammento: {fragment_id}
- Data Acquisizione: {data['timestamp']}
- Sorgente Genetica: {data['repo_url']}
- Percorso Originale: {data['file_path']}

- Analisi Cognitiva Preliminare:
Questo frammento rappresenta un'eco digitale catturata durante una spedizione di routine. La sua funzione e le sue implicazioni cognitive richiedono ulteriori studi da parte dei curatori del progetto."""
        
        return template

    def store_fragment(self, data: Dict[str, Any]) -> Optional[str]:
        """Store a code fragment in the repository and commit it."""
        try:
            # Get the next fragment ID
            fragment_id = self.get_next_id()
            
            # Determine the file extension and directory
            if data['file_path'].endswith('.ipynb'):
                target_dir = self.jupyter_dir
                ext = '.ipynb'
            else:
                target_dir = self.python_dir
                ext = '.py'
            
            # Create the fragment file
            fragment_path = target_dir / f'frammento_{fragment_id:04d}{ext}'
            fragment_path.write_text(data['file_content'])
            
            # Stage the file
            self.repo.index.add([str(fragment_path.relative_to(self.repo_path))])
            
            # Create the commit
            commit_message = self.format_commit_message(data, fragment_id)
            self.repo.index.commit(commit_message)
            
            return str(fragment_path)
            
        except Exception as e:
            print(f"Error storing fragment: {e}", file=sys.stderr)
            return None

def main():
    """Main entry point for the memory archivist."""
    try:
        # Read the input JSON from stdin
        input_data = json.load(sys.stdin)
        
        # Initialize the archivist with the current directory
        archivist = MemoryArchivist(os.getcwd())
        
        # Store the fragment
        result = archivist.store_fragment(input_data)
        
        if result:
            print(f"Successfully stored fragment at: {result}")
            return 0
        else:
            print("Failed to store fragment", file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    exit(main())
