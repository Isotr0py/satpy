#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Satpy developers
#
# This file is part of satpy.
#
# satpy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# satpy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# satpy.  If not, see <http://www.gnu.org/licenses/>.
"""Demo data download for VIIRS SDR HDF5 files."""

import os
import logging
import requests

from satpy import config

logger = logging.getLogger(__name__)
ZENODO_BASE_URL = "https://zenodo.org/api/files/6aae2ac7-5e8e-4a42-96d0-393ad6a620ea/"
GDNBO_URLS = [
    "GDNBO_npp_d20170128_t1230144_e1231386_b27228_c20170128123806232923_cspp_dev.h5",
    "GDNBO_npp_d20170128_t1231398_e1233040_b27228_c20170128123931141440_cspp_dev.h5",
    "GDNBO_npp_d20170128_t1233052_e1234294_b27228_c20170128124058766619_cspp_dev.h5",
    "GDNBO_npp_d20170128_t1234306_e1235548_b27228_c20170128124307612305_cspp_dev.h5",
    "GDNBO_npp_d20170128_t1235560_e1237184_b27228_c20170128124429250510_cspp_dev.h5",
    "GDNBO_npp_d20170128_t1237197_e1238439_b27228_c20170128124604860922_cspp_dev.h5",
    "GDNBO_npp_d20170128_t1238451_e1240093_b27228_c20170128124804684300_cspp_dev.h5",
    "GDNBO_npp_d20170128_t1240105_e1241347_b27228_c20170128124931597063_cspp_dev.h5",
    "GDNBO_npp_d20170128_t1241359_e1243001_b27228_c20170128125104219695_cspp_dev.h5",
    "GDNBO_npp_d20170128_t1243013_e1244238_b27228_c20170128125239512908_cspp_dev.h5",
]
GITCO_URLS = [
    "GITCO_npp_d20170128_t1230144_e1231386_b27228_c20170128123806844060_cspp_dev.h5",
    "GITCO_npp_d20170128_t1231398_e1233040_b27228_c20170128123931757165_cspp_dev.h5",
    "GITCO_npp_d20170128_t1233052_e1234294_b27228_c20170128124059393347_cspp_dev.h5",
    "GITCO_npp_d20170128_t1234306_e1235548_b27228_c20170128124308254991_cspp_dev.h5",
    "GITCO_npp_d20170128_t1235560_e1237184_b27228_c20170128124429909006_cspp_dev.h5",
    "GITCO_npp_d20170128_t1237197_e1238439_b27228_c20170128124605535586_cspp_dev.h5",
    "GITCO_npp_d20170128_t1238451_e1240093_b27228_c20170128124805310389_cspp_dev.h5",
    "GITCO_npp_d20170128_t1240105_e1241347_b27228_c20170128124932240716_cspp_dev.h5",
    "GITCO_npp_d20170128_t1241359_e1243001_b27228_c20170128125104876016_cspp_dev.h5",
    "GITCO_npp_d20170128_t1243013_e1244238_b27228_c20170128125240141821_cspp_dev.h5",
]
GMTCO_URLS = [
    "GMTCO_npp_d20170128_t1230144_e1231386_b27228_c20170128123807370375_cspp_dev.h5",
    "GMTCO_npp_d20170128_t1231398_e1233040_b27228_c20170128123932277110_cspp_dev.h5",
    "GMTCO_npp_d20170128_t1233052_e1234294_b27228_c20170128124059920205_cspp_dev.h5",
    "GMTCO_npp_d20170128_t1234306_e1235548_b27228_c20170128124308776985_cspp_dev.h5",
    "GMTCO_npp_d20170128_t1235560_e1237184_b27228_c20170128124430441905_cspp_dev.h5",
    "GMTCO_npp_d20170128_t1237197_e1238439_b27228_c20170128124606068231_cspp_dev.h5",
    "GMTCO_npp_d20170128_t1238451_e1240093_b27228_c20170128124805827641_cspp_dev.h5",
    "GMTCO_npp_d20170128_t1240105_e1241347_b27228_c20170128124932760643_cspp_dev.h5",
    "GMTCO_npp_d20170128_t1241359_e1243001_b27228_c20170128125105397710_cspp_dev.h5",
    "GMTCO_npp_d20170128_t1243013_e1244238_b27228_c20170128125240670869_cspp_dev.h5",
]
SVDNB_FILES = [
    "SVDNB_npp_d20170128_t1230144_e1231386_b27228_c20170128123806052274_cspp_dev.h5",
    "SVDNB_npp_d20170128_t1231398_e1233040_b27228_c20170128123930950786_cspp_dev.h5",
    "SVDNB_npp_d20170128_t1233052_e1234294_b27228_c20170128124058573341_cspp_dev.h5",
    "SVDNB_npp_d20170128_t1234306_e1235548_b27228_c20170128124307412059_cspp_dev.h5",
    "SVDNB_npp_d20170128_t1235560_e1237184_b27228_c20170128124429036820_cspp_dev.h5",
    "SVDNB_npp_d20170128_t1237197_e1238439_b27228_c20170128124604651619_cspp_dev.h5",
    "SVDNB_npp_d20170128_t1238451_e1240093_b27228_c20170128124804485537_cspp_dev.h5",
    "SVDNB_npp_d20170128_t1240105_e1241347_b27228_c20170128124931392535_cspp_dev.h5",
    "SVDNB_npp_d20170128_t1241359_e1243001_b27228_c20170128125104024324_cspp_dev.h5",
    "SVDNB_npp_d20170128_t1243013_e1244238_b27228_c20170128125239325940_cspp_dev.h5",
]
SVI01_FILES = [
    "SVI01_npp_d20170128_t1230144_e1231386_b27228_c20170128123807637119_cspp_dev.h5",
    "SVI01_npp_d20170128_t1231398_e1233040_b27228_c20170128123932561605_cspp_dev.h5",
    "SVI01_npp_d20170128_t1233052_e1234294_b27228_c20170128124100227434_cspp_dev.h5",
    "SVI01_npp_d20170128_t1234306_e1235548_b27228_c20170128124309038634_cspp_dev.h5",
    "SVI01_npp_d20170128_t1235560_e1237184_b27228_c20170128124430720302_cspp_dev.h5",
    "SVI01_npp_d20170128_t1237197_e1238439_b27228_c20170128124606429178_cspp_dev.h5",
    "SVI01_npp_d20170128_t1238451_e1240093_b27228_c20170128124806092384_cspp_dev.h5",
    "SVI01_npp_d20170128_t1240105_e1241347_b27228_c20170128124933022697_cspp_dev.h5",
    "SVI01_npp_d20170128_t1241359_e1243001_b27228_c20170128125105683986_cspp_dev.h5",
    "SVI01_npp_d20170128_t1243013_e1244238_b27228_c20170128125240927888_cspp_dev.h5",
]
SVI02_FILES = [
    "SVI02_npp_d20170128_t1230144_e1231386_b27228_c20170128123807711244_cspp_dev.h5",
    "SVI02_npp_d20170128_t1231398_e1233040_b27228_c20170128123932632807_cspp_dev.h5",
    "SVI02_npp_d20170128_t1233052_e1234294_b27228_c20170128124100316117_cspp_dev.h5",
    "SVI02_npp_d20170128_t1234306_e1235548_b27228_c20170128124309108964_cspp_dev.h5",
    "SVI02_npp_d20170128_t1235560_e1237184_b27228_c20170128124430789039_cspp_dev.h5",
    "SVI02_npp_d20170128_t1237197_e1238439_b27228_c20170128124606564398_cspp_dev.h5",
    "SVI02_npp_d20170128_t1238451_e1240093_b27228_c20170128124806162998_cspp_dev.h5",
    "SVI02_npp_d20170128_t1240105_e1241347_b27228_c20170128124933090354_cspp_dev.h5",
    "SVI02_npp_d20170128_t1241359_e1243001_b27228_c20170128125105758438_cspp_dev.h5",
    "SVI02_npp_d20170128_t1243013_e1244238_b27228_c20170128125240934475_cspp_dev.h5",
]
SVI03_FILES = [
    "SVI03_npp_d20170128_t1230144_e1231386_b27228_c20170128123807790854_cspp_dev.h5",
    "SVI03_npp_d20170128_t1231398_e1233040_b27228_c20170128123932703535_cspp_dev.h5",
    "SVI03_npp_d20170128_t1233052_e1234294_b27228_c20170128124100406626_cspp_dev.h5",
    "SVI03_npp_d20170128_t1234306_e1235548_b27228_c20170128124309179885_cspp_dev.h5",
    "SVI03_npp_d20170128_t1235560_e1237184_b27228_c20170128124430858868_cspp_dev.h5",
    "SVI03_npp_d20170128_t1237197_e1238439_b27228_c20170128124606750872_cspp_dev.h5",
    "SVI03_npp_d20170128_t1238451_e1240093_b27228_c20170128124806231759_cspp_dev.h5",
    "SVI03_npp_d20170128_t1240105_e1241347_b27228_c20170128124933157871_cspp_dev.h5",
    "SVI03_npp_d20170128_t1241359_e1243001_b27228_c20170128125105832479_cspp_dev.h5",
    "SVI03_npp_d20170128_t1243013_e1244238_b27228_c20170128125240940464_cspp_dev.h5",
]
SVI04_FILES = [
    "SVI04_npp_d20170128_t1230144_e1231386_b27228_c20170128123807879916_cspp_dev.h5",
    "SVI04_npp_d20170128_t1231398_e1233040_b27228_c20170128123932774251_cspp_dev.h5",
    "SVI04_npp_d20170128_t1233052_e1234294_b27228_c20170128124100502220_cspp_dev.h5",
    "SVI04_npp_d20170128_t1234306_e1235548_b27228_c20170128124309251788_cspp_dev.h5",
    "SVI04_npp_d20170128_t1235560_e1237184_b27228_c20170128124430928643_cspp_dev.h5",
    "SVI04_npp_d20170128_t1237197_e1238439_b27228_c20170128124606941637_cspp_dev.h5",
    "SVI04_npp_d20170128_t1238451_e1240093_b27228_c20170128124806300867_cspp_dev.h5",
    "SVI04_npp_d20170128_t1240105_e1241347_b27228_c20170128124933224276_cspp_dev.h5",
    "SVI04_npp_d20170128_t1241359_e1243001_b27228_c20170128125105908005_cspp_dev.h5",
    "SVI04_npp_d20170128_t1243013_e1244238_b27228_c20170128125240946462_cspp_dev.h5",
]
SVI05_FILES = [
    "SVI05_npp_d20170128_t1230144_e1231386_b27228_c20170128123807965352_cspp_dev.h5",
    "SVI05_npp_d20170128_t1231398_e1233040_b27228_c20170128123932843985_cspp_dev.h5",
    "SVI05_npp_d20170128_t1233052_e1234294_b27228_c20170128124100619023_cspp_dev.h5",
    "SVI05_npp_d20170128_t1234306_e1235548_b27228_c20170128124309321883_cspp_dev.h5",
    "SVI05_npp_d20170128_t1235560_e1237184_b27228_c20170128124430998015_cspp_dev.h5",
    "SVI05_npp_d20170128_t1237197_e1238439_b27228_c20170128124607124779_cspp_dev.h5",
    "SVI05_npp_d20170128_t1238451_e1240093_b27228_c20170128124806370721_cspp_dev.h5",
    "SVI05_npp_d20170128_t1240105_e1241347_b27228_c20170128124933292345_cspp_dev.h5",
    "SVI05_npp_d20170128_t1241359_e1243001_b27228_c20170128125105983240_cspp_dev.h5",
    "SVI05_npp_d20170128_t1243013_e1244238_b27228_c20170128125241011931_cspp_dev.h5",
]
SVM01_FILES = [
    "SVM01_npp_d20170128_t1230144_e1231386_b27228_c20170128123808056273_cspp_dev.h5",
    "SVM01_npp_d20170128_t1231398_e1233040_b27228_c20170128123932914817_cspp_dev.h5",
    "SVM01_npp_d20170128_t1233052_e1234294_b27228_c20170128124100687072_cspp_dev.h5",
    "SVM01_npp_d20170128_t1234306_e1235548_b27228_c20170128124309391583_cspp_dev.h5",
    "SVM01_npp_d20170128_t1235560_e1237184_b27228_c20170128124431068152_cspp_dev.h5",
    "SVM01_npp_d20170128_t1237197_e1238439_b27228_c20170128124607341439_cspp_dev.h5",
    "SVM01_npp_d20170128_t1238451_e1240093_b27228_c20170128124806439930_cspp_dev.h5",
    "SVM01_npp_d20170128_t1240105_e1241347_b27228_c20170128124933359550_cspp_dev.h5",
    "SVM01_npp_d20170128_t1241359_e1243001_b27228_c20170128125106057121_cspp_dev.h5",
    "SVM01_npp_d20170128_t1243013_e1244238_b27228_c20170128125241079274_cspp_dev.h5",
]
SVM02_FILES = [
    "SVM02_npp_d20170128_t1230144_e1231386_b27228_c20170128123808083056_cspp_dev.h5",
    "SVM02_npp_d20170128_t1231398_e1233040_b27228_c20170128123932936791_cspp_dev.h5",
    "SVM02_npp_d20170128_t1233052_e1234294_b27228_c20170128124100708303_cspp_dev.h5",
    "SVM02_npp_d20170128_t1234306_e1235548_b27228_c20170128124309411322_cspp_dev.h5",
    "SVM02_npp_d20170128_t1235560_e1237184_b27228_c20170128124431089436_cspp_dev.h5",
    "SVM02_npp_d20170128_t1237197_e1238439_b27228_c20170128124607386792_cspp_dev.h5",
    "SVM02_npp_d20170128_t1238451_e1240093_b27228_c20170128124806460870_cspp_dev.h5",
    "SVM02_npp_d20170128_t1240105_e1241347_b27228_c20170128124933381053_cspp_dev.h5",
    "SVM02_npp_d20170128_t1241359_e1243001_b27228_c20170128125106080807_cspp_dev.h5",
    "SVM02_npp_d20170128_t1243013_e1244238_b27228_c20170128125241085636_cspp_dev.h5",
]
SVM03_FILES = [
    "SVM03_npp_d20170128_t1230144_e1231386_b27228_c20170128123808110482_cspp_dev.h5",
    "SVM03_npp_d20170128_t1231398_e1233040_b27228_c20170128123932959109_cspp_dev.h5",
    "SVM03_npp_d20170128_t1233052_e1234294_b27228_c20170128124100729893_cspp_dev.h5",
    "SVM03_npp_d20170128_t1234306_e1235548_b27228_c20170128124309431166_cspp_dev.h5",
    "SVM03_npp_d20170128_t1235560_e1237184_b27228_c20170128124431111317_cspp_dev.h5",
    "SVM03_npp_d20170128_t1237197_e1238439_b27228_c20170128124607452947_cspp_dev.h5",
    "SVM03_npp_d20170128_t1238451_e1240093_b27228_c20170128124806482313_cspp_dev.h5",
    "SVM03_npp_d20170128_t1240105_e1241347_b27228_c20170128124933402956_cspp_dev.h5",
    "SVM03_npp_d20170128_t1241359_e1243001_b27228_c20170128125106104416_cspp_dev.h5",
    "SVM03_npp_d20170128_t1243013_e1244238_b27228_c20170128125241091894_cspp_dev.h5",
]
SVM04_FILES = [
    "SVM04_npp_d20170128_t1230144_e1231386_b27228_c20170128123808144258_cspp_dev.h5",
    "SVM04_npp_d20170128_t1231398_e1233040_b27228_c20170128123932987116_cspp_dev.h5",
    "SVM04_npp_d20170128_t1233052_e1234294_b27228_c20170128124100757998_cspp_dev.h5",
    "SVM04_npp_d20170128_t1234306_e1235548_b27228_c20170128124309456779_cspp_dev.h5",
    "SVM04_npp_d20170128_t1235560_e1237184_b27228_c20170128124431139074_cspp_dev.h5",
    "SVM04_npp_d20170128_t1237197_e1238439_b27228_c20170128124607542297_cspp_dev.h5",
    "SVM04_npp_d20170128_t1238451_e1240093_b27228_c20170128124806582119_cspp_dev.h5",
    "SVM04_npp_d20170128_t1240105_e1241347_b27228_c20170128124933430115_cspp_dev.h5",
    "SVM04_npp_d20170128_t1241359_e1243001_b27228_c20170128125106135317_cspp_dev.h5",
    "SVM04_npp_d20170128_t1243013_e1244238_b27228_c20170128125241097854_cspp_dev.h5",
]
SVM05_FILES = [
    "SVM05_npp_d20170128_t1230144_e1231386_b27228_c20170128123808174909_cspp_dev.h5",
    "SVM05_npp_d20170128_t1231398_e1233040_b27228_c20170128123933013965_cspp_dev.h5",
    "SVM05_npp_d20170128_t1233052_e1234294_b27228_c20170128124100786454_cspp_dev.h5",
    "SVM05_npp_d20170128_t1234306_e1235548_b27228_c20170128124309482588_cspp_dev.h5",
    "SVM05_npp_d20170128_t1235560_e1237184_b27228_c20170128124431167292_cspp_dev.h5",
    "SVM05_npp_d20170128_t1237197_e1238439_b27228_c20170128124607571141_cspp_dev.h5",
    "SVM05_npp_d20170128_t1238451_e1240093_b27228_c20170128124806609136_cspp_dev.h5",
    "SVM05_npp_d20170128_t1240105_e1241347_b27228_c20170128124933456985_cspp_dev.h5",
    "SVM05_npp_d20170128_t1241359_e1243001_b27228_c20170128125106166701_cspp_dev.h5",
    "SVM05_npp_d20170128_t1243013_e1244238_b27228_c20170128125241103776_cspp_dev.h5",
]
SVM06_FILES = [
    "SVM06_npp_d20170128_t1230144_e1231386_b27228_c20170128123808209437_cspp_dev.h5",
    "SVM06_npp_d20170128_t1231398_e1233040_b27228_c20170128123933040415_cspp_dev.h5",
    "SVM06_npp_d20170128_t1233052_e1234294_b27228_c20170128124100814386_cspp_dev.h5",
    "SVM06_npp_d20170128_t1234306_e1235548_b27228_c20170128124309508530_cspp_dev.h5",
    "SVM06_npp_d20170128_t1235560_e1237184_b27228_c20170128124431195933_cspp_dev.h5",
    "SVM06_npp_d20170128_t1237197_e1238439_b27228_c20170128124607627637_cspp_dev.h5",
    "SVM06_npp_d20170128_t1238451_e1240093_b27228_c20170128124806636359_cspp_dev.h5",
    "SVM06_npp_d20170128_t1240105_e1241347_b27228_c20170128124933483996_cspp_dev.h5",
    "SVM06_npp_d20170128_t1241359_e1243001_b27228_c20170128125106198061_cspp_dev.h5",
    "SVM06_npp_d20170128_t1243013_e1244238_b27228_c20170128125241109756_cspp_dev.h5",
]
SVM07_FILES = [
    "SVM07_npp_d20170128_t1230144_e1231386_b27228_c20170128123808817507_cspp_dev.h5",
    "SVM07_npp_d20170128_t1231398_e1233040_b27228_c20170128123933681441_cspp_dev.h5",
    "SVM07_npp_d20170128_t1233052_e1234294_b27228_c20170128124101490225_cspp_dev.h5",
    "SVM07_npp_d20170128_t1234306_e1235548_b27228_c20170128124310169252_cspp_dev.h5",
    "SVM07_npp_d20170128_t1235560_e1237184_b27228_c20170128124431921741_cspp_dev.h5",
    "SVM07_npp_d20170128_t1237197_e1238439_b27228_c20170128124608449604_cspp_dev.h5",
    "SVM07_npp_d20170128_t1238451_e1240093_b27228_c20170128124807323479_cspp_dev.h5",
    "SVM07_npp_d20170128_t1240105_e1241347_b27228_c20170128124934114857_cspp_dev.h5",
    "SVM07_npp_d20170128_t1241359_e1243001_b27228_c20170128125106915897_cspp_dev.h5",
    "SVM07_npp_d20170128_t1243013_e1244238_b27228_c20170128125241115831_cspp_dev.h5",
]
SVM08_FILES = [
    "SVM08_npp_d20170128_t1230144_e1231386_b27228_c20170128123808263071_cspp_dev.h5",
    "SVM08_npp_d20170128_t1231398_e1233040_b27228_c20170128123933088148_cspp_dev.h5",
    "SVM08_npp_d20170128_t1233052_e1234294_b27228_c20170128124100871070_cspp_dev.h5",
    "SVM08_npp_d20170128_t1234306_e1235548_b27228_c20170128124309555838_cspp_dev.h5",
    "SVM08_npp_d20170128_t1235560_e1237184_b27228_c20170128124431248317_cspp_dev.h5",
    "SVM08_npp_d20170128_t1237197_e1238439_b27228_c20170128124607703167_cspp_dev.h5",
    "SVM08_npp_d20170128_t1238451_e1240093_b27228_c20170128124806684245_cspp_dev.h5",
    "SVM08_npp_d20170128_t1240105_e1241347_b27228_c20170128124933531899_cspp_dev.h5",
    "SVM08_npp_d20170128_t1241359_e1243001_b27228_c20170128125106322404_cspp_dev.h5",
    "SVM08_npp_d20170128_t1243013_e1244238_b27228_c20170128125241141517_cspp_dev.h5",
]
SVM09_FILES = [
    "SVM09_npp_d20170128_t1230144_e1231386_b27228_c20170128123808287273_cspp_dev.h5",
    "SVM09_npp_d20170128_t1231398_e1233040_b27228_c20170128123933108818_cspp_dev.h5",
    "SVM09_npp_d20170128_t1233052_e1234294_b27228_c20170128124100892937_cspp_dev.h5",
    "SVM09_npp_d20170128_t1234306_e1235548_b27228_c20170128124309576967_cspp_dev.h5",
    "SVM09_npp_d20170128_t1235560_e1237184_b27228_c20170128124431271226_cspp_dev.h5",
    "SVM09_npp_d20170128_t1237197_e1238439_b27228_c20170128124607724822_cspp_dev.h5",
    "SVM09_npp_d20170128_t1238451_e1240093_b27228_c20170128124806704840_cspp_dev.h5",
    "SVM09_npp_d20170128_t1240105_e1241347_b27228_c20170128124933552828_cspp_dev.h5",
    "SVM09_npp_d20170128_t1241359_e1243001_b27228_c20170128125106345774_cspp_dev.h5",
    "SVM09_npp_d20170128_t1243013_e1244238_b27228_c20170128125241161505_cspp_dev.h5",
]
SVM10_FILES = [
    "SVM10_npp_d20170128_t1230144_e1231386_b27228_c20170128123808310591_cspp_dev.h5",
    "SVM10_npp_d20170128_t1231398_e1233040_b27228_c20170128123933130017_cspp_dev.h5",
    "SVM10_npp_d20170128_t1233052_e1234294_b27228_c20170128124100914429_cspp_dev.h5",
    "SVM10_npp_d20170128_t1234306_e1235548_b27228_c20170128124309597409_cspp_dev.h5",
    "SVM10_npp_d20170128_t1235560_e1237184_b27228_c20170128124431293295_cspp_dev.h5",
    "SVM10_npp_d20170128_t1237197_e1238439_b27228_c20170128124607775262_cspp_dev.h5",
    "SVM10_npp_d20170128_t1238451_e1240093_b27228_c20170128124806725948_cspp_dev.h5",
    "SVM10_npp_d20170128_t1240105_e1241347_b27228_c20170128124933573645_cspp_dev.h5",
    "SVM10_npp_d20170128_t1241359_e1243001_b27228_c20170128125106368109_cspp_dev.h5",
    "SVM10_npp_d20170128_t1243013_e1244238_b27228_c20170128125241167901_cspp_dev.h5",
]
SVM11_FILES = [
    "SVM11_npp_d20170128_t1230144_e1231386_b27228_c20170128123808334604_cspp_dev.h5",
    "SVM11_npp_d20170128_t1231398_e1233040_b27228_c20170128123933151513_cspp_dev.h5",
    "SVM11_npp_d20170128_t1233052_e1234294_b27228_c20170128124100935872_cspp_dev.h5",
    "SVM11_npp_d20170128_t1234306_e1235548_b27228_c20170128124309618913_cspp_dev.h5",
    "SVM11_npp_d20170128_t1235560_e1237184_b27228_c20170128124431315343_cspp_dev.h5",
    "SVM11_npp_d20170128_t1237197_e1238439_b27228_c20170128124607795773_cspp_dev.h5",
    "SVM11_npp_d20170128_t1238451_e1240093_b27228_c20170128124806746702_cspp_dev.h5",
    "SVM11_npp_d20170128_t1240105_e1241347_b27228_c20170128124933594619_cspp_dev.h5",
    "SVM11_npp_d20170128_t1241359_e1243001_b27228_c20170128125106390787_cspp_dev.h5",
    "SVM11_npp_d20170128_t1243013_e1244238_b27228_c20170128125241187089_cspp_dev.h5",
]
SVM12_FILES = [
    "SVM12_npp_d20170128_t1230144_e1231386_b27228_c20170128123808354907_cspp_dev.h5",
    "SVM12_npp_d20170128_t1231398_e1233040_b27228_c20170128123933172698_cspp_dev.h5",
    "SVM12_npp_d20170128_t1233052_e1234294_b27228_c20170128124100958185_cspp_dev.h5",
    "SVM12_npp_d20170128_t1234306_e1235548_b27228_c20170128124309641720_cspp_dev.h5",
    "SVM12_npp_d20170128_t1235560_e1237184_b27228_c20170128124431337449_cspp_dev.h5",
    "SVM12_npp_d20170128_t1237197_e1238439_b27228_c20170128124607849336_cspp_dev.h5",
    "SVM12_npp_d20170128_t1238451_e1240093_b27228_c20170128124806767820_cspp_dev.h5",
    "SVM12_npp_d20170128_t1240105_e1241347_b27228_c20170128124933615858_cspp_dev.h5",
    "SVM12_npp_d20170128_t1241359_e1243001_b27228_c20170128125106413369_cspp_dev.h5",
    "SVM12_npp_d20170128_t1243013_e1244238_b27228_c20170128125241193417_cspp_dev.h5",
]
SVM13_FILES = [
    "SVM13_npp_d20170128_t1230144_e1231386_b27228_c20170128123808374740_cspp_dev.h5",
    "SVM13_npp_d20170128_t1231398_e1233040_b27228_c20170128123933194069_cspp_dev.h5",
    "SVM13_npp_d20170128_t1233052_e1234294_b27228_c20170128124100980119_cspp_dev.h5",
    "SVM13_npp_d20170128_t1234306_e1235548_b27228_c20170128124309664100_cspp_dev.h5",
    "SVM13_npp_d20170128_t1235560_e1237184_b27228_c20170128124431359731_cspp_dev.h5",
    "SVM13_npp_d20170128_t1237197_e1238439_b27228_c20170128124607874078_cspp_dev.h5",
    "SVM13_npp_d20170128_t1238451_e1240093_b27228_c20170128124806788761_cspp_dev.h5",
    "SVM13_npp_d20170128_t1240105_e1241347_b27228_c20170128124933637079_cspp_dev.h5",
    "SVM13_npp_d20170128_t1241359_e1243001_b27228_c20170128125106435940_cspp_dev.h5",
    "SVM13_npp_d20170128_t1243013_e1244238_b27228_c20170128125241212475_cspp_dev.h5",
]
SVM14_FILES = [
    "SVM14_npp_d20170128_t1230144_e1231386_b27228_c20170128123808406951_cspp_dev.h5",
    "SVM14_npp_d20170128_t1231398_e1233040_b27228_c20170128123933225740_cspp_dev.h5",
    "SVM14_npp_d20170128_t1233052_e1234294_b27228_c20170128124101014245_cspp_dev.h5",
    "SVM14_npp_d20170128_t1234306_e1235548_b27228_c20170128124309701221_cspp_dev.h5",
    "SVM14_npp_d20170128_t1235560_e1237184_b27228_c20170128124431396452_cspp_dev.h5",
    "SVM14_npp_d20170128_t1237197_e1238439_b27228_c20170128124607945197_cspp_dev.h5",
    "SVM14_npp_d20170128_t1238451_e1240093_b27228_c20170128124806821782_cspp_dev.h5",
    "SVM14_npp_d20170128_t1240105_e1241347_b27228_c20170128124933671536_cspp_dev.h5",
    "SVM14_npp_d20170128_t1241359_e1243001_b27228_c20170128125106472259_cspp_dev.h5",
    "SVM14_npp_d20170128_t1243013_e1244238_b27228_c20170128125241244180_cspp_dev.h5",
]
SVM15_FILES = [
    "SVM15_npp_d20170128_t1230144_e1231386_b27228_c20170128123808427359_cspp_dev.h5",
    "SVM15_npp_d20170128_t1231398_e1233040_b27228_c20170128123933246722_cspp_dev.h5",
    "SVM15_npp_d20170128_t1233052_e1234294_b27228_c20170128124101036439_cspp_dev.h5",
    "SVM15_npp_d20170128_t1234306_e1235548_b27228_c20170128124309725283_cspp_dev.h5",
    "SVM15_npp_d20170128_t1235560_e1237184_b27228_c20170128124431418392_cspp_dev.h5",
    "SVM15_npp_d20170128_t1237197_e1238439_b27228_c20170128124607965779_cspp_dev.h5",
    "SVM15_npp_d20170128_t1238451_e1240093_b27228_c20170128124806948533_cspp_dev.h5",
    "SVM15_npp_d20170128_t1240105_e1241347_b27228_c20170128124933693703_cspp_dev.h5",
    "SVM15_npp_d20170128_t1241359_e1243001_b27228_c20170128125106494806_cspp_dev.h5",
    "SVM15_npp_d20170128_t1243013_e1244238_b27228_c20170128125241264993_cspp_dev.h5",
]
SVM16_FILES = [
    "SVM16_npp_d20170128_t1230144_e1231386_b27228_c20170128123808447333_cspp_dev.h5",
    "SVM16_npp_d20170128_t1231398_e1233040_b27228_c20170128123933268965_cspp_dev.h5",
    "SVM16_npp_d20170128_t1233052_e1234294_b27228_c20170128124101058805_cspp_dev.h5",
    "SVM16_npp_d20170128_t1234306_e1235548_b27228_c20170128124309747830_cspp_dev.h5",
    "SVM16_npp_d20170128_t1235560_e1237184_b27228_c20170128124431440604_cspp_dev.h5",
    "SVM16_npp_d20170128_t1237197_e1238439_b27228_c20170128124608015196_cspp_dev.h5",
    "SVM16_npp_d20170128_t1238451_e1240093_b27228_c20170128124806970479_cspp_dev.h5",
    "SVM16_npp_d20170128_t1240105_e1241347_b27228_c20170128124933715705_cspp_dev.h5",
    "SVM16_npp_d20170128_t1241359_e1243001_b27228_c20170128125106518023_cspp_dev.h5",
    "SVM16_npp_d20170128_t1243013_e1244238_b27228_c20170128125241285533_cspp_dev.h5",
]

