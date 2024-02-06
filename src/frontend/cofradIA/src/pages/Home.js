import * as React from 'react';
import { Button, Platform, SafeAreaView, StyleSheet, Text, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';


export default function Home({navigation}) {
  return (
    <SafeAreaView style={styles.container}>
      <View style={{paddingTop: Platform.OS === "android" && 30}}>
        <Text style={styles.text}>Cofrad-IA</Text>
        <StatusBar style="auto" />
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
    }
  });