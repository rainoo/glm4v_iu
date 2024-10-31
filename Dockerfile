FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.9-alpine

WORKDIR /code

ADD . /code

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["python", "main.py"]

# docker build -t glm4v_iu .
# docker save -o glm4v_iu.tar glm4v_iu
# docker run -e WORKINFO="eyJzcmMiOnsiaW5wdXRQYXRocyI6W3siaW5wdXRQYXRoIjoiL2lucHV0IiwidHlwZSI6IkVYVEVSTkFMIiwiaW5QYXJhbSI6eyJzdG9yZSI6ImxvY2FsIiwiY2x1c3RlcklkIjoiMTQzOCIsImZpbGVUeXBlIjoiMDEiLCJzdG9yZUluZm8iOnt9fX1dfSwidGFyZ2V0IjpbeyJyZXN1bHRQYXRoIjoiL291dHB1dCIsInR5cGUiOiJDbHVzdGVyIiwib3V0UGFyYW0iOnsic3RvcmUiOiJsb2NhbCIsImNsdXN0ZXJJZCI6IjE0MzgiLCJzdG9yZUluZm8iOnt9fX1dLCJzZXQiOnsic3RhZ2UiOiIwMyIsImlvTWFwIjpbXSwibW9kZSI6IiIsImpvYk5hbWUiOiJhaTIwMjQxMDA5MTE1MTQ1IiwiZXhlY1BhcmFtZXRlciI6eyJwcm9jZXNzaW5nX21vZGUiOiJCUklHSFRORVNTIn19fQ==" -v D:\TEST-IN:/input -v D:\TEST-OUT:/output glm4v_iu 