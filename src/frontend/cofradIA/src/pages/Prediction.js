import React, { useState, useEffect, useRef } from 'react';
import { Platform, SafeAreaView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Image } from 'react-native';
import { Button } from 'react-native-elements';
import * as MediaLibrary from 'expo-media-library'
import { Camera, CameraType } from 'expo-camera';
import RNPickerSelect from 'react-native-picker-select';
import { Ionicons } from '@expo/vector-icons';

export default function Prediction({ navigation }) {
  const [image, setImage] = useState(null);
  const [hasCameraPermission, setHasCameraPermission] = React.useState(null);
  const [type, setType] = useState(Camera.Constants.Type.back);
  const [flash, setFlash] = useState(Camera.Constants.FlashMode.off);
  const cameraRef = useRef(null);

  useEffect(() => {
    (async () => {
      MediaLibrary.requestPermissionsAsync();
      const cameraStatus = await Camera.requestCameraPermissionsAsync();
      setHasCameraPermission(cameraStatus.status === 'granted');
    })();
  }, []);

  if (hasCameraPermission === false) {
    return <Text>No access to camera</Text>
  }

  const takePicture = async () => {
    if (cameraRef) {
      try {
        const data = await cameraRef.current.takePictureAsync();
        setImage(data.uri);
        console.log(data.uri)
      }
      catch (err) {
        console.log('err: ', err);
      }
    }
  };

  const makePrediction = async () => {
    if (image) {
      try {
        await MediaLibrary.createAssetAsync(image);
        alert("Image saved")
        setImage(null);
      } catch (error) {
        console.error("Error saving image:", error);
      }

    }
  }

  const [selectedDay, setSelectedDay] = useState(null);
  const data = [
    { label: 'Option 1', value: 'value1' },
    { label: 'Option 2', value: 'value2' },
    { label: 'Option 3', value: 'value3' },
  ];
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


  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.buttonContainer}>
        <Text style={styles.text}>IA Prediction</Text>
        <View style={styles.cameraContainer}>

          {!image ?
            <Camera
              style={styles.camera}
              type={type}
              flashMode={flash}
              ref={cameraRef}
              autoFocus="on"
            >
            </Camera>

            : <Image source={{ uri: image }} style={styles.camera}></Image>}
          <View>
            {image ? <>
              <View style={{
                flexDirection: 'column',
                justifyContent: 'space-between',
                paddingHorizontal: 50,
              }}>
                <>
                  <View style={styles.buttonContainer}>
                    <View style={styles.cameraButtonContainer}>
                      <TouchableOpacity onPress={() => setImage(null)} style={styles.cameraButton}>
                        <Ionicons name="trash-outline" size={24} color="white" />
                      </TouchableOpacity>
                    </View>
                  </View>
                </>

              </View>
              <View style={{
                flexDirection: 'row',
                justifyContent: 'space-between',
                paddingHorizontal: 50,
                alignItems: 'center',

              }}>
                <View style={styles.cameraButtonContainer}>
                  <TouchableOpacity onPress={makePrediction} style={styles.cameraButton}>
                    <Ionicons name="mail" size={24} color="white" />
                  </TouchableOpacity>

                </View>
                <View style={styles.button}>
                  <RNPickerSelect
                    value={selectedDay}
                    onValueChange={(itemValue, itemIndex) =>
                      setSelectedDay(itemValue)
                    }
                    items={dias}
                  >
                  </RNPickerSelect>
                </View>

              </View>

            </>
              :
              <View style={styles.buttonContainer}>
                <View style={styles.cameraButtonContainer}>
                  <TouchableOpacity onPress={takePicture} style={styles.cameraButton}>
                    <Ionicons name="camera" size={24} color="white" />
                  </TouchableOpacity>
                </View>
              </View>
            }

          </View>
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
  camera: {
    flex: 1,
    borderRadius: 10,
    height: '100%',
    width: '100%',
    overflow: 'hidden',
  },
  cameraContainer: {
    width: '100%',
    aspectRatio: 2 / 3,
    borderRadius: 20,
    overflow: 'hidden',
    padding: 10,
    paddingTop: 10,
  },
  image: {
    flex: 1,
    marginBottom: 20,
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
