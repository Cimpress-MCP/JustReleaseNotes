.. image:: https://codeclimate.com/github/Cimpress-MCP/JustReleaseNotes/badges/gpa.svg
   :alt: Code Climate
   :align: left
   :target: https://codeclimate.com/github/Cimpress-MCP/JustReleaseNotes

.. image:: https://codeclimate.com/github/Cimpress-MCP/JustReleaseNotes/badges/coverage.svg
   :alt: Code Climate
   :align: left
   :target: https://codeclimate.com/github/Cimpress-MCP/JustReleaseNotes

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
	            },
	            "Releases" : {
	              "Provider" : <releases provider>,
	              "Repository" : ...,
	              "ArtifactUri" : ...,
	              "StorageUrl" : ...
	            },
	            "GitRepositoryUrl" : ...,
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
