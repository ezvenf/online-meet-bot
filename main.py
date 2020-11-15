from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import os
import keyboard
from schedule import schedule
import psutil as psutil
import sys
import platform

#Instructions
# Download a compatible chrome driver at https://sites.google.com/a/chromium.org/chromedriver/downloads
# !important, check the chrome browser version with the chrome driver on the website!
# Place the driver into the root of the project folder

#Add your email and password here
#Required: Turn off Gmail 2-Factor Authentication
email = "email" # <= Your Gmail email
passwrd = "password"# <= Your password

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

if platform.system().lower() == 'darwin':
    print("Detected OS: macOS")
    print("Loading Drivers....")
    # Chrome Browser Driver Path
    DRIVER_PATH_MAC = os.path.join(PROJECT_ROOT, "chromedriver")
elif platform.system().lower == 'win32':
    print("Detected OS: Windows")
    print("Loading Drivers....")
    DRIVER_PATH_MAC = os.path.join(PROJECT_ROOT, "chromedriver.exe")
elif platform.system().lower == 'linux':
    print("Detected OS: Linux")
    print("Loading Drivers....")
    DRIVER_PATH_MAC = os.path.join(PROJECT_ROOT, "chromedriver_linux")

options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 2,     # 1:allow, 2:block
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.notifications": 2
    })

def has_connection(driver):
    print("Checking connection...")
    try:
        driver.find_element_by_xpath('//span[@jsselect="heading" and @jsvalues=".innerHTML:msg"]')
        return True
    except: 
        print("Connection OK")
        return False

