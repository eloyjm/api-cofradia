import React, { useState, useEffect } from 'react';
import { SafeAreaView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { Image } from 'react-native';
import { Camera } from 'expo-camera';
import RNPickerSelect from 'react-native-picker-select';
import { Ionicons } from '@expo/vector-icons';
import { api } from "./OAuth"
import * as ImagePicker from 'expo-image-picker';

export default function Prediction({ navigation }) {
  const [image, setImage] = useState();
  const [hasCameraPermission, setHasCameraPermission] = React.useState(null);
  const [selectedDay, setSelectedDay] = useState("");
  const [result, setResult] = useState([]);

  const dias = [
    { label: "Domingo de Ramos", value: "Domingo de Ramos" },
    { label: "Lunes Santo", value: "Lunes Santo" },
    { label: "Martes Santo", value: "Martes Santo" },
    { label: "Miércoles Santo", value: "Miércoles Santo" },
    { label: "Jueves Santo", value: "Jueves Santo" },
    { label: "Viernes Santo", value: "Viernes Santo" },
    { label: "Sábado Santo", value: "Sábado Santo" },
    { label: "Domingo de Resurrección", value: "Domingo de Resurrección" }
  ];

  useEffect(() => {
    (async () => {
      const cameraStatus = await Camera.requestCameraPermissionsAsync();
      const mediaLibraryStatus = await ImagePicker.requestMediaLibraryPermissionsAsync(); // Solicita permisos de la biblioteca de medios
      setHasCameraPermission(cameraStatus.status === 'granted' && mediaLibraryStatus.status === 'granted');
    })();
  }, []);

  if (hasCameraPermission === false) {
    return <Text>No access to camera</Text>
  }

  const pickImage = async () => {
    const options = {
      mediaType: ImagePicker.MediaTypeOptions.Images,
      includeBase64: false,
      maxHeight: 2000,
      maxWidth: 2000,
      storageOptions: {
        skipBackup: true,
        path: 'images',
      },
    }
    try {
      const response = await ImagePicker.launchImageLibraryAsync(options);
      if (response.errorCode) {
        console.log("Image picker error: ", response.errorMessage);
      } else if (response.didCancel) {
        console.log("User cancelled image picker");

      } else {
        setImage(response);
        console.log("URI", response.assets?.[0]?.uri)
      }
    } catch (error) {
      console.log("Error al abrir la cámara:", error);
    }
  };

  const takePicture = async () => {
    const options = {
      mediaType: 'photo',
      includeBase64: false,
      maxHeight: 2000,
      maxWidth: 2000,
    }

    try {
      const response = await ImagePicker.launchCameraAsync(options);

      if (response.canceled) {
        console.log("El usuario canceló la selección de la imagen");
      } else if (response.errorCode) {
        console.log("Error al seleccionar la imagen:", response.errorMessage);
      } else {
        setImage(response);
        console.log(image)
      }
    } catch (error) {
      console.log("Error al abrir la cámara:", error);
    }
  }

  const makePrediction = async () => {
    if (image) {
      try {
        console.log("selectedDay", selectedDay)
        console.log("image", image)

        const formData = new FormData();
        formData.append('img', { uri: image.uri || image.assets?.[0]?.uri, type: 'image/jpeg', name: image.assets?.[0]?.fileName });
        const response = await api().post(`/prediction?day=${selectedDay}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        if (response.data.length > 0) {
          setResult(response.data);
          console.log("response", response.data)
        }
      } catch (error) {
        console.error("Error saving image:", error);
      }

    }
  }


  const makePrediction1 = async () => {
    if (image) {

      const formData = new FormData();
      const file = {
        uri: image.uri || image.assets?.[0]?.uri,
        type: 'image/jpg',
        name: new Date().getTime() + '.jpg',
      };
      formData.append('file', file);

      try {
        const response = await api().post(`/prediction1`, formData, {
          headers: {
            Accept: 'application/json',
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log("response", response.data)
        setImage(null);
      } catch (error) {
        console.error("Error saving image:", error);
      }
    }
  }


  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.buttonContainer}>
        <Text style={styles.text}>IA Prediction</Text>
        <View style={styles.cameraContainer}>

          {image ? (
            <>
              <Image
                source={{ uri: image.uri || image.assets?.[0]?.uri }}

                style={{ flex: 1, width: '100%', height: '100%' }}
                resizeMode="contain"
              />

              {result.length > 0 ? result.map((item, index) => (
                <View key={index} style={{ flexDirection: "row", justifyContent: "center", alignItems: "center" }}>
                  <Text style={{ fontSize: 20, fontWeight: "bold", color: "white" }}>Prediction: {item.name}</Text>
                </View>
              )) : null}

              <View style={styles.buttonContainer}>
                <View style={styles.cameraButtonContainer}>
                  <TouchableOpacity
                    onPress={() => setImage(null)}
                    style={styles.cameraButton}>
                    <Ionicons
                      name="trash-outline"
                      size={24}
                      color="white"
                    />
                  </TouchableOpacity>
                </View>
              </View>
              <View
                style={{
                  flexDirection: 'row',
                  justifyContent: 'space-between',
                  paddingHorizontal: 50,
                  alignItems: 'center',
                }}>
                <View style={styles.cameraButtonContainer}>
                  <TouchableOpacity
                    onPress={makePrediction}
                    style={styles.cameraButton}>
                    <Ionicons name="mail" size={24} color="white" />
                  </TouchableOpacity>
                </View>
                <View style={styles.button}>
                  <RNPickerSelect
                    value={selectedDay}
                    onValueChange={(itemValue, itemIndex) =>
                      setSelectedDay(itemValue)
                    }
                    items={dias}>
                  </RNPickerSelect>
                </View>
              </View>
            </>
          ) : (
            <View style={styles.buttonContainer}>
              <View style={styles.cameraButtonContainer}>
                <TouchableOpacity
                  onPress={takePicture}
                  style={styles.cameraButton}>
                  <Ionicons name="camera" size={24} color="white" />
                </TouchableOpacity>
              </View>
              <View style={styles.cameraButtonContainer}>
                <TouchableOpacity
                  onPress={pickImage}
                  style={styles.cameraButton}>
                  <Ionicons name="image" size={24} color="white" />
                </TouchableOpacity>
              </View>
            </View>
          )}
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  contentContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  cameraButtonContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 60,
    height: 60,
    borderRadius: 30,
    borderWidth: 2,
    borderColor: '#fff',
    marginTop: 10,
  },
  cameraButton: {
    backgroundColor: '#990033',
    borderRadius: 30,
    padding: 10,
  },
  cameraContainer: {
    width: '100%',
    aspectRatio: 2 / 3,
    borderRadius: 20,
    overflow: 'hidden',
    padding: 10,
    paddingTop: 10,
  },
  buttonsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  button: {
    backgroundColor: 'white',
    paddingHorizontal: 20,
    paddingVertical: 10,
    marginHorizontal: 10,
    borderRadius: 10,
  },
  buttonText: {
    color: 'black',
    fontSize: 16,
  },
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: "#990033"
  },
  text: {
    fontSize: 32, fontWeight: "bold", color: "white"
  },
  buttonContainer: {
    alignItems: 'center',
  },
  button: {
    backgroundColor: 'white',
    marginVertical: 10,
    width: 200,
    height: 50,
    borderRadius: 10,
  },
  buttonTitle: {
    color: 'black',
    fontSize: 18,
  },

});
