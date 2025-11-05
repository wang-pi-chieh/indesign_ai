from pathlib import Path
from reducto import Reducto
import json
import sys

# 從命令列參數接收檔案路徑
if len(sys.argv) < 2:
    print("❌ 請提供 PDF 檔案路徑")
    sys.exit(1)

pdf_path = Path(sys.argv[1])
if not pdf_path.exists():
    print(f"❌ 找不到檔案：{pdf_path}")
    sys.exit(1)

print(f"開始處理：{pdf_path}")

client = Reducto(api_key='dd24a02a63d50994f78206534dc45a6eb45b47a4be6091cef553122ff76dfdd0b005089465e0c75c179ff29cf3648585')
upload = client.upload(file=pdf_path)
# result = client.parse.run(input=upload) # 用預設設定


# 🚀 正確呼叫方式（注意 document_url）
result = client.parse.run(
    input=upload,
    # document_url=upload.file_id,
    enhance= {
        "agentic": [], #   
        "summarize_figures": True
    },
    retrieval= {
            "chunking": {"chunk_mode": "disabled"},
            "filter_blocks": [],  # 
            "embedding_optimized": False
    },
    formatting= {
            "add_page_markers": False,
            "table_output_format": "dynamic",
            "merge_tables": False,
            "include": []
    },
    spreadsheet= {
        "split_large_tables": {"enabled": True, "size": 50},
        "clustering": "accurate", 
        "exclude": []  # 
    },
    settings= {
        "ocr_system": "standard", #   
        "force_url_result": False, #   
        "return_ocr_data": False, 
        "return_images": [], #   
        "embed_pdf_metadata": False, #   
        "timeout": 900,
        "page_range": None,
        
        "document_password": None, #   
        "persist_results": False, # 決定 Reducto 是否要 在伺服器上暫存你的處理結果（方便重複查詢）
        # false（預設） → 結果只存在本次 API 回傳中，用完即刪
        # true → Reducto 會暫時保留結果（幾小時到幾天），讓你用 result_id 再次查詢

        "force_file_extension": None # 強制指文件的副檔名（格式類型）
    }
)

# 輸出 JSON 檔案
# output_path = Path("result.json")

# ✅ 依照原始 PDF 檔名輸出 JSON
output_name = pdf_path.stem + ".json"   # 例如 "第4回_指數與常用對數.pdf" → "第4回_指數與常用對數.json"
output_path = Path("downloads") / output_name
output_path.parent.mkdir(parents=True, exist_ok=True)

result_dict = result.to_dict()

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result_dict, f, ensure_ascii=False, indent=2)

print(f"解析完成！結果已儲存在：{output_path.absolute()}")


