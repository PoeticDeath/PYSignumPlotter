from py_sph_shabal import shabal256

hashsize = 32
scoops = 4096
noncesize = hashsize * scoops * 2

def plot(numid, startnonce, nonces):
    d = numid.to_bytes(8, "big")
    plotfile = [bytearray(nonces * hashsize * 2) for i in range(scoops)]
    for m in range(startnonce, startnonce + nonces):
        n = m.to_bytes(8, "big")
        hashes = bytearray(noncesize + 16)
        hashes[-16:] = d + n
        o = 0
        for i in range(noncesize, 0, -hashsize):
            hashes[i - hashsize:i] = shabal256(bytes(hashes[i:][:scoops]))
        finalhash = shabal256(bytes(hashes))
        for i in range(0, noncesize):
            hashes[i] ^= finalhash[i % hashsize]
        hashes = bytes(hashes[:-16])
        for i in range(scoops):
            plotfile[i][(m - startnonce) * hashsize * 2:(m - startnonce) * hashsize * 2 + hashsize * 2] = hashes[i * hashsize * 2:i * hashsize * 2 + hashsize] + hashes[(scoops - i - 1) * hashsize * 2 + hashsize:(scoops - i - 1) * hashsize * 2 + hashsize * 2]
    return b"".join(plotfile)

if __name__ == "__main__":
    nonce = plot(2134033412466902214, 0, 1)
    print(nonce[:64].hex() == "3e4034594fb43e7ee80ccdda4430600f23bead9579a3981b6d7efe648268c436319dca45dd0e8cf7f730114cf75ef652324da709fb61e50a0bd562cfbdb4b1e3")
