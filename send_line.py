import requests

# 아래 값은 임시 키 입니다.
key = "UGWTRR8IzlArM6mxD3n1i1NnLqmWaMHHA4TRM46G0Is"

def send_line(msg=None, imgfile=None):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {key}"  # YOUR_ACCESS_TOKEN을 실제 토큰으로 변경해주세요
    }

    if msg is not None and imgfile is not None:
        message = msg
        files = {
            "imageFile": open(imgfile, "rb")  # 전송할 이미지 파일의 경로
        }
        payload = {
            "message": message
        }
        response = requests.post(url, headers=headers, params=payload, files=files)
    elif msg is not None:
        message = msg
        payload = {
            "message": message
        }
        response = requests.post(url, headers=headers, params=payload)
    elif imgfile is not None:
        files = {
            "imageFile": open(imgfile, "rb")  # 전송할 이미지 파일의 경로
        }
        payload = {
            "message": imgfile
        }
        response = requests.post(url, headers=headers, params=payload, files=files)
    else:
        print("메시지 및 파일이 제공되지 않아 경고 알림 전송을 수행할 수 없습니다.")
        return


    if response.status_code == 200:
        print("메시지가 성공적으로 전송되었습니다.")
    else:
        print(f"메시지 전송에 실패하였습니다. 응답 코드: {response.status_code}")

if __name__ == "__main__":
    msg = "테스트 메시지"
    imgfile_path = "./TEST.PNG"

    # 메시지만 보내고 싶을때
    send_line(msg=msg)

    # 이미지만 보내고 싶을때
    send_line(imgfile=imgfile_path)

    # 텍스트와 이미지를 같이 보내고 싶을때
    send_line(msg=msg, imgfile=imgfile_path)