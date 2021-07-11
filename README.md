# Simple Flask Note Application

Flask Note is simple application base on Python, Flask and Flask-SQLAlchemy
support Restful JSON

> Sometime I'm search and research data from internet too much, I don't
remember what about data searched, to save time spends search data again,
thus I'm created this tool, it's small and help me while research data 
have been search from internet

## Requirements

1. Python 3
2. Flask
3. Flask-SQLAlchemy

## Installation

Clone the repository

```
mkdir ~/flask-apps && cd ~/flask-apps
git clone https://github.com/hoathienvu8x/Flask-Note notes
cd notes && mkdir app/data
pip3 install -r requirements.txt
./note initdb
```

## Run

```
cd ~/flask-apps/notes
chmod +x ./note
./note
```

## Routes

To add or update note using `/api/note` methods allowed `POST`, `GET`

**Params:**

- `id` required for update type `Int`
- `content` required type `String`
- `status` optional [publish,draft,trash,pending] type `String`
- `url` optional type `String` url source of content to copy
- `name` optional type `String` name to suggetion search data again or
name of site to get content

**Response:**

On success reponse `JSON` object key is `data`, or `JSON` object key `error`

To remove note using `/api/note/remove` methods allowed `POST`, `GET`

**Params**

`id` or `node`, `node` is `slug` field of table, `id` type is `Int`, `node`
type is `String`

**Response:**

On success reponse `JSON` object key is `message`, or `JSON` object key `error`

To get or search note using `/api/note/query` methods allowed `POST`, `GET`

**Params:**

`action` action get or search type `String` default `get`, if `action` is
`search` the param `s` is required with `s` type `String` this is keyword
for search data

if `action` is `get` default get all `Note` in database if `status` is `publish`
to query by status using `state` param type is `String` [all, publish, pending, draft, trash]

`id` type `Int`, `node` type `String` to get single `Note`, `node` param
is `slug` field in table

**Response:**

On success reponse `JSON` object key is `data`, or `JSON` object key `error`
if get single `Note` the `data` is object of `Note` else `data` is
array of `Note`

## Updated

On route `/api/note/query` add support to custom response object and paging

Add params `page`, `limit` type is `Int` and must be greater than 0, `page`
default value is `1` and `limit` default value is `5`

Add param `fields` type is `String` the fields to response of object separator
`,` default `["node", "content", "status", "timestamp"]`
that mean `fields=node,content,status,timestamp`

_2021-07-10 @10:34_

Update route `/api/note/query` action `get` + `search` add three key that
is `num_results`, `page`, `total_pages` because I want know exactly the mine query
worked (current page, total results response and total pages results)

The result of response will be

```
{
  "num_results":1,
  "data":[
    {
      "content":"I'm working on a ...",
      "node":"ce8147bcc81e4d661b8c2f9b46e43531_1625886495",
      "timestamp":"2021-07-10T10:40:15.547653"
    }
  ],
  "page":1,
  "total_pages":1
}
```

_2021-07-11 @16:14_

Move params endpoint handle to dict param to easy call and pass data from
code without request that mean change `request` to `args` with `args` is
dict instance

**Switch branch `master` to `note-gui` and development template + gui**

_2021-07-11 @18:20_

1. Add node `/api/node/recents` to get all `Notes` 24 hours ago
2. Add node `/api/node/hits` to get all `Notes` load to read

Update reponse list to short content data on query get list of notes, set
views when query note single

_2021-07-12 @00:10_

To access gui using uri `/graph/` all display is simple, using markdown
python to parse markdown text

## Client

This application using `curl` command or `fetch` API of javascript to send
data or using webbrower navigate to `http://127.0.0.1:9800`
