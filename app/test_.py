import hashlib

from app.utils import decrypt_md5


def test_123():
    g = '123'
    g_hash = hashlib.md5(g.encode('UTF-8')).hexdigest()
    print(g_hash)
    print(decrypt_md5(g_hash))
