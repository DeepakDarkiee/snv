import codecs
import hashlib
import hmac

payloadAsString = {
    "image": {
        "context": "document-front",
        "content": "/media/document/Screenshot_from_2021-08-05_14-16-56.png",
        "timestamp": "2019-10-29T06:30:25.597Z",
    }
}
signature = (
    hmac.new(
        codecs.encode("5e601361-a800-4164-a30e-e6363cf4a26e"),
        msg=codecs.encode(str(payloadAsString)),
        digestmod=hashlib.sha256,
    )
    .hexdigest()
    .lower()
)

print(signature)
