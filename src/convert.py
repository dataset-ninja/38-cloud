# https://www.kaggle.com/datasets/sorour/38cloud-cloud-segmentation-in-satellite-images

import os
import shutil
from urllib.parse import unquote, urlparse

import cv2
import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s
from dataset_tools.convert import unpack_if_archive


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:

    # project_name = "38-Cloud"
    train_path = "/home/grokhi/rawdata/38-cloud/38-Cloud_training"
    test_path = "/home/grokhi/rawdata/38-cloud/38-Cloud_test"

    images_subfolders = ["train_blue", "train_green", "train_nir", "train_red"]
    masks_folder = "train_gt"
    batch_size = 30
    group_tag_name = "image_id"
    masks_prefix = "gt_patch_"


    def create_ann(image_path):
        labels = []
        tags = []

        image_name = get_file_name_with_ext(image_path).split("_patch_")[1]
        channel_value = get_file_name_with_ext(image_path).split("_patch_")[0]
        id_data = get_file_name(image_name)

        tags += [sly.Tag(tag_id, value=id_data), sly.Tag(tag_channel, value=channel_value)]

        if ds_name != "test":
            mask_path = os.path.join(masks_path, masks_prefix + image_name)
            ann_np = sly.imaging.image.read(mask_path)[:, :, 0]
            obj_mask = ann_np == 255
            ret, curr_mask = connectedComponents(obj_mask.astype("uint8"), connectivity=8)
            if ret > 1:
                for i in range(1, ret):
                    obj_mask = curr_mask == i
                    curr_bitmap = sly.Bitmap(obj_mask)
                    if curr_bitmap.area > 10:
                        curr_label = sly.Label(curr_bitmap, obj_class)
                        labels.append(curr_label)

        return sly.Annotation(img_size=(384, 384), labels=labels, img_tags=tags)


    obj_class = sly.ObjClass("cloud", sly.Bitmap)

    tag_id = sly.TagMeta("image_id", sly.TagValueType.ANY_STRING)

    tag_channel = sly.TagMeta("channel", sly.TagValueType.ANY_STRING)
    group_tag_meta = sly.TagMeta(group_tag_name, sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    meta = sly.ProjectMeta(obj_classes=[obj_class], tag_metas=[group_tag_meta, tag_channel])
    # meta = meta.add_tag_meta(group_tag_meta, tag_band)
    api.project.update_meta(project.id, meta.to_json())
    api.project.images_grouping(id=project.id, enable=True, tag_name=group_tag_name)

    ds_name_to_folder = {"training": train_path, "test": test_path}

    for ds_name, data_path in ds_name_to_folder.items():
        if ds_name=='training':
            images_subfolders = ["train_blue", "train_green", "train_nir", "train_red"]
        if ds_name=='test':
            images_subfolders = ["test_blue", "test_green", "test_nir", "test_red"]
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)
        masks_path = os.path.join(data_path, masks_folder)
        for subfolder in images_subfolders:
            images_path = os.path.join(data_path, subfolder)
            images_names = os.listdir(images_path)

            progress = sly.Progress(
                "Create dataset {}, add {} data".format(ds_name, subfolder), len(images_names)
            )

            for images_names_batch in sly.batched(images_names, batch_size=batch_size):
                images_path_batch = [
                    os.path.join(images_path, image_name) for image_name in images_names_batch
                ]

                img_infos = api.image.upload_paths(dataset.id, images_names_batch, images_path_batch)
                img_ids = [im_info.id for im_info in img_infos]


                anns_batch = [create_ann(image_path) for image_path in images_path_batch]
                api.annotation.upload_anns(img_ids, anns_batch)

                progress.iters_done_report(len(images_path_batch))
    return project


