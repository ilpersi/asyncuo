from uo.compression import Compression

test = bytearray([1, 2, 3, 4, 5])
compression = Compression()

comp = compression.compress(test)
decomp = compression.decompress(comp)

if test == decomp:
    print("Success!!")