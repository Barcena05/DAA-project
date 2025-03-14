import numpy as np

# cost_matrix = np.array([
#     [0, 12, 8, 15, 20],  # Depósito (0)
#     [12, 0, 10, 18, 25],  # Cliente 1
#     [8, 10, 0, 9, 12],  # Cliente 2
#     [15, 18, 9, 0, 7],  # Cliente 3
#     [20, 25, 12, 7, 0]  # Cliente 4
# ])



# depot = {'id': 0, 'time_window': [0, 480]}

# customers = [
#     {'id': 1, 'demand': 0.8, 'time_window': [60, 120], 'service_time': 15},
#     {'id': 2, 'demand': 1.2, 'time_window': [150, 210], 'service_time': 20},
#     {'id': 3, 'demand': 0.5, 'time_window': [180, 240], 'service_time': 10},
#     {'id': 4, 'demand': 1.0, 'time_window': [300, 360], 'service_time': 15}
# ]

# vehicle_capacity = 2.5

# vehicle_capacity2 = float('inf')

# fixed_cost = 98

def twvrp(cost_matrix, customers,vehicle_capacity,fixed_cost):

    savings = []
    for i in customers:
        for j in customers:
            if i['id'] != j['id']:
                costo_i0 = cost_matrix[i['id'], 0]
                costo_0j = cost_matrix[0, j['id']]
                costo_ij = cost_matrix[i['id'], j['id']]
                savings.append((i['id'], j['id'], costo_i0 + costo_0j - costo_ij))

    savings.sort(key=lambda x: -x[2])


    def get_customer(cid):
        return next(c for c in customers if c['id'] == cid)


    def calculate_route_time(route, cost_matrix):
        current_time = 0
        for i in range(1, len(route)):
            from_node = route[i - 1]
            to_node = route[i]


            travel_time = cost_matrix[from_node, to_node]
            current_time += travel_time

            if to_node != 0:
                customer = get_customer(to_node)

                if current_time < customer['time_window'][0]:
                    current_time = customer['time_window'][0]

                if current_time > customer['time_window'][1]:
                    return float('inf')
                current_time += customer['service_time']

        return current_time


    routes = []
    for customer in customers:
        routes.append({
            'nodes': [0, customer['id'], 0],
            'demand': customer['demand'],
            'time': calculate_route_time([0, customer['id'], 0], cost_matrix)
        })



    for (i, j, _) in savings:
        route_i = next((r for r in routes if r['nodes'][-2] == i), None)
        route_j = next((r for r in routes if r['nodes'][1] == j), None)

        if route_i and route_j and route_i != route_j:
            if (route_i['demand'] + route_j['demand']) <= vehicle_capacity:
                new_route = route_i['nodes'][:-1] + route_j['nodes'][1:]
                new_time = calculate_route_time(new_route, cost_matrix)

                if new_time != float('inf'):
                    routes.remove(route_i)
                    routes.remove(route_j)
                    routes.append({
                        'nodes': new_route,
                        'demand': route_i['demand'] + route_j['demand'],
                        'time': new_time
                    })


    total_cost = sum(
        sum(cost_matrix[route['nodes'][i], route['nodes'][i + 1]]
            for i in range(len(route['nodes']) - 1))
        for route in routes
    ) + (fixed_cost * len(routes))
    return routes, total_cost

# # ===========================
# # Resultados
# # ===========================
# routes, total_cost = twvrp(cost_matrix, customers, vehicle_capacity, fixed_cost)
# print("Rutas optimizadas:")
# for idx, route in enumerate(routes, 1):
#     node_names = ["Depósito" if n == 0 else f"Cliente {n}" for n in route['nodes']]
#     print(f"Vehículo {idx}: {' -> '.join(node_names)}")
#     print(f"   Volumen: {route['demand']:.1f}m³ | Tiempo total: {route['time']} min")

# print(f"\nCosto total: ${total_cost:.2f}")
# print(f"Vehículos utilizados: {len(routes)}")