# Messaging systems

In this exercises you will experiment with messaging systems and deploy the examples that were demonstrated in the lecture on messaging systems:

https://github.com/lmkr/ada502-messaging/

## Task 1

Start by cloning the above repository and import it into your IDE / environment that you use for Python programming.

## Task 2

Create an account on HiveMQ https://console.hivemq.cloud/ and setup a messaging cluster.

Run the basic example to check that your cluster is working

https://github.com/lmkr/ada502-messaging/tree/main/ada502-messaging/basic

Remember to create credentials and set the configuration.

## Task 3

Run the example with the seperate subscriber and publisher client:

https://github.com/lmkr/ada502-messaging/tree/main/ada502-messaging/connector

Check the log files that things are working properly.

## Task 4

Creating an account on ThingsPeak https://thingspeak.com/ and setup a channel for visualisation.

Run the weather data example

https://github.com/lmkr/ada502-messaging/tree/main/ada502-messaging/wdsystem

and the Thingspeak forwarder and see whether the service is receiving the published messages.

## Task 5

Creating an account on MongoDB: https://www.mongodb.com/ and setup a database an time series collection.

Start also the MongDB forwarder and check whether the data is being stored into the time series collection.
