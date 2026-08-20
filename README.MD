DSpace Packager
===============

DSpace Packager is a web service (python Flask) that allows users to create packages in the Simple Archive Format for batch ingest into the University of Oregon's institutional repository.

### Requirements
A directory (DIR) that is writable by the user and mounted on the server where this service runs; subdirectories as described under initial project setup.

### Initial project setup
As an example, the CHC project should be set up accordingly:
  1. create DIR/chc/
  2. create chc/files/, chc/configs/, chc/work/, chc/zips/
  3. DIR/chc should be mounted in the service via the compose file
  4. metadata, config, and project methods

### Packaging
1. continuing with chc as an example: the user places the content files and metadata file in chc/files, and a config in chc/configs
2. the user launches the service by filling out the form at /setup
   required info includes name of the config, name of the metadata file, path to the content files (eg "files"), and the project name, eg "chc"
3. when the form is submitted, the packages will be created and written to DIR/chc/work, and xml can be examined as needed; zipped packages are also generated in DIR/chc/zips. If any errors were encountered, they will be written to a log file in the project directory, i.e. DIR/chc/log

### Expansion
This service can be expanded to handle additional workflows by a developer; this includes defining the metadata requirements, composing a config, adding new fields to the DublinCoreXML class if necessary, adding new/override methods as needed in a project_methods.py, and then setting up the directories as described in Initial project setup and adding the project to the web form.


### Description of the config
- The keys refer to the fields defined in the DublinCoreXML class (see app/packager/helpers.py). Additional keys must be added to the class.
- Fields which can simply be hardcoded can be indicated as a "val":
"publisher":{"val": "University of Oregon"}
- Fields which must be read from the metadata can be indicated with their row index:
"title":{"ind":0}
- Fields in which the data must be processed should indicate a method name:
"author":{"ind":[1,2], "method":"construct_name"}

### Deploying
This service is deployed using podman; ensure that the env contains the values required by the compose file, and that the mounts are properly set up. Note that the service should only be reachable on campus or by VPN.

