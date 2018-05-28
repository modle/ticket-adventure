import os, tempfile, sys
from subprocess import call

EDITOR = os.environ.get('EDITOR','vim') #that easy!

def open_editor(initial_message):

    encoded_message = bytes(initial_message, 'utf-8')

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(encoded_message)
        tf.flush()
        call([EDITOR, tf.name])

        tf.seek(0)
        edited_message = tf.read()
        return (edited_message.decode("utf-8"))
