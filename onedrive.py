import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer

redirect_uri = "http://localhost:8080/"
client_secret = "hjn1KomCF6NzabEQ6Ockpxpm2v5Zlg4q"

client = onedrivesdk.get_default_client(client_id='0000000040177DE9',
                                        scopes=['wl.signin',
                                                'wl.offline_access',
                                                'onedrive.readwrite'])

auth_url = client.auth_provider.get_auth_url(redirect_uri)

#this will block until we have the code
code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

client.auth_provider.authenticate(code, redirect_uri, client_secret)

#upload
returned_item = client.item(drive="me", id="root").children["newfile.txt"].upload("./path_to_file.txt")

#download
root_folder = client.item(drive="me", id="root").children.get()
id_of_file = root_folder[0].id

client.item(drive="me", id=id_of_file).download("./path_to_download_to.txt")

