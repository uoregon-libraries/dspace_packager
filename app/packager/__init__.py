import sys
import os
import shutil
from packager.base_record import BaseRecord
from packager.etd_record import EtdRecord
from packager.helpers import zip_work
import pdb
import logging
import datetime
import subprocess
from flask import current_app as app
from zipfile import ZipFile
import glob

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

def create_etd_record(filename: str) -> 'EtdRecord':
  global configpath
  record = EtdRecord()
  record.init("etd")
  record.import_config(configpath)
  record.set_metadata(filename)
  return record

def create_dir(dirname: str) -> str:
    """Creates a directory for the record in the work path."""
    """If directory already exists, return"""
    """If directory + dublin_core file already exists, raise error"""
    global workpath
    recorddir = os.path.join(workpath, dirname)
    if os.path.isfile(os.path.join(recorddir, "dublin_core.xml")):
        raise FileExistsError(f"Possible duplicate: {dirname}")
    os.makedirs(recorddir, exist_ok=True)
    return recorddir + os.path.sep

def write_xml(record, recordpath: str):
    """Writes the Dublin Core XML file."""
    content = record.assemble_properties()
    xml_filepath = os.path.join(recordpath, "dublin_core.xml")
    with open(xml_filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    if not hasattr(record, 'assemble_degree_properties'):
      return
    content = record.assemble_degree_properties()
    xml_filepath = os.path.join(recordpath, "metadata.xml")
    with open(xml_filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def write_colls(record, recordpath: str):
  content = record.assemble_colls()
  xml_filepath = os.path.join(recordpath, "collections")
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

def copy_content_file(record, sourcedir, destdir: str):
    """Copies the content file associated with the record."""
    filename = record.filename
    source_path = os.path.join(sourcedir, filename)
    dest_path = os.path.join(destdir, filename)
    shutil.copy(source_path, dest_path)

def process_everything(projname: str, datafile: str, configfile: str, filedir: str) -> int:
    """Processes all lines in the data file."""
    global projpath, workpath, filepath, configpath
    basedir = "/app/instance"
    projpath = os.path.join(basedir, projname)
    workpath = os.path.join(projpath, "work") #packages written here
    filepath = os.path.join(projpath, filedir)
    configpath = os.path.join(projpath, "configs", configfile)

    os.makedirs(workpath, exist_ok=True)
    setupLog()
    log.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log.info("processing ...")
    data_file_path = os.path.join(projpath, filedir, datafile)
    errorcount = 0
    try:
      if projname == "etd":
        #all the zips are in files, unzip them
        zips = glob.glob(os.path.join(filepath, "*.zip"))
        for zip in zips:
          log.info(zip)
          with ZipFile(zip, 'r') as zip_ref:
            zip_ref.extractall(filepath)
        items = glob.glob(os.path.join(filepath, "*DATA.xml"))
      else:
        items = file.readlines(data_file_path)

      try:
        for item in items:
          if projname == "etd":
            log.info("working on " + item)
            record = create_etd_record(item)
            sourcedir = filepath
          else:
            record = create_record(item.strip())
            sourcedir = filedir

          try:
            record_dir_path = create_dir(record.dirname)
            write_xml(record, record_dir_path)
            write_colls(record, record_dir_path)
            copy_content_file(record, sourcedir, record_dir_path)
            copy_license(record_dir_path)
            write_contents(record, record_dir_path)
          except Exception as e: # Base Record exceptions are caught here
               log.error(f"Error processing record: {e}\nRecord data: {record.data}...", exc_info=True)
               errorcount += 1
        log.info("all done writing dublin")
        zip_work(projname)
      except Exception as e:
          log.info(f"Error processing: {e}", exc_info=True)
    finally: return errorcount

def parseFileDir(path) -> str:
  parts = path.split('/')
  return parts[len(parts)-2]

def setupLog():
  logpath = os.path.join(projpath, "log")
  log.addHandler(logging.FileHandler(logpath))
  log.setLevel(logging.INFO)
  
