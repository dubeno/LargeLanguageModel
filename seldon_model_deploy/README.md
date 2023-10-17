# LargeLanguageModel
模型推理最佳实践

# 编译镜像
docker build . -t docker-model:1.0.0 .

#运行镜像
docker run --rm --name docker-model -p 9000:9000 docker-model:1.0.0

#使用test.py测试推理
