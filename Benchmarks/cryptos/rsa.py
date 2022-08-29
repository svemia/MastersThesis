from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_OAEP as pkc
from Crypto.Signature import PKCS1_v1_5 as pkc_sig


class RSA:
    _exp = 65537

    def __init__(self, key_size: int):
        self.key_size = key_size
        self.key = rsa.generate(bits=self.key_size, e=self._exp)

    def encrypt(self, message):
        if isinstance(message, str):
            msg = message.encode("utf8")
        else:
            msg = message
        enc_msg = pkc.new(self.key).encrypt(msg)
        return enc_msg

    def decrypt(self, message):
        dec_msg = pkc.new(self.key).decrypt(message)
        return dec_msg

    def sign(self, msg_hash):
        signed = pkc_sig.new(self.key).sign(msg_hash)
        return signed

    def verify(self, msg_hash, signature):
        try:
            pkc_sig.new(self.key).verify(msg_hash, signature)
            return True
        except ValueError:
            return False