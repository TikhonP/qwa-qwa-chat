from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto.Hash import MD5
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from hashlib import md5
from Crypto.PublicKey import RSA


def transform_password(key):
    """Transform the password string into 32 bit MD5 hash

    :param password_str: <str> password in plain text;
    :return: <str> Transformed password fixed length

    """
    h = MD5.new()
    h.update(key.encode())
    return h.hexdigest()


def symmetric_encrypt(message, key, verbose=False):
    """Encripts the message using symmetric AES algorythm.

    :param message: <str> Message for encryption;
    :param key: <object> symmetric key;
    :return: <object> Message encrypted with key

    """

    # Приводим произвольный пароль к длине 32 бита
    key_MD5 = transform_password(key)
    message_hash = SHA512.new(message.encode())
    # Добавим в конец сообщения его хеш. он понадобится нам при расшифровки
    message_with_hash = message.encode() + message_hash.hexdigest().encode()
    iv = Random.new().read(AES.block_size)
    # Создаем объект с заданными параметрами. AES.MODE_CFB - надежный режим шифрования, который предполагает наличие вектора инициализации iv. https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.blockalgo-module.html#MODE_CFB
    cipher = AES.new(key_MD5, AES.MODE_CFB, iv)
    # Включаем случайную последовательность в начало шифруемого сообщения. Это необходимо, чтобы в случае кодирования нескольких блоков текста, аналогичные блоки не давали одинаковые кодированные сообщения.
    encrypted_message = iv + cipher.encrypt(message_with_hash)
    if verbose:
        print(f'Message was encrypted into: {encrypted_message.hex()}')
    return encrypted_message


def symmetric_decrypt(encr_message, key, verbose=False):
    """Decripts the message using private_key and check it's hash

    :param encrypted_message: <object> Encrypted message
    :param key: <object> symmetric key;
    :return: <object> Message decripted with key

    """
    key_MD5 = transform_password(key)

    # Размеры боков нужны, для извлечения их из текста
    bsize = AES.block_size
    dsize = SHA512.digest_size * 2

    iv = Random.new().read(bsize)
    cipher = AES.new(key_MD5, AES.MODE_CFB, iv)
    # Извлекаем из блока случайные символу, которые мы добавляли при шифровании
    decrypted_message_with_hesh = cipher.decrypt(encr_message)[bsize:]
    # Извлекаем хеш сообщения, который мы присоединяли при шифровании
    decrypted_message = decrypted_message_with_hesh[:-dsize]
    # хеш расшифрованной части сообщения. Он будет сравниваться с хешем, который мы присоединили при шифровании.
    digest = SHA512.new(decrypted_message).hexdigest()

    # Если хеш расшифровааного сообщения и хеш, который мы добавили при шифровании равны, расшифровка правильная
    if digest == decrypted_message_with_hesh[-dsize:].decode():
        if verbose:
            print(
                f"Success!\nEncrypted hash is {decrypted_message_with_hesh[-dsize:].decode()}\nDecrypted hash is {digest}")
        return decrypted_message.decode()
    else:
        print(
            f"Encryption was not correct: the hash of decripted message doesn't match with encrypted hash\nEncrypted hash is {decrypted_message_with_hesh[-dsize:]}\nDecrypted hash is {digest}")


def encrypt_message(message, public_key):
    """Encripts the message using public_key.

    :param message: <str> Message for encryption
    :param public_key: <object> public_key
    :param verbose: <bool> Print description;
    :return: <object> Message encrypted with public_key

    """
    public_key = RSA.importKey(public_key)
    message_hash = SHA512.new(message.encode())
    cipher = PKCS1_OAEP.new(public_key)
    checksum = md5(message).hexdigest()
    encrypted_message = (cipher.encrypt(message.encode())).hex()

    return encrypted_message, checksum


def decrypt_message(encrypted_message, private_key, checksum):
    """Decripts the message using private_key and check it's hash

    :param encrypted_message: <object> Encrypted message
    :param private_key: <object> private_key
    :return: <object> Message decripted with private_key

    """
    private_key = RSA.importKey(private_key)
    encrypted_message = bytearray.fromhex(encrypted_message)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = (cipher.decrypt(encrypted_message)).decode()
    if checksum == md5(decrypted_message).hexdigest():
        return 0, decrypted_message
    else:
        return 2, "ChecksumWasInvalidCanDecrypt"


def generate_keys(rsa_bits=2048):
    private_key = RSA.generate(rsa_bits)
    public_key = private_key.publickey()
    sprivate_key = str(private_key.exportKey("PEM"))
    spublic_key = str(public_key.exportKey("PEM"))
    return sprivate_key, spublic_key
