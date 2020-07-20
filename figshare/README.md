# FigShare

## First attempt

There are VU datasets in Figshare, but how do you search by affiliation?

- https://knowledge.figshare.com/articles/item/how-to-use-advanced-search-in-figshare- 
- https://figshare.com/search?q=VU%20AND%20amsterdam&searchMode=1&types=3
- https://figshare.com/search?q=Vrije%20AND%20amsterdam&searchMode=1&types=3

## Second attempt

### Using the logged in user website "search function"

Figshare has no insitution/affiliation field in it's metadata so you have to rely on what people put in the "desciption"! There is also no access to the users email from the the public search interface.

Search filters

- type: dataset 

The search function also defaults to a substring search (looking for individual words in a phrase) unless quoted and typed using the :: descriptors. In addition the search could be limited to:

`(:description: "VU" OR :description: "Vrije") AND :description: "Amsterdam"`

**NOTE** Figshare mirrors Zenodo, so search results that are returned as Zenodo are in fact datasets taken from Zenodo and shown as if they are somehow on FigShare, thus inflating their dataset and search result counts. I assume this is the same for the Mendalay and other "named" sources. These are useless results and will be ignored.

Not particularly impressive and the mirroring is just plain ... This combined with the lack of an institution metadata field means that this search is basically impossible on figshare ... so much for findability.

### Now we try they API (non-institutional access)

https://docs.figshare.com/#figshare_documentation_api_description_searching_filtering_and_pagination

Same search as above now in JSON, except cannot restrict to figshare results, so we get a whole bunch of mirrored results taken by figshare.

```json
{
  "order": "published_date",
  "search_for": "(:description: VU OR :description: Vrije) AND :description: Amsterdam",
  "order_direction": "desc"
}
```


