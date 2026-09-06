dict_ENG = {
    "lang": "ENG",
    "general_nav_title": "Introduction",
    "units_nav_title": "Units",
    "demands_nav_title": "Demand",
    "costs_nav_title": "Costs",
    "algorithm_params_nav_title": "Algorithm Parameters",

    "general_title": "Generator Maintenance Scheduling with Genetic Algorithm",
    "general_caption": "Hello! (placeholder)",

    "units_header": "Generating units data",
    "units_caption": "The number of generating units corresponds with the problem instance size. The default size is 20.",
    "units_warning": "Changing the size will reset all the units data!",
    "units_number": "Number of units",

    "demands_header": "Power demand data",
    "period_number": "Number of periods",

    "costs_header": "Costs",
    "costs_maintenance": "Maintenance cost",
    "maintenance_caption": "Maintenance costs are described by step functions. Use the default functions or define your own.",
    "costs_operation": "Operation cost",
    "operation_caption": "Operation costs are linear. You can adjust the function coefficient.",
    "operation_coef": "Operation cost coefficient",

    "algorithm_params_header": "Algorithm Parameters",
    "population_size": "Population size",
    "generations": "Number of generations",
    "criterion": "Criterion",
    "criterion_cost": "Cost",
    "criterion_reliability": "Reliability",

    "selection": "Selection operators",
    "selection_roulette": "Roulette",
    "selection_tournament": "Tournament",
    "selection_rate": "Selection rate",

    "crossover": "Crossover operators",

    "mutation": "Mutation operators",
    "mutation_rate": "Mutation rate",

    "periods_since": "Periods since last maintenance",
    "cost": "Cost",

    "period": "Period",
    "unit_num": "Unit number",

    "results_nav_title": "Results",

    "run": "Run!",
    "elitism": "Elitism?",
    "fitness": "Fitness",
    "best_abs": "Best overall fitness",
    "best_rel": "Best fitness per generation",

    "results": "Results",

    "intro_gms": "Generator Maintenance Scheduling (GMS) aims to optimize a maintenance schedule for generating units over a specified planning horizon. The goal is to determine when individual units should be taken out of operation for maintenance while ensuring that the required power demand can be met. The resulting schedule should satisfy the imposed constraints while minimizing the total cost associated with the operation and maintenance of generating units or maximizing the generated power nett reserve.",
    "about_app": "About the application",
    "about_text": "This application provides an interactive environment for solving GMS Problem using a Genetic Algorithm (GA). It allows users to define the input data, configure the optimization algorithm, generate a maintenance schedule, and analyze the obtained results.",
    "instruction": "How does it work?",
    "instruction_text": """
                        1. **Define input data**<br>
                         Enter the parameters of generating units, power demand, and cost functions. 
                         
                        2. **Configure the algorithm**<br>
                         Set the GA parameters and select the desired genetic operators. 
                         
                        3. **Run optimization**<br>
                         Run the algorithm to search for a high-quality maintenance schedule. 
                         
                        4. **Analyze results**<br>
                         Examine the resulting schedule and objective function value.
                        """,
    "sources": "Based on",
    "sources_urls": """
                    - [Matheuristics for scheduling of maintenance service with linear operation cost and step function maintenance cost](https://www.sciencedirect.com/science/article/pii/S0377221723007580)
                    - [A Simulated Annealing based approach to solve the generator maintenance scheduling problem](https://www.sciencedirect.com/science/article/pii/S0378779611000253)
                    - [Benchmarks for maintenance scheduling problems in power generation](https://www.researchgate.net/publication/260336320_Benchmarks_for_maintenance_scheduling_problems_in_power_generation)
                    """,
    "saved": "Saved.",
    "running": "Running...",
    "done": "Done!",

    "schedule": "Maintenance Schedule",
    "objective": "Objective Function",
    "results_missing": "Run the algorithm to get your schedule.",

    "power": "Power",
    "demand": "Demand",
    "power_gen": "Power generated",

}
