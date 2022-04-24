# IART Project 1 - Optimization Methods / Meta-Heuristics
This project addresses the *Google HashCode 2021* problem, Traffic Signaling:

> Given the description of a city plan and planned paths for all cars in that city, optimize the schedule of traffic lights to minimize the total amount of time spent in traffic, and help as many cars as possible reach their destination before a given deadline.

## Members (Group 65_3A)

- Bruno Rosendo (up201906334)
- João Mesquita (up201906682)
- Rui Alves (up201905853)

## Running the program

The program was developed using Python 3, so please make sure you have the right version installed.

Run `python3 src/main.py` from the project's root folder.
At the start, the project's main page will appear:
```
#######                                          #####                                                
   #    #####    ##   ###### ###### #  ####     #     # #  ####  #    #   ##   #      # #    #  ####  
   #    #    #  #  #  #      #      # #    #    #       # #    # ##   #  #  #  #      # ##   # #    # 
   #    #    # #    # #####  #####  # #          #####  # #      # #  # #    # #      # # #  # #      
   #    #####  ###### #      #      # #               # # #  ### #  # # ###### #      # #  # # #  ### 
   #    #   #  #    # #      #      # #    #    #     # # #    # #   ## #    # #      # #   ## #    # 
   #    #    # #    # #      #      #  ####      #####  #  ####  #    # #    # ###### # #    #  #### 

Welcome to the Google Hashcode 2021 Solver, developed for the Artificial Intelligence course
Press enter to get started...
```

After clicking on `Enter`, the configuration menu will appear. Here, it's possible to set the input/output files, the maximum time or iterations and change how the initial solution is calculated:

```
General Configuration

********************************************************
1. Set Input File              ------   An example (A)
2. Set Output File             ------   out
3. Set Max Num Iterations      ------   inf
4. Set Max Execution Time      ------   120 secs
5. Show Final Solution
6. Remove Unused Streets
7. Choose Algorithm
8. Go to Main Menu
********************************************************
Insert option from the menu:
```

For example, the input file configuration menu looks like the following:

```
Choose Input File

********************************************************
1. An example (A)
2. By the ocean (B)
3. Checkmate (C)
4. Daily commute (D)
5. Etoile (E)
6. Forever jammed (F)
7. Custom Input 1
8. Custom Input 2
********************************************************
Insert option from the menu:
```

Then, we can choose the algorithm with which we want to solve the hashcode problem, by selecting the option `7`:

```
Choose Algorithm

********************************************************
1. Hill Climbing Basic Random
2. Hill Climbing Steepest Ascent
3. Simulated Annealing
4. Tabu Search
5. Generational Genetic
6. Steady State Genetic
7. Set General Configurations
8. Go to Main Menu
********************************************************
Insert option from the menu:
```

Some of the algorithms offer extra configurations, while others do not need such configuration. For example, let's choose the `Simulated Annealing` algorithm:

```
Configure Simulated Annealing

********************************************************
1. Set Initial Temperature     ------   100
2. Set Cooling alpha Constant  ------   0.85
3. Set Temperature Precision   ------   10 decimal cases
4. Set Cooling Schedule        ------   exponentialCooling
5. Run Simulated Annealing
6. Choose Algorithm
********************************************************
Insert option from the menu:
```

And let's try changing the cooling schedule:

```
Choose Cooling Schedule

********************************************************
1. Exponential Cooling ( 0.8 <= alpha <= 0.9 ) 
 T = T0 * (alpha ^ k)
2. Logarithmical Cooling ( alpha > 1 ) 
 T = T0 / (1 + alpha * ln(1 + k))
3. Linear Cooling ( alpha > 0 ) 
 T = T0 / (1 + alpha * k) 
4. Quadratic Cooling ( alpha > 0 ) 
 T = T0 / (1 + alpha * (k ^ 2)) 
********************************************************
Insert option from the menu: 3
```

We can then run the algorithm. During the execution, some information will be displayed, telling the user how the solution is evolving:

```
Configure Simulated Annealing

********************************************************
1. Set Initial Temperature     ------   100
2. Set Cooling alpha Constant  ------   1
3. Set Temperature Precision   ------   10 decimal cases
4. Set Cooling Schedule        ------   linearCooling
5. Run Simulated Annealing
6. Choose Algorithm
********************************************************
Insert option from the menu: 5
Simulated Annealing iteration 6075 at 1.5º with: 2002 points (3.45 seconds)
```

We can then see the result displayed, according to the user's initial configuration:

```
| Intersection 0 |
[rue-de-londres (2)]
| Intersection 1 |
[rue-d-athenes (1), rue-d-amsterdam (4)]
| Intersection 2 |
[rue-de-moscou (0)]
| Intersection 3 |
[rue-de-rome (4)]
Final score =  2002
Press enter to go back...
```


## Changing the default configuration

The program's configuration is present at `src/config.py`. There, it's possible to change the configuration's default values, change input and output folders, and add additional input files. However, we recommend that you change the configurations in the program's interface instead.
