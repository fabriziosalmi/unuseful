#!/usr/bin/env python3
"""
analyst.py - The Neural Linguist

This script uses a lightweight LLM to generate pseudo-scientific titles for
AI code fragments, acting as the second stage of the Memoria Residua project's
autonomous archival system.
"""

import sys
import json
from typing import Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Constants
MAX_LENGTH = 512  # Maximum input length for the model
MODEL_NAME = "distilgpt2"  # Using DistilGPT-2 for efficiency
# Prompt engineering for better titles
CONTEXT_TEMPLATE = """
Analisi di un Frammento di Memoria Residua

Questa è un'analisi scientifica di un frammento di codice recuperato durante una spedizione psionica digitale. Il frammento proviene da un progetto di {search_keyword} e richiede un'interpretazione accademica.

Il tuo compito è generare un titolo che catturi l'essenza computazionale di questo artefatto, utilizzando un linguaggio pseudo-scientifico e accademico. Il titolo deve:
- Essere lungo 5-10 parole
- Includere almeno un termine tecnico
- Suonare come il titolo di un paper accademico
- Evitare riferimenti diretti a tecnologie specifiche
- Mantenere un'aura di mistero epistemologico

Frammento Analizzato:
"""
{code}
"""

Titolo Accademico:"""

# Validation keywords for better title quality
TITLE_QUALITY_MARKERS = [
    'neural',
    'cognitive',
    'quantum',
    'emergent',
    'paradigm',
    'synthesis',
    'topology',
    'manifold',
    'epistemological',
    'ontological'
]

class NeuralAnalyst:
    def __init__(self):
        """Initialize the neural analyst with the language model."""
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        
        # Ensure we're running on CPU only
        self.model = self.model.cpu()
        self.model.eval()

    def truncate_code(self, code: str) -> str:
        """Truncate code to fit within model's maximum length."""
        tokens = self.tokenizer.encode(code)
        if len(tokens) > MAX_LENGTH:
            tokens = tokens[:MAX_LENGTH]
            code = self.tokenizer.decode(tokens)
        return code

    def generate_title(self, code: str) -> Optional[str]:
        """Generate a pseudo-scientific title for the code fragment."""
        try:
            # Truncate code if necessary
            code = self.truncate_code(code)
            
            # Extract context from the code
            code_lines = code.split('\n')[:50]  # Look at first 50 lines for context
            code_sample = '\n'.join(code_lines)
            
            # Get search keyword from input data or use a default
            search_keyword = self.input_data.get('search_keyword', 'intelligenza artificiale')
            
            # Format the prompt with context
            prompt = CONTEXT_TEMPLATE.format(
                code=code_sample,
                search_keyword=search_keyword
            )
            
            # Generate multiple titles and pick the best one
            best_title = None
            best_score = 0
            
            for _ in range(3):  # Try 3 times to get a good title
                # Tokenize input
                inputs = self.tokenizer(prompt, return_tensors="pt")
                
                # Generate title with higher temperature for creativity
                with torch.no_grad():
                    outputs = self.model.generate(
                        inputs["input_ids"],
                        max_new_tokens=50,
                        num_return_sequences=1,
                        temperature=0.9,
                        top_p=0.9,
                        no_repeat_ngram_size=2,
                        pad_token_id=self.tokenizer.eos_token_id
                    )
                
                # Decode and clean up the generated title
                generated_text = self.tokenizer.decode(outputs[0])
                title = generated_text.split("Titolo Accademico:")[-1].strip()
                
                # Clean up the title
                title = title.replace('"', '').strip()
                if len(title.split()) > 10:
                    title = " ".join(title.split()[:10])
                
                # Score the title based on quality markers
                score = sum(1 for marker in TITLE_QUALITY_MARKERS if marker.lower() in title.lower())
                
                if score > best_score:
                    best_score = score
                    best_title = title
                
                if best_score >= 2:  # If we have a good title, stop trying
                    break
            
            title = best_title if best_title else title
            
            return title
            
        except Exception as e:
            print(f"Error during title generation: {e}", file=sys.stderr)
            return None

def main():
    """Main entry point for the neural analyst."""
    try:
        # Read the input JSON from stdin
        input_data = json.load(sys.stdin)
        
        # Extract the code content
        code_content = input_data.get('file_content')
        if not code_content:
            print("No code content found in input", file=sys.stderr)
            return 1
        
        # Initialize and run the analyst
        analyst = NeuralAnalyst()
        title = analyst.generate_title(code_content)
        
        if title:
            # Add the title to the input data and output
            input_data['generated_title'] = title
            print(json.dumps(input_data))
            return 0
        else:
            print("Failed to generate title", file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    exit(main())
