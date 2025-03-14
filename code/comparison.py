import numpy as np
from main import twvrp
from results import results

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Leer la capacidad del vehículo
    line = lines[4]
    vehicle_capacity = int(lines[4].split()[1])

    # Leer los datos de los clientes
    customers = []
    for line in lines[8:]:
        parts = line.split()
        if len(parts) < 7:
            continue
        cust_no = int(parts[0])
        demand = int(parts[3])
        ready_time = int(parts[4])
        due_date = int(parts[5])
        service_time = int(parts[6])
        customers.append({
            'id': cust_no,
            'demand': demand,
            'time_window': [ready_time, due_date],
            'service_time': service_time,
            'xcoord': float(parts[1]),
            'ycoord': float(parts[2])
        })

    # Construir la matriz de costos (en este caso, usaremos distancias euclidianas)
    num_customers = len(customers)
    cost_matrix = np.zeros((num_customers, num_customers))
    for i in range(num_customers):
        for j in range(num_customers):
            if i == j:
                cost_matrix[i][j] = 0
            else:
                # Calcular la distancia euclidiana entre los clientes i y j
                x1, y1 = customers[i]['xcoord'], customers[i]['ycoord']
                x2, y2 = customers[j]['xcoord'], customers[j]['ycoord']
                cost_matrix[i][j] = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    return cost_matrix, customers, vehicle_capacity

def main():
    vehicle_error = []
    cost_error = []
    for l in ['R','C']:
        for j in range(1,3):
            for i in range(1,11):
                file_path = f'./homberger_200_customer_instances/{l}{j}_2_{i}.TXT'
                cost_matrix, customers, vehicle_capacity = read_txt_file(file_path)
                fixed_cost = 0  # Puedes ajustar este valor según sea necesario

                routes, total_cost = twvrp(cost_matrix, customers, vehicle_capacity, fixed_cost)
                # print("Rutas optimizadas:")
                # for idx, route in enumerate(routes, 1):
                #     node_names = ["Depósito" if n == 0 else f"Cliente {n}" for n in route['nodes']]
                #     print(f"Vehículo {idx}: {' -> '.join(node_names)}")
                #     print(f"   Volumen: {route['demand']:.1f}m³ | Tiempo total: {route['time']} min")
                print(f'\nArchivo: {l}{j}_2_{i}.TXT')
                print(f"Costo total: ${total_cost:.2f}")
                print(f"Vehículos utilizados: {len(routes)}")
                vehicle_error.append(abs(len(routes) - results[f'{l}{j}_2_{i}'][0])/len(routes))
                cost_error.append(abs(total_cost - results[f'{l}{j}_2_{i}'][1])/total_cost)
    vehicle_error = np.array(vehicle_error)
    cost_error = np.array(cost_error)
    print(f"\nMedia del error en vehículos: {vehicle_error.mean():.2f}")
    print(f"Desviación estandar del error en vehículos: {vehicle_error.std():.2f}")
    print(f"\nMedia del error en costo total: {cost_error.mean():.2f}")
    print(f"Desviación estandar del error en costo total: {cost_error.std():.2f}")

    import matplotlib.pyplot as plt
    plt.plot(vehicle_error, label='Error en vehículos')    
    plt.plot([vehicle_error.mean()]*len(vehicle_error), label=f'Media error en vehículos: {vehicle_error.mean():.2f}', linestyle='--')    
    plt.fill_between(range(len(vehicle_error)), [vehicle_error.mean()-vehicle_error.std()]*len(vehicle_error), [vehicle_error.mean()+vehicle_error.std()]*len(vehicle_error), alpha=0.2, color='b')    
    plt.legend()
    plt.savefig('vehicle_error.png')
    plt.show()

    plt.plot(cost_error, label='Error en costo total')
    plt.plot([cost_error.mean()]*len(cost_error), label=f'Media error en costo total: {cost_error.mean():.2f}', linestyle='--')
    plt.fill_between(range(len(cost_error)), [cost_error.mean()-cost_error.std()]*len(cost_error), [cost_error.mean()+cost_error.std()]*len(cost_error), alpha=0.2, color='r')
    plt.legend()
    plt.savefig('cost_error.png')
    plt.show()

if __name__ == "__main__":
    main()