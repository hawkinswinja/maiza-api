import requests, json, os

def crop_identifier(image_bytes):
        try:
            url = "https://plant.id/api/v3/identification?details=common_names&language=en"
            files = [('image', ('image.jpg', image_bytes, 'image/*'))]
            headers = {'Api-Key': os.getenv('PLANTID_API')}
            response = requests.post(url, headers=headers, files=files)
            result = json.loads(response.text)['result']['is_plant']['binary']
            # print(result)
            return result
        except Exception as e:
            return str(e)