import winsound

def note(key):
    note = 'C:\\Users\\thepe\\Downloads\\'+ key
    winsound.PlaySound(note, winsound.SND_FILENAME)