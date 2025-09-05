"""
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
    
    return oggetti

# Esempio di utilizzo
patterns_esempio = [
    ('Memoria', 'Struttura'),
    ('Apprendimento', 'Processo'),
    ('Percezione', 'Sensore'),
    ('Ragionamento', 'Computazione')
]

rete = crea_rete_patterns(patterns_esempio)
analisi = [p.analizza_struttura() for p in rete]
print("Analisi della rete di patterns cognitivi:", analisi)
