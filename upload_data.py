"""
上传数据到阿里云 OSS
"""
import os
import oss2
from dotenv import load_dotenv

def upload_to_oss(local_dir='data'):
    """上传本地 data 目录到 OSS"""
    load_dotenv()

    # OSS 配置
    access_key_id = os.getenv('ALIYUN_ACCESS_KEY_ID')
    access_key_secret = os.getenv('ALIYUN_ACCESS_KEY_SECRET')
    endpoint = os.getenv('ALIYUN_OSS_ENDPOINT')
    bucket_name = os.getenv('ALIYUN_OSS_BUCKET')
    prefix = os.getenv('OSS_PREFIX', 'cloud-price-index')

    if not all([access_key_id, access_key_secret, endpoint, bucket_name]):
        print("错误: OSS 配置不完整，请检查 .env 文件")
        return False

    print(f"连接 OSS: {bucket_name}")
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # 上传文件
    uploaded = 0
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            oss_path = f"{prefix}/{local_path.replace(os.sep, '/')}"

            print(f"上传: {local_path} -> {oss_path}")
            bucket.put_object_from_file(oss_path, local_path)
            uploaded += 1

    print(f"\n上传完成！共 {uploaded} 个文件")
    return True

if __name__ == '__main__':
    upload_to_oss()
