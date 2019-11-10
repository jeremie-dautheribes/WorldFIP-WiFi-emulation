import struct


class Frame:
    DEFAULT_INIT_SEQUENCE = 42  # à définir : séquence de début de trame sur 2 octets
    DEFAULT_END_SEQUENCE = 42  # à définir : séquence de fin de trame sur 2 octets

    def __init__(self):
        self._FrameInitSeq = self.DEFAULT_INIT_SEQUENCE
        self._FrameEndSeq = self.DEFAULT_END_SEQUENCE

    def get_repr(self):
        raise NotImplementedError('A frame must implement a binary *representation*')


class ID_Dat(Frame):
    '''
    Trame envoyée par l'arbitre de bus pour indiqué l'objet à transmettre
    '''
    ID_Dat = b'I'

    def __init__(self, _id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._FrameType = ID_Dat
        self._Id = _id

    def get_repr(self):
        fmt = 'hchc'
        vals = (self._FrameInitSeq, self._FrameType, self._Id, self._FrameEndSeq)
        return struct.pack(fmt, *vals)


class RP_Dat(Frame):
    '''
    Trame envoyée par les producteur en réponse à une trame ID_Dat
    '''
    RP_Dat = b'D'

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._FrameType = RP_Dat
        self._Data = data  # Données transférées, 128 octets max (taille non fixe)

    def get_repr(self):
        n = 128
        fmt = f'hc{n}sc'
        vals = (self._FrameInitSeq, self._FrameType, self._Data, self._FrameEndSeq)
        return struct.pack(fmt, *vals)
