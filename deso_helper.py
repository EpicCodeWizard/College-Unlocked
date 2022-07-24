import deso
import os

desoMedia = deso.Media(publicKey=os.environ["publicKey"], seedHex=os.environ["seedHex"])

def upload_to_deso(openFile):
  urlResponse = desoMedia.uploadImage([("file", (openFile.name, openFile, "image/png"))])
  return urlResponse.json()["ImageURL"]
