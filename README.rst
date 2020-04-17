====================
stt_sample_inspector
====================

Inspect, modify, and add metadata to DeepSpeech (speech-to-text) datasets in CSV format.

Description
===========

This tool lets you quickly inspect, edit, and add metadata to a DeepSpeech dataset.

Typical flow:

- A server has training sets in it, stored in the DeepSpeech CSV input format.
- Some stakeholders would like to quickly inspect the data without having to download all of it
- Would like to be able to extend the set with extra metadata, for example, one might want to look at a subset of samples and tag them as noisy vs. clean [functionality not added yet]
- Would like to be able to save/export the modified version of the original input CSV.

This tool can be installed and run in the server where the data resides. It'll expose a web interface that users can connect to.

This is a Python library. The user can load the CSV with Pandas, do whatever filtering or slicing is needed, then call ``stt_sample_inspector.serve_df(dataframe)`` which will start the server. When the user is done inspecting/modifying the DataFrame, the function returns the modified DataFrame.

The module also provides convenience functions to make relative paths in the CSV absolute: ``stt_sample_inspector.utils.read_csv_and_absolutify`` (read from a file path) and ``stt_sample_inspector.utils.create_abs_column`` (create the column given a DataFrame and the folder to make paths relative to) The ``abs_wav_filename`` column created by those functions is required by the tool.

In addition, the package provides a CLI tool which takes two CSV files as parameters, one as input and one was output, where the modified DataFrame will be written to once the user is done editing.
