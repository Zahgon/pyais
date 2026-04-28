
import queue
import typing

from pyais.exceptions import InvalidNMEAMessageException, UnknownMessageException
from pyais.messages import AISSentence, GatehouseSentence, NMEASentence, NMEASentenceFactory
from pyais.stream import TagBlockQueue


class NMEAQueue(queue.Queue[AISSentence]):
    """Assembles complete NMEA sentences.

    Single-line sentences are added to the queue directly. Multi-line sentences
    are buffered until all fragments are available, after which they are added to the queue."""

    def __init__(self, maxsize: int = 0, tbq: typing.Optional[TagBlockQueue] = None) -> None:
        super().__init__(maxsize)
        self.tbq = tbq
        self.buffer: typing.Dict[typing.Tuple[int, str], typing.List[typing.Optional[AISSentence]]] = {}
        self.last_wrapper: typing.Optional[GatehouseSentence] = None

    def __add_to_tbq(self, sentence: NMEASentence) -> None:
        if not self.tbq:
            # Tag Block Queue not defined. Do nothing.
            return
        self.tbq.put_sentence(sentence)

    def put(self, item: object, block: bool = True, timeout: typing.Optional[float] = None) -> None:
        """This method only exists to please mypy. Use put_line instead."""
        raise ValueError('do not call NMEAQueue.put() directly. Use NMEAQueue.put_line() instead!')

    def put_line(self, line: bytes, block: bool = True, timeout: typing.Optional[float] = None) -> None:
        """Put a line of raw bytes, as part of an NMEA sentence, into the queue."""
        pass

    def get_or_none(self) -> typing.Optional[NMEASentence]:
        """Non-blocking helper method to retrieve the last message, if one is available"""
        pass
