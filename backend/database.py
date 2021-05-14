import random
import string


def fetch_from_database(conn, key):
    """Get the image and LaTeX which is stored in the database, from the given key"""
    cur = conn.cursor()
    cur.execute("SELECT image, latex FROM Images WHERE id=(%s)", (key,))
    data = cur.fetchone()
    cur.close()
    return data


key_letters = string.ascii_letters + string.digits + "+-"


def random_key(length=8):
    """Create a random key of the given length.

    The key is a sequence of letters, numbers, and +/-.
    """
    return "".join(random.choice(key_letters) for _ in range(length))


def key_in_use(cur, key):
    """Returns true iff the given key is already in the database"""
    cur.execute("SELECT COUNT(*) FROM Images WHERE id=(%s)", (key,))
    count = cur.fetchone()
    return count[0] != 0


def insert_into_database(conn, image, latex):
    """Insert the image and latex into the database, and return its key"""
    cur = conn.cursor()
    key = random_key()
    while key_in_use(cur, key):
        key = random_key()
    # Note: It's possible for two threads to insert the same key at the same time
    # But that's not worth fixing for the class project, because usage will be low
    # and the number of possible keys makes collisions unlikely
    # The odds of a collision with two concurrent inserts are about 1 in 250 trillion.
    cur.execute(
        "INSERT INTO Images (id, image, latex) VALUES (%s, %s, %s)", (key, image, latex)
    )
    conn.commit()
    cur.close()
    return key


def encode_hex(f):
    """Takes a binary file and converts it into a hex-encoded string, in
    the format used by PostreSQL.
    """
    output = "\\x"
    while (byte := f.read(1)) :
        hex_byte = hex(ord(byte))[2:]
        if len(hex_byte) % 2 == 1:
            hex_byte = "0" + hex_byte
        output += hex_byte
    return output
