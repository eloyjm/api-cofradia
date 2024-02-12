import * as React from 'react';
import { Button, Platform, FlatList, SafeAreaView, TouchableOpacity, StyleSheet, Text, View } from 'react-native';

export default function List({navigation}) {
  dias = ["Domingo de Ramos", "Lunes Santo", "Martes Santo", "Miércoles Santo", "Jueves Santo", "Viernes Santo", "Sábado Santo", "Domingo de Resurrección"];
  
  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.button}
      onPress={() => navigation.navigate('DayList', { day: item })}
    >
      <Text style={styles.buttonText}>{item}</Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={{paddingTop: Platform.OS === "android" && 30}}>
      <FlatList
          data={dias}
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