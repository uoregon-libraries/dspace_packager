import sys
import os
import shutil
from packager.base_record import BaseRecord
from packager.helpers import zip_proj_dirs
import pdb
import logging
import datetime
import subprocess
from flask import current_app as app

# global vars
projpath = ""
workpath = ""
filepath = ""
configpath = ""
log = logging.getLogger(__name__)

def create_record(line: str, projname: str) -> 'BaseRecord':
  global configpath
  record = BaseRecord()
  record.init(projname)
  record.import_config(configpath)
  record.set_metadata(line)
  return record

def create_dir(dirname: str) -> str:
    """Creates a directory for the record in the work path."""
    global workpath
    recorddir = os.path.join(workpath, dirname)
    if os.path.isdir(recorddir):
        raise FileExistsError(f"Possible duplicate: {dirname}")
    os.makedirs(recorddir)
    return recorddir + os.path.sep

def write_xml(record, recordpath: str):
    """Writes the Dublin Core XML file."""
    content = record.assemble_properties()
    xml_filepath = os.path.join(recordpath, "dublin_core.xml")
    with open(xml_filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def write_contents(record, recordpath: str):
    """Writes the contents file"""
    fpath = os.path.join(recordpath, "contents")
    with open(fpath, 'w', encoding='utf-8') as f:
      f.write(f"{record.filename}\tbundle:ORIGINAL\n")
      f.write("license.txt\tbundle:LICENSE\n")

def copy_license(recordpath: str):
    curdir = os.getcwd()
    license_path = os.path.join(curdir, "packager", "license.txt")
    dest_path = os.path.join(recordpath, "license.txt")
    shutil.copy(license_path, dest_path)

def copy_content_file(record, recordpath: str):
    """Copies the content file associated with the record."""
    global filepath
    filename = record.filename
    source_path = os.path.join(filepath, filename)
    dest_path = os.path.join(recordpath, filename)
    shutil.copy(source_path, dest_path)

def process_everything(projname: str, datafile: str, configfile: str, filedir: str) -> int:
    """Processes all lines in the data file."""
    global projpath, workpath, filepath, configpath
    basedir = app.instance_path
    projpath = os.path.join(basedir, projname)
    workpath = os.path.join(projpath, "work") #packages written here
    filepath = os.path.join(projpath, filedir)
    configpath = os.path.join(projpath, "configs", configfile)

    os.makedirs(workpath, exist_ok=True)
    setupLog()
    log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log.info("processing ...")
    data_file_path = os.path.join(projpath, filedir, datafile)
    if not os.path.exists(data_file_path):
      log.error("data file can not be found")
      return 1
    errorcount = 0
    try:
        with open(data_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = create_record(line, projname)
                    record_dir_path = create_dir(record.dirname)
                    write_xml(record, record_dir_path)
                    copy_content_file(record, record_dir_path)
                    copy_license(record_dir_path)
                    write_contents(record, record_dir_path)
                except Exception as e: # Base Record exceptions are caught here
                    log.error(f"Error processing record: {e}\nRecord data: {line[:100]}...", exc_info=True)
                    errorcount += 1
        log.info("all done writing dublin")
        zip_proj_dirs(projname)

    finally: return errorcount

def setupLog():
  logpath = os.path.join(projpath, "log")
  log.addHandler(logging.FileHandler(logpath))
  log.setLevel(logging.INFO)
  
