import numpy as numpy
import cv2
import pickle

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read("trainner.yml")

og_labels ={}
labels = {}
with open("labels.pickle", "rb") as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)

while (True):
	#capture frame by fram
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
	for(x, y, w, h) in faces:
		#print(x, y, w, h)
		roi_gray = gray[y:y+h, x:x+w] #(y-start. y-end)
		roi_color = frame[y:y+h, x:x+w]

		#recognize
		id_, conf = recognizer.predict(roi_gray)
		if conf>=45 and conf<=85:
			print(id_)
			print(labels[id_])
			name = labels[id_]
			font = cv2.FONT_HERSHEY_SIMPLEX
			color = (255,234,133)
			stroke = 2 
			cv2.putText(frame, name, (x,y), font, 1.5, color, stroke, cv2.LINE_AA)

		n=0
		while n < 100:
			filename = "images/sanjay/%n.jpg"%n
			cv2.imwrite(filenamee, frame)
			n+=1

 # ret, frame = vid.read()
 #    filename = "images/file_%d.jpg"%d
 #    cv2.imwrite(filename, frame)
 #    d+=1

		#draw a rectangle
		color= (234, 234,122)
		stroke = 2
		end_cord_x = x + w
		end_cord_y = y + h
		cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

	#display resulting frame
	cv2.imshow('frame', frame)

	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

#when everthing is done release the frame
cap.release()
cv2.destroyAllWindows()