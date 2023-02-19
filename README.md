# fastcampus_video_crawling
The program used to download videos purchased from fastcampus.

The code consists of two parts.
 - Extracts the list of lectures with Selenium and saves them in Excel(ext_lecture_info.py)
 - Download videos using Excel files(download_mp4.py)

Each part has a config file(.yaml).  

# Part 1. ext_lecture_info.py 

In this part, information and video links from the lecture are extracted.

Since this is done in selenium, you need to download [chromedriver.exe](https://chromedriver.chromium.org/downloads) for your chrome version.


## config
The config of the first part consists of three args.
- `user_email`: User ID
- `user_password`: User Password
- `lecture_url`: Lecture links ex) 'https://fastcampus.co.kr/courses/000000/clips/'
  
## run 
Fill in the config above and run ext_lecture_info.py.

```python3 ext_lecture_info.py```

When the program runs out, `result.xlsx` file is created. 


# Part 2. download_mp4.py

In this part, video files are downloaded using the information extracted from the 'result.xlsx' file.

## config

The config of the second part consists of two args.
- `n_thread`: Number of threads to download videos
- `save_dir`: Folder you want to store the lecture videos.

## run

```python3 download_mp4.py``` 

