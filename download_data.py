"""
从阿里云 OSS 下载数据
"""
import os
import oss2
from dotenv import load_dotenv

def download_from_oss():
    """从 OSS 下载 data 目录"""
    load_dotenv()

    # 检查 OSS 是否启用
    if os.getenv('OSS_ENABLED', 'false').lower() != 'true':
        print("OSS 未启用，跳过下载")
        return False

    # OSS 配置
    access_key_id = os.getenv('ALIYUN_ACCESS_KEY_ID')
    access_key_secret = os.getenv('ALIYUN_ACCESS_KEY_SECRET')
    endpoint = os.getenv('ALIYUN_OSS_ENDPOINT')
    bucket_name = os.getenv('ALIYUN_OSS_BUCKET')
    prefix = os.getenv('OSS_PREFIX', 'cloud-price-index')

    if not all([access_key_id, access_key_secret, endpoint, bucket_name]):
        print("OSS 配置不完整")
        return False

    print(f"连接 OSS: {bucket_name}")
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # 下载 data 目录
    data_prefix = f"{prefix}/data/"
    os.makedirs('data', exist_ok=True)

    print(f"开始下载: {data_prefix}")
    for obj in oss2.ObjectIteratorV2(bucket, prefix=data_prefix):
        if obj.key.endswith('/'):
            continue

        # 本地路径
        local_path = obj.key.replace(data_prefix, 'data/')
        local_dir = os.path.dirname(local_path)

        if local_dir:
            os.makedirs(local_dir, exist_ok=True)

        print(f"下载: {obj.key} -> {local_path}")
        bucket.get_object_to_file(obj.key, local_path)

    print("下载完成！")
    return True

if __name__ == '__main__':
    download_from_oss()