class meet_bot:
    def __init__(self):
        print("Initializing chrome driver....")
        self.bot = webdriver.Chrome(chrome_options=options, executable_path=DRIVER_PATH_MAC)

    def login(self, email, paswrd, meeting_key):
        bot = self.bot
        bot.get(f"https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fmeet.google.com%2F{meeting_key}&sacu=1&hl=en_US&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        time.sleep(2)
        #Email field login attempt
        try:
            bot.find_element_by_id("identifierId").send_keys(email)
            bot.find_element_by_id("identifierNext").click()
        except:
            bot.find_element_by_id("Email").send_keys(email)
            bot.find_element_by_id("next").click()
        
        try:
            time.sleep(5)
            bot.find_element_by_name("password").send_keys(passwrd)
            bot.find_element_by_id("passwordNext").click()
        except Exception as e:
            print(f"Error: {e}")
            print("Terminating Session and Restarting script....")
            bot.quit()
            print("Restarting program.....")
            os.system("python3 main.py")
        
            

    
        
    def class_init(self):
        bot = self.bot
        dismiss_notification = bot.find_element_by_xpath("/html/body/div/div[3]/div/div[2]/div[3]/div/span/span")
        dismiss_notification.click()
        time.sleep(10)
        bot.find_element_by_xpath("/html/body/div[1]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span").click()

def core(key):
    obj = meet_bot()
    try:
        print("Attempting Login")
        # start_meeting(email, passwrd, i[0])
        obj.login(email, passwrd, key)
        time.sleep(10)
        obj.class_init()
    except Exception as e:
        print(f"Error: {e}")
        print("Terminating Session and Restarting script....")
        obj.bot.quit()
        print("Restarting program.....")
        os.system("python3 main.py")
        
                
            
            #End meeting at the end time
    try:
        wait_delta = datetime.strptime(time_asc[i+1].split(",")[0], "%H:%M:%S") - datetime.strptime(datetime.now().time().strftime("%H:%M:%S"), "%H:%M:%S")
        wait_timer = int(str(wait_delta).split(":")[0]) * 3600 + int(str(wait_delta).split(":")[1]) * 60 + int(str(wait_delta).split(":")[2])
        print("Waiting until the end of the meeting in: ", wait_timer, "Sec")
        time.sleep(wait_timer)
        obj.bot.close()
    except:
        wait_delta = datetime.strptime(datetime.now().time().strftime("%H:%M:%S"), "%H:%M:%S") - datetime.strptime(time_asc[i+1].split(",")[0], "%H:%M:%S")
        wait_timer = int(str(wait_delta).split(":")[0]) * 3600 + int(str(wait_delta).split(":")[1]) * 60 + int(str(wait_delta).split(":")[2])
        print("Waiting until the end of the meeting in: ", wait_timer, "Sec")
        time.sleep(wait_timer)
        obj.bot.close()

    #Close script after the final meeting
    wait_delta = datetime.strptime(time_asc[-1].split(",")[0], "%H:%M:%S") - datetime.strptime(datetime.now().time().strftime("%H:%M:%S"), "%H:%M:%S")
    if not "day" in str(wait_delta).split(",")[0]:
        wait_timer = int(str(wait_delta).split(":")[0]) * 3600 + int(str(wait_delta).split(":")[1]) * 60 + int(str(wait_delta).split(":")[2])
        if wait_timer < 10:
            time.sleep(wait_timer)
            quit()

def main():
    print("Logging into meet.google.com/" + str(schedule[int(time_asc[i].split(",")[1])][0]))
    core(schedule[int(time_asc[i].split(",")[1])][0])

#Collect time sequence
time_asc = []
for i in range(0, len(schedule)):
    time_asc.append(f"{schedule[i][1]},{i}")
    time_asc.append(f"{schedule[i][2]},{i}")
time_asc.sort()


for i in range(0, len(time_asc)):
    
    if i%2==0:
        
        try:
            tdelta = datetime.strptime(time_asc[i].split(",")[0], "%H:%M:%S") - datetime.strptime(datetime.now().time().strftime("%H:%M:%S"), "%H:%M:%S")
            meeting_duration = int(str(datetime.strptime(time_asc[i+1].split(",")[0], "%H:%M:%S") - datetime.strptime(time_asc[i].split(",")[0], "%H:%M:%S")).split(":")[0]) * 3600 + int(str(datetime.strptime(time_asc[i+1].split(",")[0], "%H:%M:%S") - datetime.strptime(time_asc[i].split(",")[0], "%H:%M:%S")).split(":")[1]) * 60 + int(str(datetime.strptime(time_asc[i+1].split(",")[0], "%H:%M:%S") - datetime.strptime(time_asc[i].split(",")[0], "%H:%M:%S")).split(":")[2])
            resume_time = int(str(datetime.strptime(time_asc[i+1].split(",")[0], "%H:%M:%S") - datetime.strptime(datetime.now().time().strftime("%H:%M:%S"), "%H:%M:%S")).split(":")[0]) * 3600 + int(str(datetime.strptime(time_asc[i+1].split(",")[0], "%H:%M:%S") - datetime.strptime(datetime.now().time().strftime("%H:%M:%S"), "%H:%M:%S")).split(":")[1]) * 60 + int(str(datetime.strptime(time_asc[i+1].split(",")[0], "%H:%M:%S") - datetime.strptime(datetime.now().time().strftime("%H:%M:%S"), "%H:%M:%S")).split(":")[2])
            if resume_time < meeting_duration:
                print("Resuming meeting ", schedule[int(str(time_asc[i]).split(",")[1])][0])
                main()
            elif "day" in str(tdelta).split(",")[0]:
                print("The meeting ",schedule[int(str(time_asc[i]).split(",")[1])][0], " may be in 24 Hr according to the schedule")
            else:
                wait_time = int(str(tdelta).split(":")[0]) * 3600 + int(str(tdelta).split(":")[1]) * 60 + int(str(tdelta).split(":")[2])
                if int(wait_time/3600):
                    print(f"Meeting starts in {int(wait_time/3600)} Hrs {int(wait_time/60 - int(wait_time/3600) * 60)} Min......")
                elif int(wait_time/60 - int(wait_time/3600) * 60):
                    print(f"Meeting starts in {int(wait_time/60 - int(wait_time/3600) * 60)} Min.......")
                else:
                    print(f"Meeting starts in {wait_time} Sec.......")
                
                time.sleep(wait_time)
                main()

        except Exception as e:
            print(e)