from Crypto.Cipher import AES
from Crypto.Util.number import * 
p = 193387944202565886198256260591909756041
k = 4470735776084208177429085432176719338


flag = 0xb3669dc657cef9dc17db4de5287cd1a1e8a48184ed9746f4c52d3b9f8186ec046d6fb1b8ed1b45111c35b546204b68e0
flag = long_to_bytes(flag) 
while k<p:
    aes = AES.new(long_to_bytes(k), AES.MODE_CBC, b'\0'*16)
    plaintext = aes.decrypt(flag)
    print(plaintext)
    k += (p-1)//4 
# rwctf{Singular_Elliptic_Curve_is_easy_to_break}
