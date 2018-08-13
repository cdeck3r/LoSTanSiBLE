# LoSTanSiBLE

*Low Speed Trading and Small in Budget; Large Expenses* - A data science exercise project for stock market trading.

This is an programming and machine learning, in particular deep learning, exercise. The stage of this exercise is stock market trading.

You may want to follow the project or want more information:

* [Trello board](https://trello.com/b/5fn9O35r)
* [Wiki](https://github.com/cdeck3r/LoSTanSiBLE/wiki)

## Motivation and Objective

Primary target group are traders, in particular individuals, who

* have limited time resources prohibiting them to look after their stocks
* only want to put a small amount of money at risk, and
* due to the bullet point above, experience high fees when trading. We will consider the fees as high, if the minimum transaction fee makes up a significant single digit percentage of the amount of invested capital for a stock. See [wiki](https://github.com/cdeck3r/LoSTanSiBLE/wiki/orderfees) for an example.

**Key takeaway**
> For low volume trading, the order fees reduce significantly the gross profit of the target group.

For this group of traders, LoSTanSiBLE aims to provide some algorithmic support. The objective is to make them successful at the stock market.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need the following softare preinstalled

* Docker
* Editor of your choice

### Installing

A step by step series of examples that tell you how to get a development env running
```
git clone https://github.com/cdeck3r/LoSTanSiBLE.git
cd LoSTanSiBLE
```

Build the Docker image, target is `lostansible:latest`
```
./build.sh
```

Adapt `docker run ...` command to your needs in file `lostansible.sh`. Executing the script to spin up the container.
```
./lostansible.sh bash
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

```
make test
```

## Deployment

Run LoSTanSiBLE as it is in the dev environment.  LoSTanSiBLE is intended to run on [floydhub](https://www.floydhub.com/)

## Contributing

If you like to contribute to the project, just submit a pull requests.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/cdeck3r/LoSTanSiBLE/tags).

## Authors

* Christian Decker - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

This project would not have been possible without the exceptional work of many others who have provided code .

* Jupyter and Python community
* Tensorflow and Keras community
* PurpleBooth for her [README.md template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* waleedka's [Dockerfile](https://github.com/waleedka/modern-deep-learning-docker)
* pjbull's [cookiecutter for data science](http://drivendata.github.io/cookiecutter-data-science/)

If you feel, your part is not listed here, drop me a mail.
