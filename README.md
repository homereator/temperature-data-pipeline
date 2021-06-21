# temperature-data-pipeline

This project intends to solve a use case in which we want to acquire temperature data from the [Meteostat API](https://dev.meteostat.net/) using python.

### Environment Setup

The project was developed using a Windows 10 SO and anaconda as a version managment tool for python3, testing the complete code might require the usage of that environment since some commands of the Makefile could not work as intended.

### Installation

After downloading the repository run:

`make setup`

That would create a conda environment called temperature-pipeline that would include all the packages that are needed for the poroject, afterwards activate the environment with:

`conda activate temperature-pipeline`

This project uses a SQLite database but if the correct methods are modified it could be adapted to a different relational database.

An initial setup is needed for the database since its not recomended for it to be in the repository, the following command would create that but is necesary to remember that a .env file is required for the database setup:

`make db`

#### .env file structure

The file has limited content and the `DATABASE_LOCATION` is recomended to be `data` folder to mantain consistency but is not mandatory
```
DATABASE_LOCATION=data/[database name]
```

### Running the pipeline

To run the pipeline with the default setting is possible with

`make pipeline`

Another method to perform the same task is with the command:

`python pipeline.py`

This will perform a run gathering the historical data up until a day before today, store it in the sqlite database and perform an analysis that will end with the following files created:

```
/
└── reports/
    ├── month_avg_analysis.csv
    └── month_avg_plot.jpg
```
The csv file contains the data corresponding to the analysis of the average temperature of the Berlin / Tegel terminal for the month of february during all the years that the record exists.