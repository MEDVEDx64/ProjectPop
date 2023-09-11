import numpy

def create_frame(bytes_: bytes, dimensions: (int, int)) -> numpy.ndarray:
    w, h = dimensions
    array = numpy.array(bytes_).reshape((h, w, 3))
    return numpy.array([(array/255).astype(numpy.float32)])

def unpack_frame(array: numpy.ndarray) -> bytes:
    return ((numpy.clip(array, 0.0, 1.0))*255).astype(numpy.uint8).tobytes()