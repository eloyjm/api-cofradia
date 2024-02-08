import React, { useEffect, useState } from 'react';
import { Button, Platform, FlatList, SafeAreaView, TouchableOpacity, StyleSheet, Text, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { api } from "./OAuth"


export default function DayList({navigation, route}) {
    const [hermandades, setHermandades] = useState([]);
    const [error, setError] = useState(null);
    const {day} = route.params;

    useEffect(() => {
        fetchHermandades();
    }, []);

    const fetchHermandades = async () => {
        try {
            const result = await api().get(`/hermandades/${day}`);
            setHermandades(result.data);
            console.log(result.data)
        } catch (error) {
            console.error("Error fetching hermandades:", error);
            setError(`Error: ${JSON.parse(error.request.response).detail}`);
        }
    }

  const renderItem = ({ item }) => (
    <TouchableOpacity style={styles.button}>
      {day && <Text style={styles.buttonText}>{item.name}</Text>}
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={{paddingTop: Platform.OS === "android" && 30}}>
        <Text style={styles.text}>{day}</Text>
      <FlatList
          data={hermandades}
          renderItem={renderItem}
          keyExtractor={(item, index) => index.toString()}
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
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
    button: {
      backgroundColor: 'white',
      paddingHorizontal: 20,
      paddingVertical: 15,
      marginVertical: 5,
      borderRadius: 10,
    },
    buttonText: {
      fontSize: 18,
      color: 'black',
      textAlign: 'center'
    },

  });