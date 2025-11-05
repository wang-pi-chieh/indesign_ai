from pathlib import Path
from reducto import Reducto
import json   # 匯入 JSON 模組

client = Reducto(api_key='dd24a02a63d50994f78206534dc45a6eb45b47a4be6091cef553122ff76dfdd0b005089465e0c75c179ff29cf3648585')
upload = client.upload(file=Path("123.pdf"))
result = client.parse.run(input=upload)

# print(result)

# 將結果輸出成 JSON 檔案
output_path = Path("result.json")




# 將結果轉成字典格式
result_dict = result.to_dict()

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result_dict, f, ensure_ascii=False, indent=2)

print(f"✅ 解析完成！結果已儲存在：{output_path.absolute()}")