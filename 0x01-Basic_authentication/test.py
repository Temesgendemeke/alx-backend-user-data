import base64

text_data = "temesgen"
print("text_data: ", text_data)
text_byte = text_data.encode("utf-8")
print("text_byte: ", text_byte)

base64_byte = base64.b64encode(text_byte)

print("base64_byte: ", base64_byte)

decode_base64_byte = base64.b64decode(base64_byte).decode("utf-8")

print("decode_base64_byte: ", decode_base64_byte)