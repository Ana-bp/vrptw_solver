# VRPTW Solver

## 📌Project Overview
This project is a web application developed in Python to solve the Vehicle Routing Problem with Time Windows (VRPTW). The VRPTW is an optimization problem that aims to reduce transportation 
costs and time spent in logistic operations by defining optimal routes to serve a set of clients while considering time windows constraints for client service. 

Developed to be accessible and democratize vehicle routing optimization solutions for medium and small organizations, this tool delivers satisfactory results for real-life datasets, helping to enhance efficiency and reduce logistics-related operational costs. 

The solver employs a **greedy algorithm** to generate the solution, and based on the user’s uploaded customer list and vehicle fleet details, the system provides the route planning for the set of customers. 
It also integrates external **APIs for geolocation and distance matrix calculations**, ensuring accurate and efficient routing. Additionally, a user-friendly interface was developed using **Streamlit**, allowing for easy data input and result visualization.

## 🛠️Technologies used
- **Python** (Pandas, Streamlit, Requests)
- **APIs** (OSMR, OpenStreetMap)

## 🔎How it works
1. Reads client's addresses from a CSV file.
2. Retrieves geographical coordinates for each address using the OpenStreetMap API.
3. Computes travel distances (in seconds) between all locations via the OSMR API, creating a distance matrix.
4. Implements a greedy algorithm to generate optimized routes while adhering to all VRPTW constraints.
5. Displays the route details (number of routes, clients per route, and a Gantt chart) in a Streamlit-based UI.

## 🚀 Installation & Usage
