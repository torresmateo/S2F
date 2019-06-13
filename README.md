# S2F (Sequence to Function)

A protein function prediction tool that takes only the sequences as input

* [Installation](#installation)
* [How to make a prediction](#how-to-make-a-prediction)

## Requirements

S2F relies on the following software:

* BLAST (`blastp` and `makeblastdb`)
* InterPro (`iprscan`)
* HMMer (`phmmer`)
* Python 3

S2F relies on several Python 3 packages. A script is provided that will install all the requirements simply by
running:

```bash
./install_requirements.sh
```

If you prefer to setup a `virtualenv` to use S2F, first create it, and then run the script passing the path to the python interpreter within that `virtualenv` to the script:

```bash
./install_requirements.sh ~/.virtualenvs/s2f/bin/python
```

this will also generate a script named `S2F.sh` and configure it accordingly

## Installation

A one-command solution is available to setup the entire environment for S2F (this will download HUNDREDS of GB of datasets, please look below to [configure the installer](#configure-the-installation-script) according to your needs, or the [command line options](#installer-options)). 
You may simply run:
```bash
python S2F.py install
```
You will be asked to confirm the configured options of the installation script. If you're happy and reply with `y`, the installer will download and process the required databases. This, however, assumes that all requirements listed above are met. 

### Configure the installation script

The easiest way to configure the installation is through the configuration file. The default values are:

```ini
[directories]
installation_directory = ~/.S2F

[commands]
interpro = iprscan
hmmer = phmmer
blastp = blastp
makeblastdb = makeblastdb

[databases]
string_links = download
string_sequences = download
string_species = download
uniprot_sprot = download
uniprot_goa = download
filtered_goa = infer
filtered_sprot = infer

[options]
evidence_codes = experimental
```

A description of each option is provided in the following table:

| Option | Description |
| --- | --- |
| `installation_directory` | Path to the installation directory for S2F. |
| `interpro` | manually provide the path to the `iprscan` executable to avoid passing this parameter to the other commands every time. |
| `hmmer` | manually provide the path to the `phmmer` executable to avoid passing this parameter to the other commands every time. |
| `blastp` | manually provide the path to the `blastp` command in the system. If not provided, S2F will assume that the executable is available system-wide. |
| `makeblastdb` | manually provide the path to the `makeblastdb` command in the system. If not provided, S2F will assume that the executable is available system-wide. |
| `string_links` | 'manually provide the path to the STRING interactions database, it must be the full path to either `protein.links.full.vX.x.txt.gz` or `protein.links.detailed.vX.x.txt.gz`. If not provided, the installation script will attempt to download the full database using the `wget` command.' |
| `string_sequences` | manually provide the path to the STRING sequences database, it must be the full path to the `protein.sequences.vX.x.fa.gz` file. If not provided, the installation script will attempt to download it using the `wget` command.' |
| `string_species` | manually provide the path to the STRIN species list, it must be the full path to the `species.vX.x.txt` file. If not provided, the installation script will attempt to download it using the `wget` command. |
| `uniprot_sprot` | manually provide the path to the UniProt SwissProt sequences, it must be the full path to the "goa_uniprot_all.gaf.gz" file. If not provided, the installation script will attempt to download it using the `wget` command. |
| `uniprot_goa` | manually provide the path to the UniProt GOA, it must be the full path to the "goa_uniprot_all.gaf.gz" file. If not provided, the installation script will attempt to download it using the `wget` command. |
| `evidence_codes` | manually provide a list of evidence codes that will be used to filter the UniProt GOA. If not provided, S2F will be installed using only experimental evidence codes. |

### Installer options

The command line options for the installation are the following (but we highly recommend having a look at the [configuration file](#configure-the-installation-script) to avoid mistakes):

| Option | Description | Default Value |
| --- | --- | --- |
| `--installation-directory` | Path to the installation directory for S2F. | `~/.S2F` |
| `--config-file` | location of the configuration file that will be created. If not provided, the default configuration file will be loaded. | `s2f.conf` (found in the script's directory) |
| `--interpro` | manually provide the path to the `iprscan` executable to avoid passing this parameter to the other commands every time. | `iprscan` (assumes this is correctly configured in the `PATH` environment variable) |
| `--hmmer` | manually provide the path to the `phmmer` executable to avoid passing this parameter to the other commands every time. | `phmmer` (assumes this is correctly configured in the `PATH` environment variable) |
| `--blastp` | manually provide the path to the `blastp` command in the system. If not provided, S2F will assume that the executable is available system-wide. | `blastp` (assumes this is correctly configured in the `PATH` environment variable) |
| `--makeblastdb` | manually provide the path to the `makeblastdb` command in the system. If not provided, S2F will assume that the executable is available system-wide. | `makeblastdb` (assumes this is correctly configured in the `PATH` environment variable) |
| `--string-links` | 'manually provide the path to the STRING interactions database, it must be the full path to either `protein.links.full.vX.x.txt.gz` or `protein.links.detailed.vX.x.txt.gz`. If not provided, the installation script will attempt to download the full database using the `wget` command.' | `download` |
| `--string-sequences` | manually provide the path to the STRING sequences database, it must be the full path to the `protein.sequences.vX.x.fa.gz` file. If not provided, the installation script will attempt to download it using the `wget` command.' | `download` |
| `--string-species` | manually provide the path to the STRIN species list, it must be the full path to the `species.vX.x.txt` file. If not provided, the installation script will attempt to download it using the `wget` command. | `download` |
| `--uniprot-swissprot` | manually provide the path to the UniProt SwissProt sequences, it must be the full path to the "goa_uniprot_all.gaf.gz" file. If not provided, the installation script will attempt to download it using the `wget` command. | `download` |
| `--uniprot-goa` | manually provide the path to the UniProt GOA, it must be the full path to the "goa_uniprot_all.gaf.gz" file. If not provided, the installation script will attempt to download it using the `wget` command. | `download` |
| `--evidence-codes` | manually provide a list of evidence codes that will be used to filter the UniProt GOA. If not provided, S2F will be installed using only experimental evidence codes. | `experimental` |


## How to make a prediction

### Using a configuration file

Due to the number of parameters that can be set for S2F, the easiest way to running it is to create a configuration file, which should then be provided to the `predict` 
command using the `--run-config` argument:

```bash
./S2F.sh predict --run-config my_organism.conf
```

An example configuration file is provided with the default values:

```ini
[configuration]
config_file = ~/.s2f.conf
alias = test
obo = ~/go.obo
fasta = ~/test.fasta
cpu = infer

[graphs]
combined_graph = compute
graph_collection = compute
homology_graph = compute

[seeds]
interpro_output = compute
hmmer_output = compute

[blacklists]
hmmer_blacklist = compute
transfer_blacklist = compute

[functions]
goa_clamp = compute
```

A description of each option is provided in the following table:

| Option | Description |
| --- | --- |
| `config_file` | location of the installation configuration file that will be loaded. If not provided, the default configuration file will be loaded |
| `alias`| Name of the prediction run |
| `obo`| Path to the `go.obo` file to use |
| `fasta`| Path to the protein sequence file |
| `cpu`| Number of CPUs to use for parallelisable computations |
| `transfer_blacklist`| a list of identifiers from which no transference will be done |
| `hmmer_blacklist` | a list of identifiers that will be ignored from the HMMer result list |
| `graph_collection` | provide a STRING graph collection manually to avoid building one |
| `combined_graph` | manually provide a combined graph to avoid its construction (overwrites `graph_collection`) |
| `homology_graph` | manually provide a homology graph file, avoiding its computation |
| `interpro_output`| manually provide InterPro output file and therefore avoid its computation |
| `hmmer_output`| manually provide HMMer output file and therefore avoid its computation |
| `goa_clamp` | provide a set of ground truth functional associations, these associations will be clamped (set to `1`) into the diffusion seed. The format of this file is: `PROTEIN_ID<tab>GO_ID` |


### Predict command line options

If preferred, the options listed above are also supported as command line arguments.

| Option | Description | Default Value |
| --- | --- | --- |
| `--run-config` | path to the run configuration file (**overrides all other arguments**)
| `--config-file` | location of the installation configuration file that will be loaded. If not provided, the default configuration file will be loaded | `s2f.conf` (found in the script's directory) |
| `--alias`| Name of the prediction run ||
| `--obo`| Path to the `go.obo` file to use ||
| `--fasta`| Path to the protein sequence file ||
| `--cpu`| Number of CPUs to use for parallelisable computations | `infer` |
| `--interpro-output`| manually provide InterPro output file and therefore avoid its computation | `compute` |
| `--hmmer-output`| manually provide HMMer output file and therefore avoid its computation | `compute` |
| `--transfer-blacklist`| a list of identifiers from which no transference will be done | |
| `--hmmer-blacklist` | a list of identifiers that will be ignored from the HMMer result list | `compute` |
| `--graph-collection` | provide a STRING graph collection manually to avoid building one | `compute` |
| `--combined-graph` | manually provide a combined graph to avoid its construction (overwrites `--graph-collection`) | `compute` |
| `--homology-graph` | manually provide a homology graph file, avoiding its computation | `compute` |
| `--goa-clamp` | provide a set of ground truth functional associations, these associations will be clamped (set to `1`) into the diffusion seed. The format of this file is: `PROTEIN_ID<tab>GO_ID` | `compute` |
