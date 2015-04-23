# GitReleaseNotes

The tool provides a way of customizing the process of generating the Release Notes based on:
- Issue tracking identifiers in commit messages
- Tags on commit
- Release artifacts repository

## Running the tool

python releaseNotesAll.py <configuration.json>


## Configuration

Configuration file is in flux. For now it looks something like this.

	{ 
		"pathToSave" : "<path>",
	    "WebImagesPath" : "<path to images>",
	    "JiraConf" : {
	        "JiraBrowseUrl" : "<jira browse url>",
	        "JiraRestSearchUrl" : "<jira rest search url>",
	        "Authorization" : "<jira auth>"
	    },
	    "Artifactory" : {
	        "StorageUrl" : "<artifactory url>"
	    },
	    "packages" : {
	        "<package name>" : {
	            "GitRepositoryUrl" : "<git repository url>",
	            "ArtifactoryRepository" : "<artifactory repository>",
	            "ArtifactoryArtifactUri" : "<artifactory artifact url>",
	            "WikiPageTitle" : "<wiki page title>",
	            "ReleaseNotesFormat" : "<format>",
	            "DirectDependencies" : {
	                "ANY" : {
	                    "type" : "<dependency type>"
	                }
	            }
	        }
	    }
	}


