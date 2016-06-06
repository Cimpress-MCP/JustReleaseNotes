.. image:: https://codeclimate.com/github/Cimpress-MCP/JustReleaseNotes/badges/gpa.svg
   :alt: Code Climate
   :target: https://codeclimate.com/github/Cimpress-MCP/JustReleaseNotes

.. image:: https://travis-ci.org/Cimpress-MCP/JustReleaseNotes.svg
   :alt: Code Climate
   :target: https://travis-ci.org/Cimpress-MCP/JustReleaseNotes

.. image:: https://coveralls.io/repos/Cimpress-MCP/JustReleaseNotes/badge.svg?branch=master
   :alt: Coveralls
   :target: https://coveralls.io/r/Cimpress-MCP/JustReleaseNotes?branch=master

.. image:: https://img.shields.io/pypi/v/JustReleaseNotes.svg
   :alt: PyPI
   :target: https://pypi.python.org/pypi/JustReleaseNotes/

.. image:: https://img.shields.io/pypi/dm/JustReleaseNotes.svg
   :alt: PyPI
   :target: https://pypi.python.org/pypi/JustReleaseNotes/


==================
Just Release Notes
==================

The tool provides a way of customizing the process of generating the Release Notes based on:

- Issue tracking identifiers in commit messages
- Tags on commit
- Release artifacts repository

----------------
Running the tool
----------------

Usage
-----

To run the tool, call::
   
  & just_release --config <config.json> notes

Configuration
-------------

Configuration file is in flux. For now it is a json looking something like this::

    {
       "pathToSave" : <output path>,

        "packages" : {
            <package name> : {
                "Issues" : [{
                    "Provider" : <issues provider>,
                    "HtmlUrl" : ...,
                    "Authorization" : ...,
                    "Url" : ...,
                    "WebImagesPath" : ...,
                    "TicketRegex" : ...
                }],
                "Releases" : {
                    "Provider" : <releases provider>,
                    "Repository" : ...,
                    "ArtifactUri" : ...,
                    "StorageUrl" : ...
                },
                "Source" : {
                    "Provider" : <source provider>,
                    "RepositoryUrl" : ...,
                    "Remote" : ...,
                    "Branch" : ...,
                    "VersionTagRegex" : "^([0-9]+\\.[0-9]+\\.[0-9]+)$",
                    "OldestCommitToProcess" : <commit hexsha>,
                    "ExcludeCommitsWithMessageMatchingRegex" : <regex>
                },
                "ReleaseNotesWriter" : [{
                    "Provider" : <notes writer provider>
                    "PathToSave" : ...
                }]
            }
        }
    }

where

``notes writer provider`` is either:

- HtmlWriter
- MarkdownWriter
- JsonWriter

``releases provider`` is either:

- Artifactory
- GitHubReleases

``issues provider`` is either:

- JiraIssues
- GitHubIssues

It is also possible to specify an array of issue providers, then all of them will be used to retrieve information about tickets.

``source provider`` is currently only:

- GitRepo

You can also use environment variables using the following syntax::

    {
        ...
        "key" : "aaa ENV[xxx] bbb"
        ...
    }

In the above example, ENV[xxx] will be replaced with the value of 'xxx' variable
