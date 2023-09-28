import numpy

def create_frame(bytes_: bytes, dimensions) -> numpy.ndarray:
    w, h = dimensions
    array = numpy.reshape(bytearray(bytes_), (h, w, 3))
    return numpy.array([(array/255).astype(numpy.float32)])

def unpack_frame(array: numpy.ndarray) -> bytes:
    return ((numpy.clip(array, 0.0, 1.0))*255).astype(numpy.uint8).tobytes()
