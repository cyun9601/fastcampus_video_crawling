from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modules.tree import *
from modules.general import Class_id
from modules.utils import load_config

def click_processing_dialog(driver, element, wait_time=2):
    element.click()
    process_dialog(driver, wait_time)
    
def process_dialog(driver, wait_time = 2):
    try :
        driver.implicitly_wait(wait_time)
        dialog = driver.find_element(By.XPATH, value = f"//aside[@class='{Class_id.Dialog_Class_id}']")
        dialog.find_element(By.XPATH, value = f"//button[contains(text(), '처음부터 보기')]").click()
    except: 
        pass

def lecture_info_collect(driver, lecture_elements, parent_node):
    for lecture_seq, lecture_element in enumerate(lecture_elements):
            
        lecture_title = lecture_element.find_element(by=By.CLASS_NAME, value=Class_id.Lecture_Text_Class_id).text
        
        click_processing_dialog(driver, lecture_element)
        driver.implicitly_wait(3)
        iframe_element = driver.find_element(by=By.XPATH, value = f"//iframe[@class='{Class_id.Iframe_Class_id}']")

        ## iframe driver switch
        driver.switch_to.frame(iframe_element)
        
        ## video element에서 src 추출
        video_element = driver.find_element(by=By.XPATH, value = f"//video[@class='{Class_id.Video_Class_id}']")
        video_src = video_element.get_attribute('src')
        
        ## default driver로 switch
        driver.switch_to.default_content()
        
        ## Data 생성 
        # lecture = Lecture(title = classroom_title, part = part_title, lecture=lecture_title, url = url)    
        LectureNode(lecture_seq, lecture_title, video_src, parent=parent_node)

import os 
if __name__== "__main__":
    wait_time = 5
    
    PRJ_DIR = os.path.dirname(os.path.realpath(__file__))

    # config 
    CONFIG_PATH = os.path.join(PRJ_DIR, 'config/lecture.yaml')
    args = load_config(CONFIG_PATH)

    # Selenium 설정
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(executable_path="./Chrome/chromedriver.exe", options = options)
    action = webdriver.ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    # Fastcampus.co.kr 접속 
    try: 
        driver.get("https://fastcampus.co.kr/")
        driver.maximize_window() ## 창 최대화
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sign-links__link')))
    except: 
        print('Fastcampus.co.kr 접속 실패')

    ## login 버튼 클릭
    try: 
        driver.find_element(By.CLASS_NAME, 'sign-links__link').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "이메일로 회원가입")]')))
    except: 
        print('login 버튼 클릭 실패')

    # Login 
    try: 
        ## ID/PASSWORD 입력
        driver.find_element(By.ID, 'user-email').send_keys(args.user_email)
        driver.find_element(By.ID, 'user-password').send_keys(args.user_password)
        driver.implicitly_wait(1)
        
        ## 로그인 
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, Class_id.Login_Class_id)))
        driver.find_element(By.CLASS_NAME, Class_id.Login_Class_id).click()
    except: 
        print('ID/PASSWORD 입력 실패')
    driver.implicitly_wait(wait_time)
    
    # 강의 페이지 이동 
    while True: 
        driver.get(args.lecture_url)
        driver.implicitly_wait(wait_time)
        if driver.current_url == args.lecture_url:
            break
    
    driver.implicitly_wait(10)
    process_dialog(driver, wait_time = wait_time)
    # wait.until(EC.element_to_be_clickable((By.CLASS_NAME, Class_id.Iframe_Button_Class_id)))
    driver.implicitly_wait(wait_time)
    
    # Part 개수 탐색
    print('Part 개수 탐색 중 ...')
    Part_elements = driver.find_elements(by=By.CLASS_NAME, value=Class_id.Part_Class_id)
    while len(Part_elements) == 0:
        Part_elements = driver.find_elements(by=By.CLASS_NAME, value=Class_id.Part_Class_id)
    print("Part_elements : ", Part_elements)

    # 강의명 추출
    classroom_title = driver.find_element(By.CLASS_NAME, value = Class_id.Classroom_Class_id).text

    # 전체 트리 형성
    class_node = ClassroomNode(args.lecture_url, classroom_title)

    try : 
        for part_seq, part_element in enumerate(Part_elements): 
            
            ## Part Text 추출 
            part_title = part_element.find_element(by=By.CLASS_NAME, value=Class_id.Part_Text_Class_id).text
            
            # Part Node 생성
            part_node = PartNode(part_seq, part_title, class_node)
            
            ## Toggle이 열려있는지 확인
            Toggle_element = part_element.find_elements(By.CLASS_NAME, value = Class_id.Toggle_Close_Class_id)
            if len(Toggle_element) == 1: # Toggle이 닫혀있는 경우
                ## Toggle 열기
                click_processing_dialog(driver, part_element.find_element(By.CLASS_NAME, value = Class_id.Toggle_Close_Class_id), wait_time)

            ## Chapter 개수 탐색
            Chapter_elements = part_element.find_elements(By.CLASS_NAME, value = Class_id.Chapter_Class_id)
            
            if len(Chapter_elements) == 0: # Chapter 설정 없이 강의만 있는 경우 
                
                # Empty Chapter Node 생성
                chapter_node = ChapterNode(seq=1, title='', parent = part_node)
                
                lecture_elements = part_element.find_elements(By.CLASS_NAME, value = Class_id.Lecture_Class_id)
                
                lecture_info_collect(driver, lecture_elements, chapter_node)
                
            elif len(Chapter_elements) > 0: # Chapter 설정 및 강의 존재하는 경우
                ## 해당 Chapter 개수만큼의 영상 다운을 반복해야 함
                for chapter_seq, chapter_element in enumerate(Chapter_elements):
                    
                    ## Chapter Text 추출 
                    chapter_title = chapter_element.find_element(by=By.CLASS_NAME, value=Class_id.Chapter_Text_Class_id).text
                    
                    # Chapter Node 생성
                    chapter_node = ChapterNode(chapter_seq, chapter_title, parent = part_node)
                    
                    ## Toggle이 열려있는지 확인
                    Toggle_element = chapter_element.find_elements(By.CLASS_NAME, value = Class_id.Toggle_Close_Class_id)
                    if len(Toggle_element) == 1: # Toggle이 닫혀있는 경우
                        ## Toggle 열기
                        click_processing_dialog(driver, chapter_element.find_element(By.CLASS_NAME, value = Class_id.Toggle_Close_Class_id))
                
                    ## Lecture 개수 탐색
                    lecture_elements = chapter_element.find_elements(By.CLASS_NAME, value = Class_id.Lecture_Class_id)
                
                    lecture_info_collect(driver, lecture_elements, chapter_node)

    except: 
        print('강의 정보 수집 중 오류 발생')
        print('현재까지의 영상 정보 저장')
    finally:
        df = class_node.get_children_df(type = LectureNode, attributes = ['parent.parent.parent.title', 'parent.parent.title', 'parent.title', 'title', 'url'])
        df.to_excel('result.xlsx')
        # class_node.print_node()
        
        driver.quit()