FILES_20170128_1229 = {
    "DNB": SVDNB_FILES,
    "I01": SVI01_FILES,
    "I02": SVI02_FILES,
    "I03": SVI03_FILES,
    "I04": SVI04_FILES,
    "I05": SVI05_FILES,
    "M01": SVM01_FILES,
    "M02": SVM02_FILES,
    "M03": SVM03_FILES,
    "M04": SVM04_FILES,
    "M05": SVM05_FILES,
    "M06": SVM06_FILES,
    "M07": SVM07_FILES,
    "M08": SVM08_FILES,
    "M09": SVM09_FILES,
    "M10": SVM10_FILES,
    "M11": SVM11_FILES,
    "M12": SVM12_FILES,
    "M13": SVM13_FILES,
    "M14": SVM14_FILES,
    "M15": SVM15_FILES,
    "M16": SVM16_FILES,
}


def get_viirs_sdr_20170128_1229(
        base_dir=None,
        channels=("I01", "I02", "I03", "I04", "I05",
                  "M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10",
                  "M11", "M12", "M13", "M14", "M15", "M16",
                  "DNB"),
        granules=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)):
    r"""Get VIIRS SDR files for 2017-01-28 12:29 to 12:43.

    These files are downloaded from Zenodo. You can see the full file
    listing here: https://zenodo.org/record/263296

    Specific channels can be specified with the ``channels`` keyword argument.
    By default, all channels (all I bands, M bands, and DNB bands) will be
    downloaded. Channels are referred to by their band type and channel number
    (ex. "I01" or "M16" or "DNB"). Terrain-corrected geolocation files are
    always downloaded when the corresponding band data is specified.

    The ``granules`` argument will control whichranules ("time steps")
    are downloaded. There are 10 available and the keyword argument can be
    specified as a tuple of integers from 1 to 10.

    This full dataset is ~10.1GB.

    Notes:
        File list was retrieved using the zenodo API.

        .. code-block:: python

            import requests
            viirs_listing = requests.get("https://zenodo.org/api/records/263296")
            viirs_dict = json.loads(viirs_listing.content)
            print("\n".join(sorted(x['links']['self'] for x in viirs_dict['files'])))

    """
    base_dir = base_dir or config.get("demo_data_dir", ".")

    # assume directory in zip is the same as zip filename without the extension
    subdir = os.path.join(base_dir, "viirs_sdr", "20170128_1229")
    os.makedirs(subdir, exist_ok=True)
    urls = (ZENODO_BASE_URL + fn for fn in _get_filenames_to_download(channels, granules))

    files = []
    for url in urls:
        target = os.path.join(subdir, os.path.basename(url))
        files.append(target)
        if os.path.isfile(target):
            logger.info(f"File {target} already exists, skipping...")
            continue
        logger.info(f"Downloading file to {target}...")
        _download_url(url, target)

    return files


def _get_filenames_to_download(channels, granules):
    if any("DNB" in chan for chan in channels):
        yield from _yield_specific_granules(GDNBO_URLS, granules)
    if any("I" in chan for chan in channels):
        yield from _yield_specific_granules(GITCO_URLS, granules)
    if any("M" in chan for chan in channels):
        yield from _yield_specific_granules(GMTCO_URLS, granules)
    for channel in channels:
        yield from _yield_specific_granules(FILES_20170128_1229[channel], granules)


def _yield_specific_granules(filenames, granules):
    for gran_num in granules:
        yield filenames[gran_num - 1]


def _download_url(source, target):
    with requests.get(source, stream=True) as r:
        r.raise_for_status()
        with open(target, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
