.. image:: https://codeclimate.com/github/Cimpress-MCP/JustReleaseNotes/badges/gpa.svg
   :alt: Code Climate
   :target: https://codeclimate.com/github/Cimpress-MCP/JustReleaseNotes

.. image:: https://travis-ci.org/Cimpress-MCP/JustReleaseNotes.svg
   :alt: Code Climate
   :target: https://travis-ci.org/Cimpress-MCP/JustReleaseNotes

.. image:: https://coveralls.io/repos/Cimpress-MCP/JustReleaseNotes/badge.svg?branch=master
  :target: https://coveralls.io/r/Cimpress-MCP/JustReleaseNotes?branch=master


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
   
  & just_release notes -c <config.json>

Configuration
-------------

Configuration file is in flux. For now it is a json looking something like this::

    {
       "pathToSave" : <output path>,

        "packages" : {
            <package name> : {
                "Issues" : {
                    "Provider" : <issues provider>,
                    "HtmlUrl" : ...,
                    "Authorization" : ...,
                    "Url" : ...,
                    "WebImagesPath" : ...
                    "TicketRegex" : ...
                },
                "Releases" : {
                    "Provider" : <releases provider>,
                    "Repository" : ...,
                    "ArtifactUri" : ...,
                    "StorageUrl" : ...
                },
                "Source" : {
                    "Provider" : <source provider>
                    "RepositoryUrl" : ...
                },
                "ReleaseNotesWriter" : <notes writer>
            }
        }
    }

where

``notes writer`` is either:

- HtmlWriter
- MarkdownWriter

``releases provider`` is either:

- Artifactory
- GitHubReleases

``issues provider`` is either:

- JiraIssues
- GitHubIssues

``source provider`` is currently only:

- GitRepo

You can also use environment variables using the following syntax::

    {
        ...
        "key" : "aaa ENV[xxx] bbb"
        ...
    }

In the above example, ENV[xxx] will be replaced with the value of 'xxx' variable
