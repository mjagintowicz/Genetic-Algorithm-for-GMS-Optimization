dict_PL = {
    "lang": "PL",
    "general_nav_title": "Wprowadzenie",
    "units_nav_title": "Jednostki",
    "demands_nav_title": "Zapotrzebowanie",
    "costs_nav_title": "Koszty",
    "algorithm_params_nav_title": "Parametry algorytmu",

    "general_title": "Harmonogramowanie remontów jednostek wytwórczych z wykorzystaniem algorytmu genetycznego",
    "general_caption": "Witaj! (placeholder)",

    "units_header": "Dane jednostek wytwórczych",
    "units_caption": "Liczba jednostek wytwórczych odpowiada rozmiarowi instancji problemu. Domyślny rozmiar wynosi 20.",
    "units_warning": "Zmiana rozmiaru spowoduje zresetowanie wszystkich danych jednostek!",
    "units_number": "Liczba jednostek",
    "units_power": "Moc wytwarzana w okresie",

    "demands_header": "Zapotrzebowanie energetyczne w okresach",
    "period_number": "Liczba okresów",

    "costs_header": "Koszty",
    "costs_maintenance": "Koszty remontów",
    "maintenance_caption": "Koszty remontów są opisane za pomocą funkcji schodkowych. Możesz użyć domyślnych funkcji lub zdefiniować własne.",
    "costs_operation": "Koszty eksploatacji",
    "operation_caption": "Koszty eksploatacji są liniowe. Możesz dostosować współczynnik funkcji.",
    "operation_coef": "Współczynnik kosztu eksploatacji",

    "algorithm_params_header": "Parametry algorytmu",
    "population_size": "Rozmiar populacji",
    "generations": "Liczba pokoleń",
    "criterion": "Kryterium",
    "criterion_cost": "Koszt",
    "criterion_reliability": "Niezawodność",

    "selection": "Operatory selekcji",
    "selection_roulette": "Ruletka",
    "selection_tournament": "Turniej",
    "selection_rate": "Prawdopodobieństwo selekcji",

    "crossover": "Operatory krzyżowania",

    "mutation": "Operatory mutacji",
    "mutation_rate": "Prawdopodobieństwo mutacji",

    "periods_since": "Liczba okresów od ostatniej konserwacji",
    "cost": "Koszt",

    "period": "Okres",
    "unit_num": "Numer jednostki",

    "results_nav_title": "Wyniki",

    "run": "Uruchom!",
    "elitism": "Elitaryzm?",
    "fitness": "Przystosowanie",
    "best_abs": "Najlepsze dotychczasowe",
    "best_rel": "Najlepsze w generacji",

    "results": "Wyniki",

    "intro_gms": "Problem planowania konserwacji jednostek wytwórczych (ang. Generator Maintenance Scheduling, GMS) polega na optymalizacji harmonogramu prac konserwacyjnych i remontowych jednostek wytwórczych w określonym horyzoncie czasowym. Celem jest ustalenie terminów wyłączenia poszczególnych jednostek z eksploatacji na czas remontu, przy jednoczesnym zapewnieniu możliwości pokrycia wymaganego zapotrzebowania na moc. Otrzymany harmonogram powinien spełniać nałożone ograniczenia oraz minimalizować całkowity koszt związany z eksploatacją i remontami jednostek lub maksymalizować dostępną rezerwę mocy netto.",
    "about_app": "O aplikacji",
    "about_text": "Aplikacja zapewnia interaktywne środowisko do rozwiązywania problemu GMS z wykorzystaniem algorytmu genetycznego (GA). Umożliwia zdefiniowanie danych wejściowych, konfigurację algorytmu optymalizacji, wygenerowanie harmonogramu remontów oraz analizę otrzymanych wyników.",
    "instruction": "Jak to działa?",
    "instruction_text": """
                        1. **Zdefiniuj dane wejściowe**<br>
                           Wprowadź parametry jednostek wytwórczych, zapotrzebowanie na moc oraz funkcje kosztów.
                        
                        2. **Skonfiguruj algorytm**<br>
                           Ustaw parametry algorytmu genetycznego oraz wybierz odpowiednie operatory genetyczne.
                        
                        3. **Uruchom optymalizację**<br>
                           Uruchom algorytm w celu znalezienia rozwiązania o wysokiej jakości.
                        
                        4. **Przeanalizuj wyniki**<br>
                           Przeanalizuj otrzymany harmonogram oraz wartość funkcji celu.
                        """,
    "sources": "Źródła",
    "sources_urls": """
- [Matheuristics for scheduling of maintenance service with linear operation cost and step function maintenance cost](https://www.sciencedirect.com/science/article/pii/S0377221723007580)
- [A Simulated Annealing based approach to solve the generator maintenance scheduling problem](https://www.sciencedirect.com/science/article/pii/S0378779611000253)
- [Benchmarks for maintenance scheduling problems in power generation](https://www.researchgate.net/publication/260336320_Benchmarks_for_maintenance_scheduling_problems_in_power_generation)
"""
}
