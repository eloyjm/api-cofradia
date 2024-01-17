import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

#DATOS
celsius = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
fahrenheit = np.array([-40, 14, 32, 46, 59, 72, 100], dtype=float)

#MODELO CAPAS REDEs
oculta1 = tf.keras.layers.Dense(units=3, input_shape=[1])
oculta2 = tf.keras.layers.Dense(units=3)
salida = tf.keras.layers.Dense(units=1)
modelo = tf.keras.Sequential([oculta1, oculta2, salida])

#CONFIGURACION MODELO
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.1),
    loss='mean_squared_error'
)

#ENTRENAMIENTO MODELO
print("Comenzando entrenamiento...")
historial = modelo.fit(celsius, fahrenheit, epochs=1000, verbose=False)
print("Modelo entrenado!")

#USO DE MODELO
def prediccion(celsius):
    print("Hagamos una prediccion")
    resultado = modelo.predict([celsius])
    return resultado

print("Farenheit: ", prediccion(100.0))
