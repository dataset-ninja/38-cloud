**38-Cloud: Cloud Segmentation in Satellite Images** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the geospatial and environmental domains. 

The dataset consists of 70404 images with 292496 labeled objects belonging to 1 single class (*cloud*).

Images in the 38-Cloud dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. There are 51484 (73% of the total) unlabeled images (i.e. without annotations). There are 2 splits in the dataset: *test* (36804 images) and *training* (33600 images). Additionally, every one-channel image grouped by its ***image_id*** and ***channel*** tag. Explore them in supervisely advanced labeling tool. The dataset was released in 2018 by the Simon Fraser University, Canada.

<img src="https://github.com/dataset-ninja/38-cloud/raw/main/visualizations/poster.png">
