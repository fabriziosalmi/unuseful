// Fragment data embedded directly in JavaScript
const FRAGMENTS_DATA = {
  "fragments": [
    {
      "id": 3,
      "title": "Modello cognitivo con tensore neurale",
      "timestamp": "2024-03-21T15:30:00Z",
      "source": {
        "repo": "https://github.com/fabriziosalmi/unuseful",
        "path": "examples/neural_pattern.py",
        "keyword": "neural"
      },
      "content": `import torch
import torch.nn as nn

class CognitiveLayer(nn.Module):
    """Strato cognitivo che implementa un pattern di apprendimento adattivo."""
    
    def __init__(self, input_dim: int, pattern_dim: int):
        super().__init__()
        self.pattern_weights = nn.Parameter(torch.randn(input_dim, pattern_dim))
        self.activation = nn.Tanh()
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Proiezione dell'input nello spazio dei pattern
        pattern_space = torch.matmul(x, self.pattern_weights)
        # Attivazione non lineare per emergenza di pattern
        activated_patterns = self.activation(pattern_space)
        return activated_patterns

class CognitiveNetwork(nn.Module):
    """Rete neurale che implementa un sistema cognitivo multi-livello."""
    
    def __init__(self, layers_dims: list[int]):
        super().__init__()
        self.cognitive_layers = nn.ModuleList([
            CognitiveLayer(in_dim, out_dim)
            for in_dim, out_dim in zip(layers_dims[:-1], layers_dims[1:])
        ])
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Propagazione attraverso gli strati cognitivi
        for layer in self.cognitive_layers:
            x = layer(x)
        return x

# Esempio di utilizzo
input_dim = 784  # Dimensione input (es. MNIST)
pattern_dims = [784, 256, 64, 10]  # Dimensioni degli strati

# Creazione del modello
model = CognitiveNetwork(pattern_dims)

# Input di esempio
batch_size = 32
input_data = torch.randn(batch_size, input_dim)

# Inferenza
patterns = model(input_data)
print(f"Pattern emergenti: {patterns.shape}")
`,
      "file_type": "python",
      "patterns": "struttura oggettuale,tensore neurale,modello cognitivo,apprendimento automatico",
      "size": 1536
    },
    {
      "id": 2,
      "title": "Archivista cognitivo avanzato",
      "timestamp": "2024-03-20T18:45:00Z",
      "source": {
        "repo": "https://github.com/fabriziosalmi/unuseful",
        "path": "scripts/enhanced_archivist.py",
        "keyword": "archive"
      },
      "content": `from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import json
import hashlib

@dataclass
class CognitiveMeta:
    """Metadati cognitivi per un frammento archiviato."""
    timestamp: datetime
    patterns: List[str]
    complexity: float
    entropy: float
    connections: List[str]

class CognitiveFragment:
    """Un frammento di conoscenza con proprietà cognitive."""
    
    def __init__(self, content: str, meta: Optional[CognitiveMeta] = None):
        self.content = content
        self.meta = meta or self._analyze_content()
        self.fragment_id = self._generate_id()
    
    def _analyze_content(self) -> CognitiveMeta:
        """Analizza il contenuto per estrarre pattern cognitivi."""
        # Calcolo della complessità basata su vari fattori
        complexity = len(self.content.split('\n')) * 0.1
        
        # Calcolo dell'entropia del contenuto
        entropy = sum([
            -p * log2(p) 
            for p in self._char_frequencies().values() 
            if p > 0
        ])
        
        # Identificazione pattern nel contenuto
        patterns = [
            'struttura' if 'class' in self.content else None,
            'funzione' if 'def' in self.content else None,
            'modello' if 'model' in self.content else None
        ]
        patterns = [p for p in patterns if p]
        
        return CognitiveMeta(
            timestamp=datetime.now(),
            patterns=patterns,
            complexity=complexity,
            entropy=entropy,
            connections=[]
        )
    
    def _char_frequencies(self) -> dict[str, float]:
        """Calcola le frequenze dei caratteri nel contenuto."""
        total = len(self.content)
        return {
            char: self.content.count(char) / total
            for char in set(self.content)
        }
    
    def _generate_id(self) -> str:
        """Genera un ID unico basato sul contenuto e metadati."""
        content_hash = hashlib.sha256(
            self.content.encode('utf-8')
        ).hexdigest()
        return f"fragment_{content_hash[:8]}"
    
    def connect_to(self, other: 'CognitiveFragment') -> None:
        """Stabilisce una connessione con un altro frammento."""
        if other.fragment_id not in self.meta.connections:
            self.meta.connections.append(other.fragment_id)
            other.meta.connections.append(self.fragment_id)
    
    def to_json(self) -> str:
        """Serializza il frammento in formato JSON."""
        return json.dumps({
            'id': self.fragment_id,
            'content': self.content,
            'meta': {
                'timestamp': self.meta.timestamp.isoformat(),
                'patterns': self.meta.patterns,
                'complexity': self.meta.complexity,
                'entropy': self.meta.entropy,
                'connections': self.meta.connections
            }
        }, indent=2)
`,
      "file_type": "python",
      "patterns": "struttura oggettuale,funzione computazionale,modello cognitivo",
      "size": 2048
    },
    {
      "id": 1,
      "title": "Pattern cognitivo iniziale",
      "timestamp": "2024-03-20T10:00:00Z",
      "source": {
        "repo": "https://github.com/fabriziosalmi/unuseful",
        "path": "scripts/archivist.py",
        "keyword": "pattern"
      },
      "content": `"""
# Frammento 0001
# Titolo: Pattern cognitivo iniziale
# Origine: https://github.com/fabriziosalmi/unuseful
# Data: 2024-03-20T10:00:00Z
"""

class PatternCognitivo:
    """Una classe che rappresenta un pattern cognitivo di base."""
    
    def __init__(self, nome: str, tipo: str):
        self.nome = nome
        self.tipo = tipo
        self.connessioni = []
    
    def aggiungi_connessione(self, altro_pattern: 'PatternCognitivo') -> None:
        """Stabilisce una connessione con un altro pattern cognitivo."""
        if altro_pattern not in self.connessioni:
            self.connessioni.append(altro_pattern)
            altro_pattern.aggiungi_connessione(self)
    
    def analizza_struttura(self) -> dict:
        """Analizza la struttura del pattern e le sue connessioni."""
        return {
            'nome': self.nome,
            'tipo': self.tipo,
            'num_connessioni': len(self.connessioni),
            'patterns_collegati': [p.nome for p in self.connessioni]
        }

def crea_rete_patterns(patterns: list[tuple[str, str]]) -> list[PatternCognitivo]:
    """Crea una rete di patterns cognitivi interconnessi."""
    oggetti = [PatternCognitivo(nome, tipo) for nome, tipo in patterns]
    
    # Crea connessioni tra patterns adiacenti
    for i in range(len(oggetti) - 1):
        oggetti[i].aggiungi_connessione(oggetti[i + 1])
    
    return oggetti`,
      "file_type": "python",
      "patterns": "struttura oggettuale,funzione computazionale",
      "size": 1024
    }
  ]
};
