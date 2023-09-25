from flask import Flask, render_template
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ejecutar_codigo', methods=['POST'])
def ejecutar_codigo():
    # Aquí puedes colocar el código que deseas ejecutar cuando se presione el botón
    # Puedes acceder a los datos enviados desde el cliente utilizando request
    # Por ejemplo, para acceder a datos de formulario:
    # valor = request.form['nombre_del_campo']

    # Ejemplo de código:

    
    # mensaje = "¡Código ejecutado en Flask!"
    # return mensaje

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Iniciamos la captura de la cámara
    cap = cv2.VideoCapture(0)  # Cambia el número a 1 si tienes varias cámaras

    while True:
        # Capturamos un fotograma de la cámara
        ret, frame = cap.read()
        
        # Convertimos la imagen a escala de grises (el clasificador de caras de OpenCV trabaja con imágenes en escala de grises)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Realizamos la detección de caras en el fotograma
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # Dibujamos los rectángulos alrededor de las caras detectadas
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Agregamos un mensaje en el rectángulo
            cv2.putText(frame, 'Cara', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Mostramos el resultado
        cv2.imshow('Detección de Caras', frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    app.run()