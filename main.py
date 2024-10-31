# -*- encoding: utf-8 -*-
# -------------------------------------------------------
# @File    :   main.py
# @Time    :   2024/10/31 11:02:48
# @Author  :   Gao Yu
# @Version :   1.0
# @Contact :   gaoyu@datatang.com
# @License :   (C)Copyright 2024
# @Desc    :   Image description with zhipuai
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import base64
import glm4v_iu
import json
import os
import sys
import time

from log import set_global_logger
from traceback import format_exc


# 获取WORKINFO参数信息
def get_params():
    # 获取环境变量"WORKINFO"的值
    code = os.environ.get("WORKINFO")
    # 如果获取到了值
    if code:
        # 将code解码为utf-8字符串
        info = base64.b64decode(code).decode("utf-8")
        # 将解码后的字符串解析为JSON对象
        params = json.loads(info)
        # 返回params
        return params
    else:
        # 抛出获取异常
        raise ValueError("Failed to retrieve WORKINFO environment variable.")


def run():

    input_path = "/input"
    output_path = "/output"

    try:
        params = get_params()
        # stage
        stage = params["set"]["stage"]
        # job_name
        job_name = params["set"]["jobName"]

        logger.info(f"{params}", extra={"event_type": "EventType.METRICS", "stage": stage, "job_name": job_name})
    except Exception as e:
        logger.error("get_params error", extra={"event_type": "EventType.TASK_CRASHED"}, exc_info=format_exc())
        sys.exit(-1)

    # 数据存放路径
    output_data_path = os.path.join(output_path, stage)

    # 对input_path下的所有图像进行描述，并将生成的描述以特定的json格式保存到output下目录。
    glm4v_iu.image_description(input_path, output_data_path, params)


if __name__ == "__main__":

    logger = set_global_logger(console_level="INFO")
    starttime = time.time()
    logger.info("TASK_STARTED", extra={"event_type": "TASK_STARTED"})

    run()

    endtime = time.time()
    logger.info("Total Duration Seconds", extra={"event_type": "EventType.METRICS", "Total Duration Seconds": round((endtime - starttime), 3)})
    logger.info("TASK_FINISHED", extra={"event_type": "TASK_FINISHED"})