# -*- coding: utf-8 -*-
import os
import random
import pickle
import cv2
from ..dataset.coco_parser import COCOParser
from ..dataset.dataset import Dataset


def pack(image_root_path, pack_save_path, mode='train'):
    assert os.path.exists(image_root_path), 'image root path does not exist!'
    assert pack_save_path.lower().endswith('.pkl'), 'the required suffix is .pkl!'
    assert mode in ['train', 'val'], 'the valid mode: train, val'

    if not os.path.exists(os.path.dirname(pack_save_path)):
        os.makedirs(os.path.dirname(pack_save_path))

    annotation_path = os.path.join(os.path.dirname(__file__), '../../datasets/coco/instances_' + mode + '2017.json')

    parser = COCOParser(image_root=image_root_path, coco_annotation_path=annotation_path)

    dataset = Dataset(parser, save_path=pack_save_path)

    print(dataset)


def pack_mini_for_debug(val_pkl_path, mini_pkl_save_path):
    """
    get a mini dataset for debug based on existed pkl files
    :return:
    """
    assert os.path.exists(val_pkl_path), 'val pkl path does not exist!'

    if not os.path.exists(os.path.dirname(mini_pkl_save_path)):
        os.makedirs(os.path.dirname(mini_pkl_save_path))

    meta_info, index_annotation_dict, dataset = pickle.load(open(val_pkl_path, 'rb'))

    new_index_annotation_dict = dict()
    new_dataset = dict()

    keys = list(index_annotation_dict.keys())
    random.shuffle(keys)
    selected_keys = keys[:320]

    for key in selected_keys:
        new_index_annotation_dict[key] = index_annotation_dict[key]
        new_dataset[key] = dataset[key]

    pickle.dump([meta_info, new_index_annotation_dict, new_dataset], open(mini_pkl_save_path, 'wb'), pickle.HIGHEST_PROTOCOL)


def check(pkl_path):
    assert os.path.exists(pkl_path), 'pkl path does not exist!'

    dataset = Dataset(load_path=pkl_path)
    print(dataset)

    index_annotation_dict = dataset.index_annotation_dict
    category_ids_to_label_indexes, label_indexes_to_category_ids, category_ids_to_category_names = dataset.meta_info

    for index, annotation in index_annotation_dict.items():
        sample = dataset[index]
        image = cv2.imread(sample['image_path'], cv2.IMREAD_COLOR)
        if 'bboxes' in sample:
            bboxes = sample['bboxes']
            bbox_labels = sample['bbox_labels']
            for i, bbox in enumerate(bboxes):
                cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), (0, 255, 0), 2)
        cv2.imshow('image', image)
        cv2.waitKey()

