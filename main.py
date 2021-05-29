import numpy as np 
import cv2
import pickle

import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select



path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)

#face-recog trained data
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")


#face-recog
def face_recog():
    og_labels = {}
    labels ={}
    with open("labels.pickle", "rb") as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}

    cap = cv2.VideoCapture(0)

    try:
    	while(True):
        	#capture frame
        	ret, frame =cap.read()
        	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        	for(x, y, w, h) in faces:
        	    roi_gray = gray[y:y+h, x:x+w]
        	    roi_color = frame[y:y+h, x:x+w]

        	    #recognize
        	    id_, conf = recognizer.predict(roi_gray)
        	    if conf>=45 and conf<=85:
        	        name = labels[id_]
        	        font = cv2.FONT_HERSHEY_SIMPLEX
        	        color = (255,234,133)
        	        stroke = 2 
        	        cv2.putText(frame, name, (x,y), font, 1.5, color, stroke, cv2.LINE_AA)
	
        	    img_item = "new_image.png"
        	    cv2.imwrite(img_item, frame)

        	    color= (234, 234,122)
        	    stroke = 2
        	    end_cord_x = x + w
        	    end_cord_y = y + h
        	    cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

        	cv2.imshow('frame', frame)

        	if cv2.waitKey(6000) or 0xFF == ord('q'):
        		break
        
    	cap.release()
    	cv2.destroyAllWindows()
    	return name
    except UnboundLocalError:
    	speak("Sorry, Cannot detect your face. Please try again.")


# speak given text 
def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice_main.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

#specifying url to visit
def web(said):
    driver.get(said)


# listening to audio and return text
def get_audio():
    r = sr.Recognizer();
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
        return said


def web_open(domain):
    driver.get("https://" + domain + ".in")

#login process
def login(name):
    if(name == "rohan"):
        loginTextArea = driver.find_element_by_id("ap_email")
        loginTextArea.send_keys("rohansawant1801@gmail.com")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "continue"))).click()

        passwordTextArea = driver.find_element_by_id("ap_password")
        passwordTextArea.send_keys("")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "signInSubmit"))).click()

#searching a specific product which is store in ITEM variable
def search_prod(): 
    search = driver.find_element_by_id("twotabsearchtextbox")
    search.send_keys("apple iphone 12")
    speak("searching for apple iphone 12")
    search.send_keys(Keys.RETURN)


#filtering products
# def filter_prod():
# #clicking 3 stars and above products image on left hand side
	
# 	#for filtering bases on sizes
# 	speak("Which size do you prefer?")
# 	size = get_audio()
# 	speak("Filtering out tshirts having size "+size)
# 	if(size == "L"):
# 		large = driver.find_element_by_id("a-autoid-7-announce")
# 	elif (size == "XL"):
# 		xlarge = driver.find_element_by_id("a-autoid-8-announce")


# 	speak("Please wait, Filtering out products having ratings 3 and above")
# 	stars = driver.find_element_by_id('p_72/1318477031')
# 	stars.click()
# 	speak(" Filtering of products complete ")

# 	name = driver.find_elements_by_tag_name('h5')
#     price = driver.find_elements_by_class_name('a-price-whole')

#     n=0
#     for p in price:
#         if(n <= 3):
#             print(name[n].text+":"+p.text)
#             n+=1
#         else:
#             break

#     print ("done")


def filter_prod():

	#filter based on size
	# speak("which size do you prefer?")
	# size= "L" #get_audio()
	# speak("filtering out" + size + "tshirts for you")

	# if(size == "L"):
	# 	large = driver.find_element_by_id("a-autoid-7-announce")
	# elif (size == "XL"):
	# 	xlarge = driver.find_element_by_id("a-autoid-8-announce")

	# speak("Filtering of tshirts complete.")
	# time.sleep(1)
	speak("Please wait, Filtering out products having ratings 3 and above")
	stars = driver.find_element_by_id("p_72/1318477031")
	stars.click()
	speak("Filtering of products complete")

	name = driver.find_elements_by_class_name("a-size-medium a-color-base a-text-normal")
	
	price = driver.find_elements_by_class_name("a-price-whole")

	n=0
	for p in price:
		if(n <= 3):
			print(name[n].text + " : " + p.text)
			n+=1
		else:
			break

def addToCart():

	size = "L" #get_audio()
	print("size "+ size)
	element = driver.find_element_by_id("native_dropdown_selected_size_name")
	drp = Select(element)
	drp.select_by_visible_text(size)


#func call
nameofPerson = face_recog()
# print("nameofPerson :" + nameofPerson)

if not nameofPerson is None:
	speak("Hello"+  nameofPerson+ ", please wait signing in to your amazon account")
	time.sleep(1)

	web("https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")

	login(nameofPerson)

	speak("Sign in process complete")
	time.sleep(1)

	speak("what you want to search for?")
	time.sleep(1)

	search_prod()
	filter_prod()
	speak("I have selected top 3 product for you.")
	speak("selecting first product for you")
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[1]/div/span[3]/div[2]/div[10]/div/span/div/div/div[4]/h2/a/span"))).click()
	# addToCart()
	# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "buy-now-button"))).click()
else:
	driver.quit()
	

#website = get_audio()
#time.sleep(2)



#web_open("amazon")
#time.sleep(1)



#item = get_audio()




#/html/body/div[1]/div[2]/div[1]/div/div[1]/div/span[3]/div[2]/div[8]/div/span/div/div/div/div[4]/h2/a/span

# /html/body/div[1]/div[2]/div[1]/div/div[1]/div/span[3]/div[2]/div[7]/div/span/div/div/div/div/div[4]/div[2]/h5/span
# /html/body/div[1]/div[2]/div[1]/div/div[1]/div/span[3]/div[2]/div[5]/div/span/div/div/div/div/div[4]/div[2]/h5/span

# /html/body/div[1]/div[2]/div[1]/div/div[1]/div/span[3]/div[2]/div[8]/div/span/div/div/div/div[4]/div/h5/span
# /html/body/div[1]/div[2]/div[1]/div/div[1]/div/span[3]/div[2]/div[10]/div/span/div/div/div[4]/div/h5/span
# /html/body/div[1]/div[2]/div[1]/div/div[1]/div/span[3]/div[2]/div[8]/div/span/div/div/div/div[4]/div/h5/span
# /html/body/div[1]/div[2]/div[1]/div/div[1]/div/span[3]/div[2]/div[11]/div/span/div/div/div[4]/div/h5/span

