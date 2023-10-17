Dataset **38-Cloud** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/a/B/0f/BHwzzAbNfepHJctH9e4irIH4EijrElXhBZzFnrvMdNIsQG1COK0HRtjWK9JrzPnp4jiHQqqcf1BOcS8Mr8R4rii8eLLFgVqouDTJCnYc1bXOvpqAKpHoVzs7M7Up.tar)

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