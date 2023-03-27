#
# Copyright (C) 2009 The Android Open Source Project
# Copyright (c) 2011, The Linux Foundation. All rights reserved.
# Copyright (C) 2017 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

import hashlib
import common
import re

def FullOTA_Assertions(info):
  AddVendorAssertion(info)
  AddModemAssertion(info)
  return

def IncrementalOTA_Assertions(info):
  AddVendorAssertion(info)
  AddModemAssertion(info)
  return

def AddVendorAssertion(info):
  cmd = 'assert(cheeseburger.file_exists("/dev/block/bootdevice/by-name/vendor") == "1" || \
    abort("Error: Vendor partition doesn\'t exist!"););'
  info.script.AppendExtra(cmd)
  return

def AddModemAssertion(info):
  android_info = info.input_zip.read("OTA/android-info.txt").decode('utf-8')
  m = re.search(r'require\s+version-modem\s*=\s*(.+)', android_info)
  f = re.search(r'require\s+version-firmware\s*=\s*(.+)', android_info)
  if m and f:
    version_modem = m.group(1).rstrip()
    version_firmware = f.group(1).rstrip()
    if ((len(version_modem) and '*' not in version_modem) and \
        (len(version_firmware) and '*' not in version_firmware)):
      cmd = 'assert(cheeseburger.verify_modem("' + version_modem + '") == "1" || \
        abort("Error: This package requires firmware version ' + version_firmware + \
        ' or newer. Please upgrade firmware and retry!"););'
      info.script.AppendExtra(cmd)
  return
