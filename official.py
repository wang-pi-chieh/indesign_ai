from pathlib import Path
from reducto import Reducto

client = Reducto(api_key='dd24a02a63d50994f78206534dc45a6eb45b47a4be6091cef553122ff76dfdd0b005089465e0c75c179ff29cf3648585')
upload = client.upload(file=Path("123.pdf"))
result = client.parse.run(input=upload)

print(result)