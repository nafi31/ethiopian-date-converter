#!/usr/bin/env python3
# encoding=utf-8
# maintainer: rgaudin

""" Ethiopian Date Converter

Convert from Ethiopian date to Gregorian date (and vice-versa)

Examples:

greg_date = EthiopianDateConverter.to_gregorian(2003, 4, 11)
ethi_date = EthiopianDateConverter.date_to_ethiopian(datetime.date.today())

"""

from .ethiopian_date import EthiopianDateConverter
