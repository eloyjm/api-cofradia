import * as React from 'react';
import { Button, Platform, FlatList, SafeAreaView, TouchableOpacity, StyleSheet, Text, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { api } from "../login/OAuth"


export default function DayList({navigation}) {
    const [hermandades, setHermandades] = React.useState([]);
    const [error, setError] = React.useState(null);

    useEffect(() => {
        fetchHermandades();
    }, []);

    const fetchHermandades = async () => {
        try {
            const result = await api().get("/hermandades");
            setHermandades(result.data);
            console.log(result.data)
        } catch (error) {
            console.error("Error fetching hermandades:", error);
            setError(`Error: ${JSON.parse(error.request.response).detail}`);
        }
    }

  const renderItem = ({ item }) => (
    <TouchableOpacity style={styles.button}>
      <Text style={styles.buttonText}>{item}</Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={{paddingTop: Platform.OS === "android" && 30}}>
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