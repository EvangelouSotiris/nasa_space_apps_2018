# Find My Cryosphere! Nasa Space Apps 2018 

Our focus and project for the NASA Space Apps 2018, is to provide a way for a person, a company or another kind of economical entity to monitor the cryosphere effects on their location of interest.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will first need to install gdal.

To add the repository for gdal:
```
sudo apt-add-repository ppa:ubuntugis/ubuntugis-unstable
```
You then need to update the repository list:
```
sudo apt-get update
```
And then you need to perform the installation:
```
sudo apt-get install python-gdal
```

You will then need to install geopy:
```
pip install geopy
```

Then you will need to install requests:
```
pip install requests
```

Finally, install pyproj:
```
pip install pyproj
```

### Installing

All you have to do is clone the project

```
git clone https://github.com/GiorgosNikitopoulos/nasa_space_apps_2018.git
```

## Running the software

To run the software just type:
```
python core.py
```


## Contributing

Additional details on how to contribute on this project will be uploaded shortly.


## Authors

* **Nikitopoulos Georgios** - *Developer* - [Github](https://github.com/GiorgosNikitopoulos)
* **Evangelou Sotiris** - *Developer* - [Github](https://github.com/EvangelouSotiris)

## License

This project is licensed under the GPL V3 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* The Nasa Space Apps:Thessaloniki Volunteers and Organisers 
* etc


