# AiiDA Workchain
This workchain demonstrates the power of AiiDA in orchestrating and managing complex workflows for atomic calculations, offering a systematic and efficient approach to materials research and computational chemistry tasks.

## Workflow

* `Part 1 - System Creation`
  
  In the first step, this workchain creates a material system using specific rules and parameters. It defines the atomic structure and other relevant properties required for subsequent calculations. This step ensures the setup of a consistent input for Quantum Espresso calculations.

* `Part 2 - Symmetry Equivalence Check`
  
  The second step checks for symmetric equivalence between the newly created material system and previously computed systems. This check is essential to prevent redundant calculations and ensure that identical results are not repeated unnecessarily. It leverages symmetry information to identify equivalences.

* `Part 3 - Atomic Calculation with Quantum Espresso`
  
  Upon confirming the absence of symmetrically equivalent systems, the workchain proceeds with the execution of atomic calculations using the Quantum Espresso plugin. It performs electronic structure calculations, optimizing the system's atomic positions and obtaining relevant properties like energy and forces.

* `Part 4 - Results Formatting to JSON`
  
  Following the atomic calculations, the fourth step adapts the obtained results into a structured JSON format. This format makes it easier to handle and share the data, enabling further analysis and visualization of the calculated properties.

* `Part 5 - External Database Storage`
  
  In the final step, the workchain stores the adapted results into an external database separate from the AiiDA infrastructure, such as MongoDB. This step ensures data persistence and allows for easy retrieval and integration of the calculated atomic properties into other applications or systems.

* `Overall Workflow`
  
  The Quantum Espresso Atomic Calculation Workchain is designed to automate and streamline the process of performing atomic calculations for materials. It begins by defining the material system, checks for symmetry equivalence to avoid redundancy, executes Quantum Espresso calculations, formats the results into JSON, and finally stores the results in an external database. This workflow ensures the efficient and organized handling of atomic calculations, making them accessible for further analysis and integration into external systems.

* `Use Cases`

    - Materials science research
    - Computational chemistry
    - Electronic structure calculations
    - High-throughput materials screening


## **How to install**

 1. Download git repository in own directory:

```bash
    git clone https://gitlab.brindisi.enea.it/claudio.ronchetti/ai4mat.git
```

 2. Set MongoDB authentication user and password in the `mongodb.properties` properties file. The user **MUST HAVE** the writing permits.

> **Note:** AiiDA must be installed on the computer.

## **Which computer to select** 

See _How to setup a computer_ [guide](https://aiida.readthedocs.io/projects/aiida-core/en/v1.1.0/get_started/computers.html#computer-setup-and-configuration) and _How to setup a code_ [guide](https://aiida.readthedocs.io/projects/aiida-core/en/v1.1.0/get_started/codes.html) for more details.

## **How to run** 

Once downloaded the project and set up the MongoDB authentication, you can use the AiiDA workflow by running the `python main.py` command.

The main.py script has following command line interface:

~~~
usage: main.py [-h] [-cp CALCULATION_PARAMS] [-mp MONGODB_PROPERTIES] [-xyz COORDINATES] [--default_generator]

AI4MAT - AiiDA Workflow

optional arguments:
  -h, --help            show this help message and exit
  -cp CALCULATION_PARAMS, --calculation-params CALCULATION_PARAMS
                        Path of the calculation parameters
  -mp MONGODB_PROPERTIES, --mongodb-properties MONGODB_PROPERTIES
                        Path of the MongoDB properties
  -xyz COORDINATES, --coordinates COORDINATES
                        Path of the material coordinates
  --default_generator   If true the structure generator function returns the same input structure otherwise the random structure

~~~

Now, you should be able to run the main python script:

~~~bash
python main.py -cp <PARAMETERS_FILE> -mp <CONNECTION_FILE> -xyz <XYZ_FILE>
~~~

## How to set parameters

The parameters' file allows you to customize the hyper-parameters of workflow.
This page describes all parameters you can set up.

| Parameter name | Description | Note |
| --- | ------- | --- |
| **parameters** | It contains the Quantum ESPRESSO _pw_ input ([link](computing/workchain.py) for details) |  |
| **kpoints** | Define the kpoints _mesh_ and _value_ |  |
| **pseudos** | Define the _UPF file_ for each elements of the material | It isn't required |
| **metadata.options.resources** | Define the cores' number with _tot_num_mpiprocs_ | |
| **metadata.options.queue_name** | Define the LSF queue to submit the Quantum ESPRESSO calculation | |
| **metadata.options.prepend_text**  | Define the pre-runned commands | |
| **metadata.options.append_text** | Define the post-runned commands | |
| **parallelization** | Define the parallelization level with _pool_ | Default value: 1 |
| **codename** | It contains the _code_ and the _computer_ running the workflow | The format is code@computer |
| **rules** | It's the list of rules called in the material structure generator step | Choices: ['sodium_removing' , 'manganese_replacement', 'all_sodium_removing']. Default value: ['manganese_replacement']  |
| **manganese_replacement_step** | It's the step of replacements for each elements | Default value: 2 |
| **manganese_min_number** | It's the minimum number of the manganese atoms in the system | Default value: `int(len(Mn_idx)/2)` (almost 50% of manganese atoms) |
| **transaction_metals** | It's the list of transaction metals used in the manganese replacement rule | Default value: ['Ni', 'Ti'] | 
