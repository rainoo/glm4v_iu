import base64
import json
import os

from log import set_global_logger
from zhipuai import ZhipuAI

logger = set_global_logger(console_level="INFO")
client = ZhipuAI(api_key="your api key")
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg')

def image_description(input_path, output_data_path, params):
    all_files = [os.path.join(root, file) for root, dirs, files in os.walk(input_path) for file in files if file.lower().endswith(IMAGE_EXTENSIONS)]
    
    total_files = len(all_files)
    processing_failure_files = 0
    
    for index, file_path in enumerate(all_files, start=1):
        rel_path = os.path.relpath(file_path, input_path)
        output_dir = os.path.dirname(os.path.join(output_data_path, rel_path))
        os.makedirs(output_dir, exist_ok=True)

        if total_files <= 20 or index % 20 == 0 or index in [1, total_files]:
            logger.info(f"Processing {index}/{total_files}: {file_path}", extra={"event_type": "EventType.METRICS", "total files": total_files,  "current": index})
        
        try:
            with open(file_path, 'rb') as img_file:
                img_base = base64.b64encode(img_file.read()).decode('utf-8')
            response = client.chat.completions.create(
                model="glm-4v-plus",
                messages=[
                  {
                    "role": "user",
                    "content": [
                      {
                        "type": "image_url",
                        "image_url": {
                            "url": img_base
                        }
                      },
                      {
                        "type": "text",
                        "text": "请描述这个图片"
                      }
                    ]
                  }
                ]
            )
            image_description = response.choices[0].message.content

            # 构建JSON对象
            data = {
                "markResult": {
                    "type": "FeatureCollection",
                    "imageResult": {
                        "content": {
                            "prompt": image_description
                        }
                    }
                }
            }

            base_file_name = os.path.basename(file_path)  # 获取文件名（包含后缀）
            base_file_name_without_ext, _ = os.path.splitext(base_file_name)  # 去除后缀
            json_file_name = f"{base_file_name_without_ext}.json"  # 拼接JSON文件名
            json_file_path = os.path.join(output_dir, json_file_name)  # 生成完整的JSON文件路径

            # 将JSON对象写入文件
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            logger.error(f"Error processing file {file_path}", extra={"event_type": "EventType.TASK_CRASHED"}, exc_info=True)
            create_error_csv(file_path)
            processing_failure_files += 1

    logger.info(f"All images were processed, success {total_files - processing_failure_files} file(s), failure {processing_failure_files} file(s).", extra={"event_type": "METRICS"})


def create_error_csv(filePath, error_dir="/output/info/"):

    os.makedirs(error_dir, exist_ok=True)
    error_file_name = os.path.join(error_dir, "error.csv")

    with open(error_file_name, "a", encoding="utf-8") as f:
        f.write(filePath + "\n")