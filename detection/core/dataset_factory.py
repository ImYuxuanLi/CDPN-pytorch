"""
Register datasets in this file
will be imported in project root to register the datasets
"""
import logging
import os.path as osp

import mmcv

# import ref
from detectron2.data import DatasetCatalog
from core.datasets import (lm_dataset_d2, lm_pbr, lmo_bop_test,
    ycbv_pbr, ycbv_bop_test, ycbv_d2,
    tless_pbr, tless_train_primesense_fuse, tless_bop_test,
    icbin_pbr, icbin_bop_test,
    tudl_pbr, tudl_bop_test, tudl_d2,
    hb_pbr, hb_bop_test, hb_d2,
    itodd_pbr, itodd_bop_test, itodd_d2)

cur_dir = osp.dirname(osp.abspath(__file__))

# from lib.utils.utils import iprint

__all__ = ["register_dataset", "register_datasets", "register_datasets_in_cfg", "get_available_datasets"]

_DSET_MOD_NAMES = [
    "lm_dataset_d2", "lm_pbr", "lmo_bop_test",
    'ycbv_pbr', 'ycbv_bop_test', 'ycbv_d2',
    'tless_pbr', 'tless_bop_test', 'tless_train_primesense_fuse',
    "icbin_pbr", "icbin_bop_test",
    "tudl_pbr", "tudl_bop_test", "tudl_d2",
    'hb_pbr', 'hb_bop_test', 'hb_d2',
    "itodd_pbr", "itodd_bop_test", "itodd_d2",
]

logger = logging.getLogger(__name__)


def register_dataset(mod_name, dset_name, data_cfg=None):
    """
    mod_name: a module under core.datasets or other dataset source file imported here
    dset_name: dataset name
    data_cfg: dataset config
    """
    register_func = eval(mod_name)
    register_func.register_with_name_cfg(dset_name, data_cfg)


def get_available_datasets(mod_name):
    return eval(mod_name).get_available_datasets()


def register_datasets_in_cfg(cfg):
    for split in ["TRAIN", "TEST", "SS_TRAIN", "TEST_DEBUG", "TRAIN_REAL", "TRAIN_SYN_SUP"]:
        for name in cfg.DATASETS.get(split, []):
            if name in DatasetCatalog.list():
                continue
            registered = False
            # try to find in pre-defined datasets
            # NOTE: it is better to let all datasets pre-refined
            for _mod_name in _DSET_MOD_NAMES:
                if name in get_available_datasets(_mod_name):
                    register_dataset(_mod_name, name, data_cfg=None)
                    registered = True
                    break
            # not in pre-defined; not recommend
            if not registered:
                # try to get mod_name and data_cfg from cfg
                """load data_cfg and mod_name from file
                cfg.DATA_CFG[name] = 'path_to_cfg'
                """
                assert "DATA_CFG" in cfg and name in cfg.DATA_CFG, "no cfg.DATA_CFG.{}".format(name)
                assert osp.exists(cfg.DATA_CFG[name])
                data_cfg = mmcv.load(cfg.DATA_CFG[name])
                mod_name = data_cfg.pop("mod_name", None)
                assert mod_name in _DSET_MOD_NAMES, mod_name
                register_dataset(mod_name, name, data_cfg)


def register_datasets(dataset_names):
    for name in dataset_names:
        if name in DatasetCatalog.list():
            continue
        registered = False
        # try to find in pre-defined datasets
        # NOTE: it is better to let all datasets pre-refined
        for _mod_name in _DSET_MOD_NAMES:
            if name in get_available_datasets(_mod_name):
                register_dataset(_mod_name, name, data_cfg=None)
                registered = True
                break
        # not in pre-defined; not recommend
        if not registered:
            raise ValueError(f"dataset {name} is not defined")
