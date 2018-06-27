"""
..  module:: tasks.py
    :synopsis: Module to import all the functions that run as Celery tasks.
"""
from __future__ import absolute_import

from celery import shared_task  # pylint: disable=unused-import

from remapp.exports.mg_export import exportMG2excel  # pylint: disable=unused-import
from remapp.exports.ct_export import ctxlsx, ct_csv  # pylint: disable=unused-import
from remapp.exports.mg_csv_nhsbsp import mg_csv_nhsbsp  # pylint: disable=unused-import
from remapp.exports.dx_export import exportDX2excel, dxxlsx  # pylint: disable=unused-import
from remapp.exports.rf_export import exportFL2excel, rfxlsx  # pylint: disable=unused-import
from remapp.extractors.ct_philips import ct_philips  # pylint: disable=unused-import
from remapp.extractors.dx import dx  # pylint: disable=unused-import
from remapp.extractors.mam import mam  # pylint: disable=unused-import
from remapp.extractors.rdsr import rdsr  # pylint: disable=unused-import
from remapp.extractors.ptsizecsv2db import websizeimport  # pylint: disable=unused-import
from remapp.netdicom.qrscu import qrscu, movescu  # pylint: disable=unused-import
from remapp.netdicom.keepalive import keep_alive  # pylint: disable=unused-import
from remapp.tools.make_skin_map import make_skin_map  # pylint: disable=unused-import
