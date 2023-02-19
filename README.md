# fastcampus_video_crawling
The program used to download videos purchased from fastcampus.

본 코드는 2가지 파트로 구성되어 있습니다. 
 - Selenium 으로 강의 목록을 추출하여 Excel로 저장하는 부분(ext_lecture_info.py)
 - 저장된 Excel 파일을 이용하여 영상을 다운받는 부분(download_mp4.py)

각 part는 설정을 입력하는 config(.yaml) 파일을 가지고 있다.  

# Part 1. ext_lecture_info.py 

이 파일에서는 강의의 정보와 영상 링크를 추출한다. 
해당 작업은 selenium 으로 진행되기 때문에, 본인의 chrome 버전에 맞는 [chromedriver.exe](https://chromedriver.chromium.org/downloads) 를 다운받아야 한다.


## config
첫번째 파트의 config는 총 3가지로 구성된다.
- `user_email`: fastcampus의 User ID
- `user_password`: fastcampus의 User Password
- `lecture_url`: 강의 시청 링크. ex) 'https://fastcampus.co.kr/courses/000000/clips/'
  
## run 
위 config를 채우고 ext_lecture_info.py 를 실행하면 된다. 

```python3 ext_lecture_info.py```

해당 프로그램이 다 돌아가면 `result.xlsx` 파일이 생성된다. 


# Part 2. download_mp4.py

본 파트에서는 `result.xlsx` 파일로 추출된 정보를 이용하여 mp4 파일을 다운로드한다.

## config

총 2가지의 config로 구성된다. 
- `n_thread`: 다운받을 thread 수.
- `save_dir`: 강의 영상을 저장할 폴더.

## run

```python3 download_mp4.py``` 

