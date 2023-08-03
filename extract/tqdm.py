
import io

from tqdm import tqdm


class tqdm_file(io.RawIOBase):
    """Wrap file with tqdm.

    Does only handle monotonic traversal. Seeking is not supported.

    Example:
        Uncompressed size for GZip files is unknown. It is useful to show a
        progress during processing, even if it is based on the compressed size:
        
        >>> import io
        ... import gzip
        ...
        ... with io.open("data.gz", "rb") as compressed_file:
        ...
        ...     size = compressed_file.seek(0, io.SEEK_END)
        ...     compressed_file.seek(0)
        ...
        ...     with tqdm_file(compressed_file, total=size, unit="B", unit_scale=True, unit_divisor=1024) as wrapped_compressed_file:
        ...         with gzip.open(wrapped_compressed_file) as file:
        ...             file.read()
    
    """

    def __init__(self, file, tqdm_func=tqdm, **kwargs):
        self.file = file
        self.tqdm = tqdm_func(**kwargs)

    def readable(self):
        return True

    def read(self, size=-1):
        result = self.file.read(size)
        if result:
            self.tqdm.update(len(result))
        return result

    def readinto(self, buffer):
        size = self.file.readinto(buffer)
        if size:
            self.tqdm.update(size)
        return size

    def tell(self):
        return self.tqdm.n

    def close(self):
        self.tqdm.close()
        self.file.close()
        super().close()
