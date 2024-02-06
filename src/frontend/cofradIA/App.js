import { StatusBar } from 'expo-status-bar';
import { Button, Platform, SafeAreaView, StyleSheet, Text, View } from 'react-native';
import { useState } from 'react';
import MainContainer from './src/pages/MainContainter';

export default function App() {
  return (
    <MainContainer />
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
