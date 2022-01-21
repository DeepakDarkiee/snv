import codecs
import hashlib
import hmac


def generate_signature(payload, key):
    signature = (
        hmac.new(
            codecs.encode(key),
            msg=codecs.encode(str(payload)),
            digestmod=hashlib.sha256,
        )
        .hexdigest()
        .lower()
    )

    print(signature)
    return signature
