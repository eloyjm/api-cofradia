import * as React from 'react';
import { Button, Platform, SafeAreaView, StyleSheet, Text, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer, Screen } from '@react-navigation/native';
import { createBottomTabNavigator, } from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';
import { createStackNavigator } from '@react-navigation/stack';

// Screens
import Home from './Home';
import Prediction from './Prediction';
import List from './List';
import DayList from './DayList';

// Screen names
const homeName = "Home";
const predictionName = "Prediction";
const listName = "List";
const dayListName = "DayList";

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Stack Navigator para List y DayList
function ListStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen name={listName} component={List} options={{ headerShown: false }}/>
            <Stack.Screen name={dayListName} component={DayList} options={{ headerShown: false }}/>
        </Stack.Navigator>
    );
}

export default function MainContainer({ navigation }) {
    return (
        <NavigationContainer>
            <StatusBar style="light"/>
            <Tab.Navigator
                initialRouteName={homeName}
                screenOptions={({ route }) => ({
                    tabBarIcon: ({ focused, size }) => {
                        let iconName;
                        const iconSize = 30;

                        if (route.name === homeName) {
                            iconName = focused ? 'home' : 'home-outline';
                        } else if (route.name === predictionName) {
                            iconName = focused ? 'camera' : 'camera-outline';
                        } else if (route.name === listName) {
                            iconName = focused ? 'list' : 'list-outline';
                        }
                        return <Ionicons name={iconName} size={iconSize} color={"#990033"} />;
                    },
                    headerShown: false,
                    tabBarActiveTintColor: "#990033",
                    tabBarShowLabel: false,
                    

                })}
            >
                <Tab.Screen name={homeName} component={Home} />
                <Tab.Screen name={listName} component={ListStack} />
                <Tab.Screen name={predictionName} component={Prediction} />
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