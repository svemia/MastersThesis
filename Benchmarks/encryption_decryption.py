from cryptos import aes, rsa

aes_keys = [128, 196, 256]
modes = ["ecb", "cbc", "ofb", "cfb", "ctr"]
rsa_keys = [1024, 2048]

crypt_id = {1: aes.AES,
            2: rsa.RSA}


def main():
    msg = "Don't tell anyone I told you this."

    print("=============================================================================================")
    print("Message that will be encrypted: {msg}".format(msg=msg))
    print("=============================================================================================")

    # 1 -> AES, 2 -> RSA
    type_cry = 2

    results = {"original message": msg,
               "algorithm": None,
               "key size": None,
               "mode": None,
               "encrypted message": None,
               "decrypted message": None}

    if type_cry == 1:
        # Select key size for AES: 128, 192, or 256.
        key_size = 256
        # Select mode for AES: ecb, cbc, ofb, ctr, or cfb.
        mode = "cbc"

        results["algorithm"] = "AES"
        results["key size"] = str(key_size)
        results["mode"] = mode.upper()

        selected = aes.AES(key_size, mode)
        enc_msg = selected.encrypt(msg)
        dec_msg = selected.decrypt(enc_msg)

        results["encrypted message"] = enc_msg.hex()
        results["decrypted message"] = dec_msg.decode("utf8")

    elif type_cry == 2:

        # Select key size for RSA: 1024 or 2048.
        key_size = 2048

        results["algorithm"] = "RSA"
        results["key size"] = str(key_size)

        selected = rsa.RSA(key_size)
        enc_msg = selected.encrypt(msg)
        dec_msg = selected.decrypt(enc_msg)

        results["encrypted message"] = enc_msg.hex()
        results["decrypted message"] = dec_msg.decode("utf8")

    #for k in results:
    #    print("{key} : {value}".format(key=k, value=results[k]))


if __name__ == '__main__':
    #main()
    for i in range(20):
        main()
