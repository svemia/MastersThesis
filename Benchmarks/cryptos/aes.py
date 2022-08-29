from Crypto.Cipher import AES as aes
from base64 import b64decode, b64encode
from Crypto.Random import get_random_bytes

from Crypto.Util.py3compat import *


def pad(data_to_pad, block_size, style='pkcs7'):
    padding_len = block_size - len(data_to_pad) % block_size
    if style == 'pkcs7':
        padding = bchr(padding_len) * padding_len
    elif style == 'x923':
        padding = bchr(0) * (padding_len - 1) + bchr(padding_len)
    elif style == 'iso7816':
        padding = bchr(128) + bchr(0) * (padding_len - 1)
    else:
        raise ValueError("Unknown padding style")
    return data_to_pad + padding


def unpad(padded_data, block_size, style='pkcs7'):
    pdata_len = len(padded_data)
    if pdata_len % block_size:
        raise ValueError("Input data is not padded")
    if style in ('pkcs7', 'x923'):
        padding_len = bord(padded_data[-1])
        if padding_len < 1 or padding_len > min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if style == 'pkcs7':
            if padded_data[-padding_len:] != bchr(padding_len) * padding_len:
                raise ValueError("PKCS#7 padding is incorrect.")
        else:
            if padded_data[-padding_len:-1] != bchr(0) * (padding_len - 1):
                raise ValueError("ANSI X.923 padding is incorrect.")
    elif style == 'iso7816':
        padding_len = pdata_len - padded_data.rfind(bchr(128))
        if padding_len < 1 or padding_len > min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if padding_len > 1 and padded_data[1 - padding_len:] != bchr(0) * (padding_len - 1):
            raise ValueError("ISO 7816-4 padding is incorrect.")
    else:
        raise ValueError("Unknown padding style")
    return padded_data[:-padding_len]


class AES:
    _modes = {"ecb": aes.MODE_ECB, "cbc": aes.MODE_CBC, "ofb": aes.MODE_OFB, "cfb": aes.MODE_CFB, "ctr": aes.MODE_CTR}

    def __init__(self, key_size: int, mode: str):
        self.key_size = int(key_size / 8)
        self.mode = mode
        self.init_vector = get_random_bytes(aes.block_size)
        self.key = get_random_bytes(self.key_size)

    def _create_aes(self):
        if self.mode in ["cbc", "ofb", "cfb"]:
            new_aes = aes.new(key=self.key, mode=self._modes[self.mode], iv=self.init_vector)
        elif self.mode == "ctr":
            new_aes = aes.new(key=self.key, mode=self._modes[self.mode], nonce=b"")
        else:
            new_aes = aes.new(key=self.key, mode=self._modes[self.mode])

        return new_aes

    def encrypt(self, message):
        if isinstance(message, str):
            msg = message.encode("utf8")
        else:
            msg = message
        msg = pad(msg, aes.block_size)
        new_aes = self._create_aes()
        enc_msg = new_aes.encrypt(msg)

        return b64encode(enc_msg)

    def decrypt(self, message):
        msg = b64decode(message)
        new_aes = self._create_aes()
        dec_msg = new_aes.decrypt(msg)

        return unpad(dec_msg, aes.block_size)
