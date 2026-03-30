# -*- coding: utf-8 -*-
# 时间 : 2026/3/30 08:46
# 作者 : mcy
# 文件 : 下载模型.py
# 魔搭下载Embedding模型
from modelscope.hub.snapshot_download import snapshot_download
emb_model_dir = snapshot_download('AI-ModelScope/bge-large-zh-v1.5',
                                  cache_dir='../models')