import * as React from 'react';
import { Button, Platform, SafeAreaView, StyleSheet, Text, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator, } from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';

// Screens
import Home from './Home';
import Camera from './Camera';
import List from './List';

// Screen names
const homeName = "Home";
const cameraName = "Camera";
const listName = "List";

const Tab = createBottomTabNavigator();

export default function MainContainer({ navigation }) {
    return (
        <NavigationContainer>
            <Tab.Navigator
                initialRouteName={homeName}
                screenOptions={({ route }) => ({
                    tabBarIcon: ({ focused, color, size }) => {
                        let iconName;
                        if (route.name === homeName) {
                            iconName = focused ? 'home' : 'home-outline';
                        } else if (route.name === cameraName) {
                            iconName = focused ? 'camera' : 'camera-outline';
                        } else if (route.name === listName) {
                            iconName = focused ? 'list' : 'list-outline';
                        }
                        return <Ionicons name={iconName} size={size} color={color} />;
                    },

                    "tabBarActiveTintColor": "#990033",
                    "tabBarInactiveTintColor": "gray",
                    "tabBarLabelStyle": {
                        "paddingBottom": 10,
                        "paddingTop": 10,
                        "fontSize": 10,
                        "fontWeight": "bold"
                    },
                    "tabBarStyle": [
                        {
                            "display": "flex"
                        },
                        null
                    ]

                })}
            >
                <Tab.Screen name={homeName} component={Home} />
                <Tab.Screen name={listName} component={List} />
                <Tab.Screen name={cameraName} component={Camera} />


            </Tab.Navigator>
        </NavigationContainer>
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