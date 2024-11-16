import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt



def maximize_cost(precios, produccion, graph = False, S_max = 15000,
                  B_max = 3000, V_max = 4000, S_init = 4500):
 
    n = 24  # Número de horas
    v = cp.Variable(n)         # Energía vendida al mercado por hora
    b_in = cp.Variable(n)      # Energía que entra a la batería por hora
    b_out = cp.Variable(n)     # Energía que sale de la batería por hora
    s = cp.Variable(n)     # Estado de carga de la batería (incluye estado inicial)
    carga_flag = cp.Variable(n, boolean = True)
    
    datetime = ['2023-04-15T01:00:00' '2023-04-15T02:00:00'
                '2023-04-15T03:00:00' '2023-04-15T04:00:00'
                '2023-04-15T05:00:00' '2023-04-15T06:00:00'
                '2023-04-15T07:00:00' '2023-04-15T08:00:00'
                '2023-04-15T09:00:00' '2023-04-15T10:00:00'
                '2023-04-15T11:00:00' '2023-04-15T12:00:00'
                '2023-04-15T13:00:00' '2023-04-15T14:00:00'
                '2023-04-15T15:00:00' '2023-04-15T16:00:00'
                '2023-04-15T17:00:00' '2023-04-15T18:00:00'
                '2023-04-15T19:00:00' '2023-04-15T20:00:00'
                '2023-04-15T21:00:00' '2023-04-15T22:00:00'
                '2023-04-15T23:00:00' '2023-04-16T00:00:00']

    # Restricciones
    constraints = []

    # Inicializar el estado de la batería
    constraints.append(s[0] == S_init)
    constraints.append(s[-1] == S_init)

    # Restricciones por hora
    for t in range(n):
        # Balance de energía
            
        # Límites de almacenamiento de la batería
        constraints.append(0 <= s[t])
        constraints.append(s[t] <= S_max)
        # Límites de carga/descarga
        constraints.append(s[t] == s[t-1] + b_in[t] - b_out[t])
        constraints.append(0 <= b_in[t])
        constraints.append(b_in[t] <= B_max * carga_flag[t])
        constraints.append(0 <= b_out[t])
        constraints.append(b_out[t] <= B_max * (1 - carga_flag[t]))
        # Límite de venta
        constraints.append(0 <= v[t])
        constraints.append(v[t] <= V_max)
        constraints.append(v[t] == produccion[t] + (s[t-1] - s[t])) 
        if produccion[t] == 0:
            constraints.append(b_in[t] == 0)
        
    # Función objetivo: maximizar beneficios
    objective = cp.Maximize(cp.sum(cp.multiply(precios, v)))

    # Resolver el problema
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.GUROBI, reoptimize=True)

    
    if graph == True:
        
        fig, ax = plt.subplots(figsize = (15,5))
        ax.bar(x = np.arange(1,25,1), height = s.value, label = 'Batería')
        ax.plot(np.arange(1,25,1),b_in.value, c = 'purple', label = 'Ingreso batería')
        ax.plot(np.arange(1,25,1),b_out.value, c = 'k', label = 'Retiro batería')
        plt.axhline(4500, c = 'r', linestyle = 'dashed', label = 'Mínimo batería inicio/final')
        plt.xticks(np.arange(1,25,1), datetime, rotation = 90)
        plt.grid()
        plt.legend()
        plt.show()

        fig, ax = plt.subplots(figsize = (15,5))
        ax.bar(x = np.arange(1,25,1), height = v.value, label = 'Venta', color = 'g')
        plt.xticks(np.arange(1,25,1), datetime, rotation = 90)
        plt.grid()
        plt.legend()
        plt.show()
        
    else:
        
        return(problem.value, v.value, s.value, b_in.value, b_out.value)

def maximize_cost_penal(precios, produccion_real, produccion, penal, S_max = 3600, S_min = 0, B_max = 1800, V_max = 4000, S_init = 1080):
    # Variables
    real = maximize_cost(precios, produccion_real, S_max = S_max, S_min = S_min, B_max = B_max, V_max = V_max, S_init = S_init)
    v_real = real[1]
    total_real = real[0]
    n = 24  # Número de horas
    v = cp.Variable(n)         # Energía vendida al mercado por hora
    b_in = cp.Variable(n)      # Energía que entra a la batería por hora
    b_out = cp.Variable(n)     # Energía que sale de la batería por hora
    s = cp.Variable(n)     # Estado de carga de la batería (incluye estado inicial)
    carga_flag = cp.Variable(n, boolean=True)
    # Restricciones
    constraints = []
        
    # Inicializar el estado de la batería
    constraints.append(s[0] == S_init)
    constraints.append(s[-1] == S_init)
    # Restricciones por hora
    for t in range(n):
        def positive_value(expr):
            try:
                cp.sqrt(expr)
                return expr
            except ValueError:
                return -expr
            
        # Límites de almacenamiento de la batería
        constraints.append(0 <= s[t])
        constraints.append(s[t] <= S_max)
        # Límites de carga/descarga
        constraints.append(s[t] == s[t-1] + b_in[t] - b_out[t])
        constraints.append(0 <= b_in[t])
        constraints.append(b_in[t] <= B_max * carga_flag[t])
        constraints.append(0 <= b_out[t])
        constraints.append(b_out[t] <= B_max * (1 - carga_flag[t]))
        # Límite de venta
        constraints.append(0 <= v[t])
        constraints.append(v[t] <= V_max)
        constraints.append(v[t] == produccion[t] + (s[t-1] - s[t]) - positive_value(penal[t]*(v_real[t] - v[t])))
        if produccion[t] == 0:
            constraints.append(b_in[t] == 0)
        
    # Función objetivo: maximizar beneficios
    objective = cp.Maximize(cp.sum(cp.multiply(precios, v)))

    # Resolver el problema
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.GUROBI, reoptimize=True)

    return(problem.value, v.value, s.value, b_in.value, b_out.value, v_real, v_real - v.value, total_real, v_real)