```json
[
  {
    "defined_type_name": "presentation",
    "handle": "",
    "url_private_html": "https://figshare.com/account/articles/12300743",
    "timeline": {
      "publisherPublication": "2017-10-11T00:00:00",
      "revision": "2020-05-14T05:09:22",
      "firstOnline": "2020-05-14T05:09:19",
      "posted": "2020-05-14T05:09:19"
    },
    "url_private_api": "https://api.figshare.com/v2/account/articles/12300743",
    "url_public_api": "https://api.figshare.com/v2/articles/12300743",
    "id": 12300743,
    "doi": "10.5281/zenodo.3824310",
    "thumb": "https://s3-eu-west-1.amazonaws.com/ppreviews-zenodo-0712276593/22673300/thumb.png",
    "title": "BioExcel Webinar #17 - MDStudio, microservice based molecular dynamics workflows",
    "url": "https://api.figshare.com/v2/articles/12300743",
    "defined_type": 7,
    "resource_title": "",
    "url_public_html": "https://zenodo.figshare.com/articles/presentation/BioExcel_Webinar_17_-_MDStudio_microservice_based_molecular_dynamics_workflows/12300743",
    "resource_doi": "",
    "published_date": "2020-05-14T05:09:19Z",
    "group_id": 17126
  },
  {
    "defined_type_name": "dataset",
    "handle": "",
    "url_private_html": "https://figshare.com/account/articles/12229172",
    "timeline": {
      "revision": "2020-05-01T11:00:43",
      "firstOnline": "2020-05-01T11:00:43",
      "posted": "2020-05-01T11:00:43"
    },
    "url_private_api": "https://api.figshare.com/v2/account/articles/12229172",
    "url_public_api": "https://api.figshare.com/v2/articles/12229172",
    "id": 12229172,
    "doi": "10.6084/m9.figshare.12229172.v1",
    "thumb": "",
    "title": "Raw_Psychophysiological_Data_Dental_Anxiety_2020.xlsx",
    "url": "https://api.figshare.com/v2/articles/12229172",
    "defined_type": 3,
    "resource_title": "",
    "url_public_html": "https://figshare.com/articles/dataset/Raw_Psychophysiological_Data_Dental_Anxiety_2020_xlsx/12229172",
    "resource_doi": "",
    "published_date": "2020-05-01T11:00:43Z",
    "group_id": null
  },
  {
    "defined_type_name": "media",
    "handle": "",
    "url_private_html": "https://figshare.com/account/articles/12071571",
    "timeline": {
      "revision": "2020-04-02T20:25:30",
      "firstOnline": "2020-04-02T20:25:30",
      "posted": "2020-04-02T20:25:30"
    },
    "url_private_api": "https://api.figshare.com/v2/account/articles/12071571",
    "url_public_api": "https://api.figshare.com/v2/articles/12071571",
    "id": 12071571,
    "doi": "10.6084/m9.figshare.12071571.v1",
    "thumb": "https://s3-eu-west-1.amazonaws.com/pfigshare-u-previews/22185177/thumb.png",
    "title": "tomoPIV-subdModel-rollover.gif",
    "url": "https://api.figshare.com/v2/articles/12071571",
    "defined_type": 2,
    "resource_title": "",
    "url_public_html": "https://figshare.com/articles/media/tomoPIV-subdModel-rollover_gif/12071571",
    "resource_doi": "",
    "published_date": "2020-04-02T20:25:30Z",
    "group_id": null
  },
  {
    "defined_type_name": "presentation",
    "handle": "",
    "url_private_html": "https://figshare.com/account/articles/11770248",
    "timeline": {
      "publisherPublication": "2020-01-29T00:00:00",
      "revision": "2020-02-04T16:18:43",
      "firstOnline": "2020-01-30T08:52:32",
      "posted": "2020-01-30T08:52:32"
    },
    "url_private_api": "https://api.figshare.com/v2/account/articles/11770248",
    "url_public_api": "https://api.figshare.com/v2/articles/11770248",
    "id": 11770248,
    "doi": "10.5281/zenodo.3629176",
    "thumb": "https://s3-eu-west-1.amazonaws.com/ppreviews-zenodo-0712276593/21477198/thumb.png",
    "title": "Version control with Git",
    "url": "https://api.figshare.com/v2/articles/11770248",
    "defined_type": 7,
    "resource_title": "",
    "url_public_html": "https://zenodo.figshare.com/articles/presentation/Version_control_with_Git/11770248",
    "resource_doi": "",
    "published_date": "2020-01-30T08:52:32Z",
    "group_id": 17126
  },
  {
    "defined_type_name": "presentation",
    "handle": "",
    "url_private_html": "https://figshare.com/account/articles/11650065",
    "timeline": {
      "publisherPublication": "2019-11-19T00:00:00",
      "revision": "2020-01-20T00:15:22",
      "firstOnline": "2020-01-18T16:42:14",
      "posted": "2020-01-18T16:42:14"
    },
    "url_private_api": "https://api.figshare.com/v2/account/articles/11650065",
    "url_public_api": "https://api.figshare.com/v2/articles/11650065",
    "id": 11650065,
    "doi": "10.5281/zenodo.3543734",
    "thumb": "https://ndownloader.figshare.com/files/21148581/preview/21148581/thumb.png",
    "title": "How to use version control to improve reproducibility",
    "url": "https://api.figshare.com/v2/articles/11650065",
    "defined_type": 7,
    "resource_title": "",
    "url_public_html": "https://zenodo.figshare.com/articles/presentation/How_to_use_version_control_to_improve_reproducibility/11650065",
    "resource_doi": "",
    "published_date": "2020-01-18T16:42:14Z",
    "group_id": 17126
  },
  {
    "defined_type_name": "presentation",
    "handle": "",
    "url_private_html": "https://figshare.com/account/articles/11635179",
    "timeline": {
      "publisherPublication": "2017-07-05T00:00:00",
      "revision": "2020-01-17T05:32:12",
      "firstOnline": "2020-01-17T05:32:12",
      "posted": "2020-01-17T05:32:12"
    },
    "url_private_api": "https://api.figshare.com/v2/account/articles/11635179",
    "url_public_api": "https://api.figshare.com/v2/articles/11635179",
    "id": 11635179,
    "doi": "10.5281/zenodo.3610195",
    "thumb": "https://ndownloader.figshare.com/files/21101991/preview/21101991/thumb.png",
    "title": "3.2 Digital Humanities Clinics – Leading Dutch Librarians into DH",
    "url": "https://api.figshare.com/v2/articles/11635179",
    "defined_type": 7,
    "resource_title": "",
    "url_public_html": "https://zenodo.figshare.com/articles/presentation/3_2_Digital_Humanities_Clinics_Leading_Dutch_Librarians_into_DH/11635179",
    "resource_doi": "",
    "published_date": "2020-01-17T05:32:12Z",
    "group_id": 17126
  },
  {
    "defined_type_name": "presentation",
    "handle": "",
    "url_private_html": "https://figshare.com/account/articles/11633853",
    "timeline": {
      "publisherPublication": "2015-06-26T00:00:00",
      "revision": "2020-01-22T19:36:29",
      "firstOnline": "2020-01-16T22:29:57",
      "posted": "2020-01-16T22:29:57"
    },
    "url_private_api": "https://api.figshare.com/v2/account/articles/11633853",
    "url_public_api": "https://api.figshare.com/v2/articles/11633853",
    "id": 11633853,
    "doi": "10.5281/zenodo.3603206",
    "thumb": "https://ndownloader.figshare.com/files/21097815/preview/21097815/thumb.png",
    "title": "11.2 Selecting Research Data for Reuse: Challenges During the Implementation of Support for Data Archiving in Research Libraries",
    "url": "https://api.figshare.com/v2/articles/11633853",
    "defined_type": 7,
    "resource_title": "",
    "url_public_html": "https://zenodo.figshare.com/articles/presentation/11_2_Selecting_Research_Data_for_Reuse_Challenges_During_the_Implementation_of_Support_for_Data_Archiving_in_Research_Libraries/11633853",
    "resource_doi": "",
    "published_date": "2020-01-16T22:29:57Z",
    "group_id": 17126
  },
  {
    "defined_type_name": "dataset",
    "handle": "",
    "url_private_html": "https://figshare.com/account/articles/8963519",
    "timeline": {
      "publisherPublication": "2018-04-20T08:19:57",
      "revision": "2019-07-19T09:42:57",
      "firstOnline": "2019-07-19T09:42:57",
      "posted": "2019-07-19T09:42:57"
    },
    "url_private_api": "https://api.figshare.com/v2/account/articles/8963519",
    "url_public_api": "https://api.figshare.com/v2/articles/8963519",
    "id": 8963519,
    "doi": "10.17632/53cskwwpdn.1",
    "thumb": "https://s3-eu-west-1.amazonaws.com/ppreviews-mendeley-2843568692/16398383/thumb.png",
    "title": "Project: Fostering Transparent and Responsible Conduct of Research: What can Journals do?",
    "url": "https://api.figshare.com/v2/articles/8963519",
    "defined_type": 3,
    "resource_title": "",
    "url_public_html": "https://mendeley.figshare.com/articles/dataset/Project_Fostering_Transparent_and_Responsible_Conduct_of_Research_What_can_Journals_do_/8963519",
    "resource_doi": "",
    "published_date": "2019-07-19T09:42:57Z",
    "group_id": 23331
  },
  {
    "defined_type_name": "media",
    "handle": "",
    "url_private_html": "https://figshare.com/account/articles/8797286",
    "timeline": {
      "publisherPublication": "2019-07-04T00:00:00",
      "revision": "2019-07-08T06:05:43",
      "firstOnline": "2019-07-08T06:05:43",
      "posted": "2019-07-08T06:05:43"
    },
    "url_private_api": "https://api.figshare.com/v2/account/articles/8797286",
    "url_public_api": "https://api.figshare.com/v2/articles/8797286",
    "id": 8797286,
    "doi": "10.5281/zenodo.3268518",
    "thumb": "",
    "title": "Measuring Impact: Research Assessment",
    "url": "https://api.figshare.com/v2/articles/8797286",
    "defined_type": 2,
    "resource_title": "",
    "url_public_html": "https://zenodo.figshare.com/articles/media/Measuring_Impact_Research_Assessment/8797286",
    "resource_doi": "",
    "published_date": "2019-07-08T06:05:43Z",
    "group_id": 17126
  },
  {
    "defined_type_name": "presentation",
    "handle": "",
    "url_private_html": "https://figshare.com/account/articles/8311151",
    "timeline": {
      "publisherPublication": "2019-06-21T00:00:00",
      "revision": "2019-08-01T09:51:53",
      "firstOnline": "2019-06-22T07:28:57",
      "posted": "2019-06-22T07:28:57"
    },
    "url_private_api": "https://api.figshare.com/v2/account/articles/8311151",
    "url_public_api": "https://api.figshare.com/v2/articles/8311151",
    "id": 8311151,
    "doi": "10.5281/zenodo.3251806",
    "thumb": "https://s3-eu-west-1.amazonaws.com/ppreviews-zenodo-0712276593/15571937/thumb.png",
    "title": "VU Data Conversations: Open Data, Open Methods, Reproducible Research",
    "url": "https://api.figshare.com/v2/articles/8311151",
    "defined_type": 7,
    "resource_title": "",
    "url_public_html": "https://zenodo.figshare.com/articles/presentation/VU_Data_Conversations_Open_Data_Open_Methods_Reproducible_Research/8311151",
    "resource_doi": "",
    "published_date": "2019-06-22T07:28:57Z",
    "group_id": 17126
  }
]
```

### Conclusion
The easiest will be to do this by hand from the web interface. Welcome to findable data ... courtesy of figshare.
