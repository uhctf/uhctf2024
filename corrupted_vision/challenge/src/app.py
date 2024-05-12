import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from flask import Flask, request, redirect, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

FLAG = "uhctf{t0-x0r-0r-n0t-t0-x0r-2a32aa}"
DEFAULT_USERNAME = "guest"
KEY = "K6nBABRs3tjPV0ib"

# adapted from https://stackoverflow.com/questions/12524994/encrypt-and-decrypt-using-pycrypto-aes-256
class AESCipher(object):
    def __init__(self):
        self.bs = AES.block_size
        self.key = hashlib.sha256(KEY.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.urlsafe_b64encode(iv + cipher.encrypt(raw.encode("ascii"))).decode("ascii")

    def decrypt(self, enc):
        # adding "=" to prevent padding issues. Let's be kind to our players
        enc = base64.urlsafe_b64decode(enc + "===")
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size:])).decode("ascii", errors="backslashreplace")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

app = Flask(__name__)
aes_cipher = AESCipher()
nth_visitor = 32 # just to make it seem more lively
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["3 per second"],
    storage_uri="memory://",
)

def increment_guest_visitor_nr():
    global nth_visitor
    # increment by number in range 1..=8
    nth_visitor = nth_visitor + (ord(Random.new().read(1)) % 8) + 1
    # wrap at some point, but never back to 0 to prevent accidental solves
    nth_visitor = (nth_visitor % 4096) + 32
    return nth_visitor

@app.route('/', methods=["GET"])
def index_route():
    visitor_nr = increment_guest_visitor_nr()

    global aes_cipher
    user_data = aes_cipher.encrypt(f"{DEFAULT_USERNAME}&{visitor_nr}")
    return redirect(f"/user?data={user_data}",code=302)

@app.route('/user', methods=["GET"])
def user_route():
    user_data = request.args.get("data", type = str)
    user_data = aes_cipher.decrypt(user_data).split("&")

    try:
        user_name = user_data[0]
    except IndexError:
        user_name = ""

    try:
        user_id = int(user_data[1])
    except IndexError:
        user_id = ""
    except ValueError:
        user_id = user_data[1]

    return render_template('index.html', user_name=user_name, user_id=user_id, flag=FLAG)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)