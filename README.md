# AiiDA Workchain
This workchain demonstrates the power of AiiDA in orchestrating and managing complex workflows for atomic calculations, offering a systematic and efficient approach to materials research and computational chemistry tasks.

## Workflow

The workflow calculates atomic properties of and relaxes the materials. It consists of six parts:

 1. **Structure builder** - It creates a material system with specific rules.

 2. **Symmetry equivalence check** - This task computes a symmetry equivalence check between the new system and the previously calculated configuration to avoid repeating the same results.

 3. **Computing procedure**: An atomic calculation task (e.g. scf, relax, vc-relax) applyed on the new system using Quantum Espresso (v.6.7).

 4. **Adapter** - This task receives the previously calculated results and convertes them into a new format (e.g. json format).

 5. **Property addition** - This task computes additional atomic properties (e.g. formation energy, redox potential) added into results.

 6. **Store data** - It stores the results in a MongoDB istance as a json document.


## **How to install**

 1. Download git repository in own directory:

```bash
    git clone https://gitlab.brindisi.enea.it/claudio.ronchetti/ai4mat.git
    cd computing # Enter in AiiDA workflow folder
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
