import requests
import os
import datetime

hhm_api = 'https://h.aaaapp.cn/posts'     # 主页批量提取接口
user_id = 'F87EFB7A648914AD24FB313BB58789BD'         # 这里改成你自己的 userId
secret_key = '150c09abbb832ebad6323283cca62573'      # 这里改成你自己的 secretKey

# 参数
url = 'https://www.tiktok.com/@ntv.news/video/7029479478222380802'

params = {
    'userId': user_id,
    'secretKey': secret_key,
    'url': url
}

r = requests.post(hhm_api, json=params, verify=False)

if r.status_code == 200:
    data = r.json()
    post = data['data']['posts'][0]
    medias = post['medias']
    video_url = medias[0]['resource_url']
    cover_url = medias[0]['preview_url']
    # 获取视频标题
    title = post['text'].strip().replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
    # 创建文件夹
    username = url.split('@')[1].split('/')[0]
    date = datetime.datetime.fromtimestamp(post['create_time']).strftime('%Y-%m-%d_%H-%M-%S')
    folder_name = f'{username}_{date}'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # 下载视频
    video_file = os.path.join(folder_name, f'{title}.mp4')
    with open(video_file, 'wb') as f:
        f.write(requests.get(video_url).content)
    print(f'{title} 的视频下载完成')
    # 下载封面
    cover_file = os.path.join(folder_name, f'{title}.jpg')
    with open(cover_file, 'wb') as f:
        f.write(requests.get(cover_url).content)
    print(f'{title} 的封面下载完成')
    # 保存标题
    title_file = os.path.join(folder_name, f'{title}.txt')
    with open(title_file, 'w', encoding='utf-8') as f:
        f.write(title)
    print(f'{title} 的标题保存完成')
else:
    print("请求失败：", r.status_code)
