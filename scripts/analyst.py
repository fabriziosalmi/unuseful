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
PROMPT_TEMPLATE = '''Il seguente frammento di codice Python è una memoria residua di un'intelligenza artificiale. Genera un titolo accademico e pseudo-scientifico di massimo 10 parole per descriverlo.

Codice:
"""
{code}
"""

Titolo:'''

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
            
            # Format the prompt
            prompt = PROMPT_TEMPLATE.format(code=code)
            
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt")
            
            # Generate title
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"],
                    max_new_tokens=50,
                    num_return_sequences=1,
                    temperature=0.7,
                    no_repeat_ngram_size=2,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode and clean up the generated title
            generated_text = self.tokenizer.decode(outputs[0])
            title = generated_text.split("Titolo:")[-1].strip()
            
            # Ensure the title is not too long
            if len(title.split()) > 10:
                title = " ".join(title.split()[:10])
            
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
