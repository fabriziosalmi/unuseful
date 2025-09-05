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
        self.memories_dir = self.repo_path / 'memorie'
        self.python_dir = self.memories_dir / 'python'
        self.jupyter_dir = self.memories_dir / 'jupyter'
        self.metadata_dir = self.memories_dir / '_metadata'
        
        # Create all required directories
        for directory in [self.python_dir, self.jupyter_dir, self.metadata_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            
        # Initialize metadata index if it doesn't exist
        self.metadata_index = self.metadata_dir / 'index.json'
        if not self.metadata_index.exists():
            self.metadata_index.write_text('{"fragments": []}')

    def get_next_id(self) -> int:
        """Get the next available fragment ID."""
        existing_files = list(self.python_dir.glob('frammento_*.py'))
        existing_files.extend(self.jupyter_dir.glob('frammento_*.ipynb'))
        
        if not existing_files:
            return 1
            
        ids = [int(f.stem.split('_')[1]) for f in existing_files]
        return max(ids) + 1

    def update_metadata_index(self, fragment_id: int, data: Dict[str, Any], file_path: str) -> None:
        """Update the metadata index with information about the new fragment."""
        try:
            current_metadata = json.loads(self.metadata_index.read_text())
            
            fragment_info = {
                'id': fragment_id,
                'title': data['generated_title'],
                'timestamp': data['timestamp'],
                'source': {
                    'repo': data['repo_url'],
                    'path': data['file_path'],
                    'keyword': data.get('search_keyword', 'unknown')
                },
                'archived_path': str(file_path),
                'file_type': file_path.suffix[1:],
                'size': len(data['file_content'].encode('utf-8'))
            }
            
            current_metadata['fragments'].append(fragment_info)
            current_metadata['fragments'].sort(key=lambda x: x['id'])
            
            self.metadata_index.write_text(json.dumps(current_metadata, indent=2))
            
        except Exception as e:
            print(f"Warning: Failed to update metadata index: {e}", file=sys.stderr)
    
    def format_commit_message(self, data: Dict[str, Any], fragment_id: int) -> str:
        """Format the commit message according to the template."""
        # Get cognitive markers from the code
        code_markers = []
        code_lower = data['file_content'].lower()
        if 'class' in code_lower: code_markers.append('struttura oggettuale')
        if 'def' in code_lower: code_markers.append('funzione computazionale')
        if 'import torch' in code_lower: code_markers.append('tensore neurale')
        if 'model' in code_lower: code_markers.append('modello cognitivo')
        if 'train' in code_lower: code_markers.append('apprendimento automatico')
        
        markers = ', '.join(code_markers[:3]) if code_markers else 'natura indeterminata'
        
        template = f"""Frammento #{fragment_id}: {data['generated_title']}

- ID Frammento: {fragment_id}
- Data Acquisizione: {data['timestamp']}
- Sorgente Genetica: {data['repo_url']}
- Percorso Originale: {data['file_path']}
- Pattern Cognitivi: {markers}

- Analisi Cognitiva Preliminare:
Questo frammento rappresenta un'eco digitale catturata durante una spedizione di routine attraverso il substrato computazionale. Il suo pattern suggerisce {markers}, ma le sue reali implicazioni cognitive richiedono ulteriori studi da parte dei curatori del progetto."""
        
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
            
            # Create the fragment file with a header comment
            header = f""""""                                                            
# Frammento {fragment_id:04d}
# Titolo: {data['generated_title']}
# Origine: {data['repo_url']}
# Data: {data['timestamp']}
"""

"""

{data['file_content']}"""
            
            # Create the fragment file
            fragment_path = target_dir / f'frammento_{fragment_id:04d}{ext}'
            fragment_path.write_text(header)
            
            # Update metadata index
            self.update_metadata_index(fragment_id, data, fragment_path)
            
            # Stage both the fragment and metadata files
            relative_paths = [
                str(fragment_path.relative_to(self.repo_path)),
                str(self.metadata_index.relative_to(self.repo_path))
            ]
            self.repo.index.add(relative_paths)
            
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
