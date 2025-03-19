# VRPTW Solver

## 📌Project Overview
This project consists on a web application developed in Python to solve the Vehicle Routing Problem with Time Windows (VRPTW). The VRPTW is an optimization problem that aims to reduce transportation 
costs and time spent in logistic operations by defining optimal routes to serve a set of clients, while considering time windows constraints for client service. Developed to be accessible and democratize 
vehicle routing optimization solutions for medium and small organizations, the tool offers satisfactory results for real-life datasets, helping to enhance efficiency and reduce logistics-related operational costs. 

The solver employs a **greedy algorithm** to generate the solution, and based on the user’s uploaded customer list and vehicle fleet details, it provides the route planning for the set of customers. 
The system utilizes external **APIs for geolocation and distance matrix calculations**, ensuring accurate and efficient routing. Additionally, a user interface was developed through **Streamlit**, to facilitate 
data input and visualization of results.

## 🛠️Technologies used
- **Python** (Pandas, Streamlit, Requests)
- **APIs** (OSMR, OpenStreetMap)

## 🔎How it works
1. Collects client's addresses from a CSV file
2. Gets the coordinates of each address through the OpenStreetMap API
3. Calculates the distance (in seconds) between every coordinate through the OSMR API, creating a distance matrix
4. Implements a greedy algorithm to create the less time-consuming routes, while respecting all the constraints of the VRPTW
5. Provides the routes (how many routes, clients per route, and Gantt chart) to the user in a Streamlit-based UI

## 🚀 Installation & Usage
