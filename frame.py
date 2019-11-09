class Frame:
    def __init__(self):
        self._FrameInitSeq = None # à définir : séquence de début de trame sur 2 octets
        self._FrameEndSeq = None # à définir : séquence de fin de trame sur 2 octets



# Trame de l'arbitre de bus
class ID_Dat(Frame):
    def __init__(self, _id):
        super().__init__()
        self._FrameType = 'ID-Dat' # On a le type ID-Dat ou RP-Dat sur 1 octet, à voir comment on le définit
        self._Id = _id # sur 2 octets



# Trame de producteur
class RP_Dat(Frame):
    def __init__(self, data):
        super().__init__()
        self._FrameType = 'RP-Dat' # Cf ID_dat._FrameType
        self._Data = data # Données transférées, 128 octets max (taille non fixe)
