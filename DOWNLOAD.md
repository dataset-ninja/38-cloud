Dataset **38-Cloud** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/Y/C/i2/xGaSjhnHFBcv2KqDbdw5j02bidDbglcc7qdSlcqIRpjv6E6EKeZUSrC3ygK8dgKYA0ys3W6RbOGkwmAH6aJIBPNcuYsj50enFo7eZy7ccRkcWH1RgPmHDNN6aU2O.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='38-Cloud', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/sorour/38cloud-cloud-segmentation-in-satellite-images/download?datasetVersionNumber=4).