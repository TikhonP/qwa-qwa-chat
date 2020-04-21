from Crypto.Cipher import AES # алгоритм шифрования
from Crypto.Hash import SHA512 # Для хеширования данных используем также популярный алгоритм SHA.
from Crypto.Hash import MD5 # Этот алгоритм хеширования будет использован для приведения произвольной строки пароля к 32 битной
from Crypto import Random


def transform_password(key):
    """Transform the password string into 32 bit MD5 hash

    :param password_str: <str> password in plain text;
    :return: <str> Transformed password fixed length

    """
    h = MD5.new()
    h.update(key.encode())
    return h.hexdigest()

def symmetric_encrypt(message, key, verbose = False):
    """Encripts the message using symmetric AES algorythm.

    :param message: <str> Message for encryption;
    :param key: <object> symmetric key;
    :return: <object> Message encrypted with key

    """

    key_MD5 = transform_password(key) # Приводим произвольный пароль к длине 32 бита
    message_hash = SHA512.new(message.encode())
    message_with_hash = message.encode() + message_hash.hexdigest().encode() #Добавим в конец сообщения его хеш. он понадобится нам при расшифровки
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key_MD5, AES.MODE_CFB, iv) # Создаем объект с заданными параметрами. AES.MODE_CFB - надежный режим шифрования, который предполагает наличие вектора инициализации iv. https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.blockalgo-module.html#MODE_CFB
    encrypted_message = iv + cipher.encrypt(message_with_hash) # Включаем случайную последовательность в начало шифруемого сообщения. Это необходимо, чтобы в случае кодирования нескольких блоков текста, аналогичные блоки не давали одинаковые кодированные сообщения.
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
    dsize = SHA512.digest_size*2

    iv = Random.new().read(bsize)
    cipher = AES.new(key_MD5, AES.MODE_CFB, iv)
    decrypted_message_with_hesh = cipher.decrypt(encr_message)[bsize:] # Извлекаем из блока случайные символу, которые мы добавляли при шифровании
    decrypted_message = decrypted_message_with_hesh[:-dsize] # Извлекаем хеш сообщения, который мы присоединяли при шифровании
    digest = SHA512.new(decrypted_message).hexdigest() # хеш расшифрованной части сообщения. Он будет сравниваться с хешем, который мы присоединили при шифровании.

    if digest==decrypted_message_with_hesh[-dsize:].decode(): # Если хеш расшифровааного сообщения и хеш, который мы добавили при шифровании равны, расшифровка правильная
        if verbose:
            print(f"Success!\nEncrypted hash is {decrypted_message_with_hesh[-dsize:].decode()}\nDecrypted hash is {digest}")
        return decrypted_message.decode()
    else:
        print(f"Encryption was not correct: the hash of decripted message doesn't match with encrypted hash\nEncrypted hash is {decrypted_message_with_hesh[-dsize:]}\nDecrypted hash is {digest}")
