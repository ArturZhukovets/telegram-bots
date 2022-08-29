import requests
from config import API_KEY
from PIL import Image
from io import BytesIO
import os

def get_picture(query:str, page:str):
    """Изображение сохраняется при помощи Pillow. В метод open помещается изображение в байтах BytesIO(bites)"""
    headers = {"Authorization": API_KEY}
    params = {"query": query, "per_page": 1}
    for i in range(1, int(page) + 1):
        params['page'] = i
        url = f"https://api.pexels.com/v1/search"

        req = requests.get(url=url, headers=headers, params=params)
        if req.status_code == 200:
            response = req.json()
            image_url = response.get('photos')[0].get('src').get("original")
            get_image = requests.get(image_url)

            image = Image.open(BytesIO(get_image.content))
            if 'media' not in os.listdir():
                os.mkdir('media')
            picture_path:str = f"media/{query}_{i}.{image_url.split('.')[-1]}"
            image.save(picture_path)

    return image




def main():
    query = input("Query: ")
    p = input("Count pages: ")
    get_picture(query, p)


if __name__ == '__main__':
    main()